#!/usr/bin/env python3
"""validate_markdown_delivery.py v2 - markdown-it-py block-aware validator.

v2 replaces the line-by-line skip heuristics of v1 with the CommonMark token
stream from markdown-it-py (the parser behind mdformat/mkdocs). Every line is
classified by its TOKEN's block semantics, so:

  - fenced / indented code tokens  -> content is code, checks skipped
  - html_block tokens              -> raw HTML residue; if it is a
                                      table-structure block it gets the
                                      `indented-html-table` code (fix with
                                      convert_leftover_html_tables.py),
                                      otherwise `active-html`
  - heading tokens                 -> exact H1 counting (level 1 only)
  - everything else                -> visible content: bare-page-number,
                                      image-markup, active-html checks

v1's hole: any 4-space-indented line was skipped as "code", so EPUB tables
left as indented raw HTML (<table>/<tr>/<td>...) passed validation. markdown-it
-py reports those as html_block tokens regardless of indentation.

Same CLI as v1:  python3 validate_markdown_v2.py <file|dir> [--json-report F]
"""
import argparse
import json
import pathlib
import re
import sys

try:
    from markdown_it import MarkdownIt
except ImportError:
    sys.stderr.write("markdown-it-py is required: pip install markdown-it-py\n")
    sys.exit(2)

CANONICAL_FILENAME_PATTERN = re.compile(r"^[A-Z0-9][A-Za-z0-9_ -]{0,88}[A-Za-z0-9]-[12][0-9]{3}\.md$")
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\([^)]*\)|<img\b|\[Start Picture-Text\]", re.IGNORECASE)
BARE_PAGE_PATTERN = re.compile(r"^\d{1,4}$")
STRUCTURED_SOURCE_PATTERN = re.compile(r"^(?:structured|source)\s*:", re.MULTILINE | re.IGNORECASE)

# ============================================================
# Tag policy - MAINTAINABLE ALLOWLIST with diagnosis.
#
# `ALLOWED_TAGS`: tags that may remain in delivered markdown. EPUB converters
#   emit <sub>/<sup> for chemistry/isotope notation - keep them as semantic
#   HTML per the delivery contract. To allow a new tag, add it here.
#
# ANY tag outside the allowlist is flagged, but the DIAGNOSIS depends on the
# tag's kind:
#   - `disallowed-html`  : the tag is in EPUB_RESIDUE_TAGS (ol, ul, li, p, br,
#     table-family, span, div, em, strong, u, mark, cite, wbr, aside, ...) -
#     markup the pipeline should have unwrapped, converted to GFM, or escaped.
#   - `code-not-fenced`  : the tag is an UNKNOWN name (<dyn>, <u8>, <book>,
#     <reaction>, ...). That is NOT HTML residue - it is code or XML that
#     escaped its code block (e.g. a fence-parity defect left it unfenced).
#     The fix is to wrap the surrounding lines in a code block, or re-convert
#     from source. An allowlist (not a deny list) is required here: hitting an
#     unknown tag is the SIGNAL that a code block is missing.
#
# To allow a new tag, add it here (and update the skill's validator-cleanup.md).
ALLOWED_TAGS = {"sub", "sup"}

# Tags that are known EPUB/PDF conversion residue (flag as disallowed-html).
EPUB_RESIDUE_TAGS = {
    "a", "abbr", "address", "article", "aside", "b", "blockquote", "br",
    "button", "caption", "cite", "code", "col", "colgroup", "dd", "del",
    "details", "dfn", "div", "dl", "dt", "em", "fieldset", "figcaption",
    "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
    "header", "hgroup", "hr", "i", "img", "input", "ins", "kbd", "label",
    "legend", "li", "main", "mark", "menu", "nav", "ol", "optgroup", "option",
    "p", "pre", "progress", "q", "s", "samp", "script", "section", "select",
    "small", "span", "strong", "style", "summary", "table", "tbody", "td",
    "textarea", "tfoot", "th", "thead", "tr", "u", "ul", "var", "wbr",
}

# HTML tags that indicate a leftover raw table (for the indented-html-table code).
TABLE_STRUCTURE_TAG = re.compile(
    r"</?(?:table|tbody|thead|tfoot|tr|td|th|colgroup|col)\b", re.IGNORECASE
)

# ============================================================
# Code-block policy - MAINTAINABLE PER-SUBJECT LIST.
#
# Prose-only subjects (genetics, biology, biochemistry, ...) normally contain
# no code; a fence there is usually a conversion artifact. Reported as
# `unexpected-code-block` only when code is PREVALENT (>=5 blocks or >=1% of
# non-empty lines) - a lone legitimate snippet is tolerated. Per-book opt-out:
# set `allow_code_blocks: true` in frontmatter.
#
# NOTE: computational/statistical subjects (bayesian, statistics, biostatistics,
# bioinformatics, prompt_engineering, linear_algebra, accessibility) are NOT
# listed here even though they sit in the sciences - their books legitimately
# carry Python/R code as subject matter (measured: 1000-3800 fences across the
# corpus). Keep this list to TRUE prose subjects.
NO_CODE_SUBJECTS = {
    "assessment_taxonomy", "biochemistry", "biology",
    "biology_adjacent_subjects", "biophysics", "biotech",
    "business_plans", "cell_biology", "chemistry", "eugenics", "film_studies",
    "fourier_transforms", "genetics_history", "inheritance_genetics",
    "mathematical_biology", "medicinal_chemistry", "molecular_biology",
    "protein_structure", "rosalind_franklin", "virology",
}

# code-ish token types whose content must never be checked
CODE_TOKEN_TYPES = {"fence", "code_block"}
# tokens that open a block whose CONTENT lines we already handled as block
# (we only need inline tokens and headings; container tokens carry no text)
SKIP_TOKEN_TYPES = {
    "paragraph_open", "paragraph_close", "heading_open", "heading_close",
    "bullet_list_open", "bullet_list_close", "ordered_list_open",
    "ordered_list_close", "list_item_open", "list_item_close",
    "blockquote_open", "blockquote_close", "table_open", "table_close",
    "thead_open", "thead_close", "tbody_open", "tbody_close",
    "tr_open", "tr_close", "th_open", "th_close", "td_open", "td_close",
    "hr", "softbreak", "hardbreak",
}


class ValidationIssue:
    __slots__ = ("code", "path", "line", "message")

    def __init__(self, code: str, path: pathlib.Path, line: int, message: str) -> None:
        self.code = code
        self.path = str(path)
        self.line = line
        self.message = message

    def as_dict(self) -> dict:
        return {"code": self.code, "path": self.path, "line": self.line, "message": self.message}


#============================================
def validate_filename(path: pathlib.Path) -> list[ValidationIssue]:
    issues = []
    filename = path.name
    if any(ord(c) > 127 for c in filename):
        issues.append(ValidationIssue("filename-nonascii", path, 0, "filename must contain only ASCII characters"))
    if CANONICAL_FILENAME_PATTERN.fullmatch(filename) is None:
        issues.append(ValidationIssue(
            "filename-shape", path, 0,
            "use metadata title words joined by underscores plus -YYYY.md",
        ))
    if re.search(r"(?:^|_)(?:from_)?(?:pdf|epub)(?:_|-\d{4}\.md$)", filename, re.IGNORECASE):
        issues.append(ValidationIssue("source-suffix", path, 0, "remove source-specific PDF or EPUB suffixes"))
    return issues


#============================================
def frontmatter_policy(text: str) -> dict:
    """Read policy opt-outs from the YAML frontmatter.

    Supported keys (all optional):
      allow_code_blocks: true   - the book legitimately contains code
                                  (e.g. an R/Python snippet in a genetics book)
      allow_tags: [em, strong]  - extra HTML tags this book may keep
    """
    policy = {"allow_code_blocks": False, "allow_tags": set()}
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return policy
    fm = m.group(1)
    m2 = re.search(r"^allow_code_blocks:\s*(true|yes|1)\s*$", fm, re.M | re.I)
    if m2:
        policy["allow_code_blocks"] = True
    m3 = re.search(r"^allow_tags:\s*\[(.*?)\]", fm, re.M | re.I)
    if m3:
        for t in m3.group(1).split(","):
            t = t.strip().strip("'\"")
            if t:
                policy["allow_tags"].add(t.lower())
    return policy


#============================================
def subject_of(path: pathlib.Path) -> str:
    """Return the delivery subject dir (the parent folder name)."""
    return path.parent.name


#============================================
def tag_names(html_text: str) -> set[str]:
    """Return ALL tag names in an HTML fragment (allowlist semantics).

    Any tag outside ALLOWED_TAGS is flagged. The caller classifies each tag as
    `disallowed-html` (in EPUB_RESIDUE_TAGS) or `code-not-fenced` (unknown
    name = XML/Rust/custom markup that escaped its code block).
    """
    return {m.lower() for m in re.findall(r"</?([a-z][a-z0-9-]*)\b", html_text, re.I)}


#============================================
def classify_tags(tags: set[str]) -> tuple[set[str], set[str]]:
    """Split tag names into (residue, unfenced_code).

    residue       = known EPUB/PDF conversion-residue tags (disallowed-html)
    unfenced_code = unknown names - code/XML that escaped its fence
                    (code-not-fenced)
    """
    residue = tags & EPUB_RESIDUE_TAGS
    unfenced = tags - EPUB_RESIDUE_TAGS - ALLOWED_TAGS
    return residue, unfenced


#============================================
def validate_text(path: pathlib.Path, text: str) -> list[ValidationIssue]:
    issues = []
    lines = text.splitlines()
    structured_source = STRUCTURED_SOURCE_PATTERN.search(text) is not None
    subject = subject_of(path)
    policy = frontmatter_policy(text)
    allowed_tags = ALLOWED_TAGS | policy["allow_tags"]
    md = MarkdownIt("commonmark", {"html": True})
    tokens = md.parse(text)

    code_lines: set[int] = set()      # 0-based lines inside code tokens
    html_block_lines: set[int] = set()  # every line covered by an html_block token
    html_block_issues: dict[int, str] = {}  # start line -> issue code
    code_block_lines: list[int] = []   # 1-based start lines of code tokens
    for token in tokens:
        if token.type in CODE_TOKEN_TYPES and token.map is not None:
            for ln in range(token.map[0], token.map[1]):
                code_lines.add(ln)
            code_block_lines.append(token.map[0] + 1)
        elif token.type == "html_block" and token.map is not None:
            start = token.map[0]
            for ln in range(token.map[0], token.map[1]):
                html_block_lines.add(ln)
            if TABLE_STRUCTURE_TAG.search(token.content):
                html_block_issues[start] = "indented-html-table"
            else:
                residue, unfenced = classify_tags(set(tag_names(token.content)) - allowed_tags)
                if residue:
                    html_block_issues[start] = "disallowed-html"
                elif unfenced:
                    html_block_issues[start] = "code-not-fenced"

    # code-block policy: prose subjects normally have no code. A lone snippet
    # is tolerated; flag only when code is PREVALENT (>=5 blocks or >=1% of
    # non-empty lines). Frontmatter `allow_code_blocks: true` opts the book out.
    if subject in NO_CODE_SUBJECTS and not policy["allow_code_blocks"]:
        nonempty = sum(1 for l in lines if l.strip())
        code_lines_count = len(code_block_lines)
        # count fenced lines for the share
        fenced_share = len(code_lines) / max(nonempty, 1)
        if code_lines_count >= 5 or fenced_share >= 0.01:
            issues.append(ValidationIssue(
                "unexpected-code-block", path, code_block_lines[0] if code_block_lines else 0,
                f"prose subject: {code_lines_count} code blocks ({fenced_share:.0%} of non-empty lines) "
                f"- expected none; set allow_code_blocks: true in frontmatter if intentional",
            ))

    # H1 count from heading tokens (level 1 only) - exact, no fence-guessing
    h1_lines = [t.map[0] + 1 for t in tokens if t.type == "heading_open" and t.tag == "h1" and t.map]
    if len(h1_lines) != 1:
        issues.append(ValidationIssue(
            "h1-count", path, 0, f"expected exactly one H1; found {len(h1_lines)}"
        ))

    # non-ASCII check (first offending line only, same as v1)
    for index, line in enumerate(lines):
        if any(ord(c) > 127 for c in line):
            issues.append(ValidationIssue(
                "nonascii-content", path, index + 1,
                "replace raw non-ASCII text with ASCII or entities",
            ))
            break

    # per-line checks on visible content
    for index, line in enumerate(lines):
        if index in code_lines or index in html_block_lines:
            continue
        if index in html_block_issues:
            code = html_block_issues[index]
            if code == "indented-html-table":
                msg = "convert indented HTML table markup to GFM pipe tables or fenced text"
            elif code == "code-not-fenced":
                msg = "unknown tags suggest code/XML that escaped its fence; wrap in a code block or re-convert"
            else:
                msg = "unwrap or escape HTML tags not in the allowlist"
            issues.append(ValidationIssue(code, path, index + 1, msg))
            continue
        if not structured_source and BARE_PAGE_PATTERN.fullmatch(line):
            issues.append(ValidationIssue("bare-page-number", path, index + 1, "remove the page-only line"))
        visible = re.sub(r"`[^`]*`", "", line)  # strip inline code spans
        if IMAGE_PATTERN.search(visible):
            issues.append(ValidationIssue(
                "image-markup", path, index + 1,
                "remove image markup while retaining useful captions",
            ))
    # inline HTML via token children (precise, code-aware) - one issue per
    # line, classified by tag kind (deduped)
    inline_bad: dict[int, set[str]] = {}
    inline_unfenced: dict[int, set[str]] = {}
    for token in tokens:
        if token.type == "inline" and token.map and token.children:
            for child in token.children:
                if child.type == "html_inline":
                    tags = set(tag_names(child.content)) - allowed_tags
                    if tags:
                        residue, unfenced = classify_tags(tags)
                        if residue:
                            inline_bad.setdefault(token.map[0] + 1, set()).update(residue)
                        if unfenced:
                            inline_unfenced.setdefault(token.map[0] + 1, set()).update(unfenced)
    for ln, bad in sorted(inline_bad.items()):
        issues.append(ValidationIssue(
            "disallowed-html", path, ln,
            f"unwrap or escape HTML tags not in the allowlist: {', '.join(sorted(bad))}",
        ))
    for ln, bad in sorted(inline_unfenced.items()):
        issues.append(ValidationIssue(
            "code-not-fenced", path, ln,
            f"unknown tags suggest code/XML that escaped its fence: {', '.join(sorted(bad))} - wrap in a code block or re-convert",
        ))
    return issues


#============================================
def validate_one(path: pathlib.Path) -> list[ValidationIssue]:
    if path.suffix.lower() != ".md":
        return []
    # README / index files are corpus scaffolding, not book deliverables
    if path.name.lower() in ("readme.md", "readme.txt", "index.md"):
        return []
    issues = validate_filename(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        issues.append(ValidationIssue("unreadable", path, 0, str(exc)))
        return issues
    issues.extend(validate_text(path, text))
    return issues


#============================================
def main() -> int:
    parser = argparse.ArgumentParser(description="v2 markdown-it-py delivery validation")
    parser.add_argument("input", help="markdown file or directory")
    parser.add_argument("-j", "--json-report", metavar="F", help="write machine-readable report")
    args = parser.parse_args()

    inp = pathlib.Path(args.input)
    files = sorted(inp.rglob("*.md")) if inp.is_dir() else [inp]

    all_issues = []
    for f in files:
        all_issues.extend(validate_one(f))

    report = {
        "validator": "v2",
        "input": str(inp),
        "status": "PASS" if not all_issues else "FAIL",
        "file_count": len(files),
        "issue_count": len(all_issues),
        "files": sorted({i.path for i in all_issues}),
        "issues": [i.as_dict() for i in all_issues],
    }
    if args.json_report:
        pathlib.Path(args.json_report).write_text(json.dumps(report, indent=1))

    print("Delivery validation (v2 markdown-it-py)")
    if all_issues:
        print(f"Status: FAIL ({len(all_issues)} issues in {len(report['files'])} files)")
        for i in all_issues[:50]:
            print(f"- {i.path}:{i.line} [{i.code}] {i.message}")
        if len(all_issues) > 50:
            print(f"- ... {len(all_issues) - 50} additional issues; use --json-report for the complete list")
    else:
        print("Status: PASS")
        print(f"Markdown files: {len(files)}")
        print("Issues: 0")
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
