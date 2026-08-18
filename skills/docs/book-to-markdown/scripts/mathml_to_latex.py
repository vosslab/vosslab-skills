#!/usr/bin/env python3
"""Convert MathML to LaTeX — standalone, or targeted in-place repair inside a Markdown text block.

Two modes:

1. Standalone conversion (read MathML from a string, a file, or stdin):
       echo '<math>...</math>' | mathml_to_latex.py
       mathml_to_latex.py --mathml '<math>...</math>'
       mathml_to_latex.py --input fragment.html

2. Markdown text-block repair (extract <math> blocks from a line range, convert
   them, and print or write back the result):
       mathml_to_latex.py --markdown book.md --lines 120:180               # dry-run: print replacements
       mathml_to_latex.py --markdown book.md --lines 120:180 -o fixed.md    # write a separate corrected file
       mathml_to_latex.py --markdown book.md --lines 120:180 --in-place     # rewrite the file (backup kept)

Backends are tried in order until one succeeds:
    1. an embedded LaTeX <annotation encoding="application/x-tex"> is extracted verbatim,
    2. pandoc (most robust; preserves inline vs display and numeric entities),
    3. the 'mathml-to-latex' PyPI package,
    4. sympy (expression-level MathML only).
If every backend fails the block is left unchanged and reported with status
'unconverted' — content is never silently dropped.

Input forms handled: single-line and multi-line <math> blocks, blocks inside
HTML comments (<!-- <math>...</math> -->, which are replaced by active LaTeX),
and HTML-escaped (&lt;math&gt; ... &lt;/math&gt;) blocks.
"""

import argparse
import bisect
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------- backends

RE_ANNOTATION_TEX = re.compile(
    r'<annotation[^>]*encoding=["\']application/x-tex["\'][^>]*>(.*?)</annotation>',
    re.DOTALL | re.IGNORECASE,
)


def _extract_annotation_tex(mathml: str) -> str | None:
    """Return embedded LaTeX from an x-tex annotation, or None."""
    m = RE_ANNOTATION_TEX.search(mathml)
    if not m:
        return None
    return html.unescape(m.group(1)).strip()


def _pandoc(mathml: str) -> str:
    """Convert one <math> block with pandoc; returns bare LaTeX plus a display flag."""
    proc = subprocess.run(
        ["pandoc", "-f", "html", "-t", "latex"],
        input=mathml,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "pandoc failed")
    return proc.stdout.strip()


def _mathml_to_latex_pkg(mathml: str) -> str:
    """Convert with the 'mathml-to-latex' PyPI package."""
    try:
        from mathml_to_latex import MathMLToLaTeX  # type: ignore
    except ImportError as exc:
        raise RuntimeError("mathml-to-latex not installed") from exc
    return MathMLToLaTeX().convert(mathml)


def _sympy(mathml: str) -> str:
    """Convert expression-level MathML with sympy."""
    try:
        from sympy import latex  # type: ignore
        from sympy.parsing.mathml import parse_mathml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("sympy not installed") from exc
    return latex(parse_mathml(mathml))


def _strip_paren(latex: str) -> tuple[str, bool]:
    """Split pandoc output into (bare_latex, is_display)."""
    latex = latex.strip()
    if latex.startswith("\\["):
        return latex[2:].rstrip().removesuffix("\\]").strip(), True
    if latex.startswith("\\("):
        return latex[2:].rstrip().removesuffix("\\)").strip(), False
    return latex, False


def _display_attr(mathml: str) -> bool:
    """True when the <math> opening tag declares display mode."""
    m = re.match(r"<math\b[^>]*>", mathml, re.IGNORECASE)
    if not m:
        return False
    return re.search(r'display\s*=\s*["\']block["\']', m.group(0), re.IGNORECASE) is not None


def convert_mathml(mathml: str) -> tuple[str, bool, str]:
    """Convert a <math>...</math> string to (bare_latex, is_display, backend).

    Raises RuntimeError if no backend succeeds.
    """
    embedded = _extract_annotation_tex(mathml)
    if embedded:
        return embedded, _display_attr(mathml), "annotation/x-tex"

    errors: list[str] = []
    try:
        out = _pandoc(mathml)
        latex, display = _strip_paren(out)
        return latex, display, "pandoc"
    except Exception as exc:  # noqa: BLE001
        errors.append(f"pandoc: {exc}")

    try:
        latex = _mathml_to_latex_pkg(mathml)
        return latex.strip(), _display_attr(mathml), "mathml-to-latex"
    except Exception as exc:  # noqa: BLE001
        errors.append(f"mathml-to-latex: {exc}")

    try:
        latex = _sympy(mathml)
        return latex.strip(), _display_attr(mathml), "sympy"
    except Exception as exc:  # noqa: BLE001
        errors.append(f"sympy: {exc}")

    raise RuntimeError("; ".join(errors))


# ---------------------------------------------------------------- rendering

DELIMITERS = ("dollar", "paren", "bare")


def render(latex: str, is_display: bool, delimiter: str) -> str:
    """Wrap bare LaTeX in the requested delimiter style."""
    if delimiter == "dollar":
        return f"$${latex}$$" if is_display else f"${latex}$"
    if delimiter == "paren":
        return f"\\[{latex}\\]" if is_display else f"\\({latex}\\)"
    if delimiter == "bare":
        return latex
    raise ValueError(f"unknown delimiter {delimiter!r}")


# ---------------------------------------------------------------- extraction

RE_MATH = re.compile(r"<math\b[^>]*>.*?</math>", re.DOTALL | re.IGNORECASE)
RE_ESCAPED_MATH = re.compile(r"&lt;math\b.*?&lt;/math&gt;", re.DOTALL | re.IGNORECASE)


def _mathml_from_escaped(escaped: str) -> str:
    return html.unescape(escaped)


def find_blocks(text: str) -> list[dict]:
    """Return every MathML block as {start, end, raw, xml, is_display, escaped}.

    A block inside an HTML comment is expanded to include the comment delimiters
    so the whole <!-- <math>...</math> --> is replaced by active LaTeX.
    """
    spans: list[tuple[int, int]] = []
    for m in RE_ESCAPED_MATH.finditer(text):
        spans.append((m.start(), m.end()))
    for m in RE_MATH.finditer(text):
        start, end = m.start(), m.end()
        before = text[:start]
        open_comment = before.rfind("<!--")
        close_comment = before.rfind("-->")
        if open_comment > close_comment:
            start = open_comment
            after = text.find("-->", end)
            if after != -1:
                end = after + 3
        spans.append((start, end))

    blocks = []
    for start, end in sorted(set(spans)):
        raw = text[start:end]
        escaped = raw.lstrip().startswith("&lt;math")
        xml = _mathml_from_escaped(raw) if escaped else raw
        inner = RE_MATH.search(xml)
        xml = inner.group(0) if inner else xml
        blocks.append({
            "start": start,
            "end": end,
            "raw": raw,
            "xml": xml,
            "is_display": _display_attr(xml),
            "escaped": escaped,
        })
    return blocks


# ---------------------------------------------------------------- line range

def parse_lines(spec: str | None, total: int) -> tuple[int, int]:
    """Parse 'L' or 'L1:L2' (1-based inclusive) into (start, end)."""
    if not spec:
        return 1, total
    if ":" in spec:
        a, b = spec.split(":", 1)
        start = int(a) if a else 1
        end = int(b) if b else total
    else:
        start = end = int(spec)
    start = max(1, min(start, total))
    end = max(start, min(end, total))
    return start, end


def line_offsets(text: str) -> list[int]:
    """Character offset of each 1-based line start; final entry is len(text)."""
    offsets = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            offsets.append(i + 1)
    offsets.append(len(text))
    return offsets


def line_of(offsets: list[int], pos: int) -> int:
    """1-based line number containing character offset pos."""
    return bisect.bisect_right(offsets, pos)  # idx of first offset > pos == 1-based line


# ---------------------------------------------------------------- CLI

def _standalone(args) -> int:
    if args.mathml is not None:
        xml = args.mathml
    elif args.input:
        xml = Path(args.input).read_text(encoding="utf-8", errors="replace")
    else:
        xml = sys.stdin.read()
    if "<math" not in html.unescape(xml).lower():
        print("error: input contains no <math> element", file=sys.stderr)
        return 2
    latex, display, _backend = convert_mathml(xml)
    print(render(latex, display, args.delimiter))
    return 0


def _markdown_fix(args) -> int:
    path = Path(args.markdown)
    text = path.read_text(encoding="utf-8", errors="replace")
    offsets = line_offsets(text)
    total_lines = len(offsets) - 2
    l1, l2 = parse_lines(args.lines, total_lines)

    pairs = []  # (block, result)
    for block in find_blocks(text):
        ln = line_of(offsets, block["start"])
        if not (l1 <= ln <= l2):
            continue
        try:
            latex, display, backend = convert_mathml(block["xml"])
            rendered = render(latex, display, args.delimiter)
            result = {
                "line": ln,
                "backend": backend,
                "status": "converted",
                "is_display": display,
                "input_preview": block["raw"][:80].replace("\n", " "),
                "output": rendered,
            }
        except RuntimeError as exc:
            result = {
                "line": ln,
                "backend": "",
                "status": "unconverted",
                "is_display": block["is_display"],
                "input_preview": block["raw"][:80].replace("\n", " "),
                "output": block["raw"],
                "error": str(exc),
            }
        pairs.append((block, result))

    new_text = text
    for block, result in sorted(pairs, key=lambda pr: pr[0]["start"], reverse=True):
        new_text = new_text[:block["start"]] + result["output"] + new_text[block["end"]:]

    if args.in_place:
        backup = path.with_suffix(path.suffix + ".mathml-bak")
        shutil.copy2(path, backup)
        path.write_text(new_text, encoding="utf-8")
        print(f"wrote {path} ({len(pairs)} blocks); backup at {backup}")
    elif args.output:
        Path(args.output).write_text(new_text, encoding="utf-8")
        print(f"wrote {args.output} ({len(pairs)} blocks)")
    else:
        for _, result in pairs:
            tag = "DISP" if result["is_display"] else "INLN"
            print(f"L{result['line']:>6} [{tag}] {result['status']:<10} {result['output']}")
            if result["status"] == "unconverted":
                print(f"          kept ({result['error']}): {result['input_preview']}")

    if args.json_report:
        report = {
            "file": str(path),
            "lines": [l1, l2],
            "delimiter": args.delimiter,
            "converted": sum(1 for _, r in pairs if r["status"] == "converted"),
            "unconverted": sum(1 for _, r in pairs if r["status"] != "converted"),
            "blocks": [r for _, r in pairs],
        }
        Path(args.json_report).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"report: {args.json_report}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert MathML to LaTeX (standalone or in-place inside a Markdown line range).",
    )
    p.add_argument("--mathml", help="A single <math>...</math> string to convert.")
    p.add_argument("-i", "--input", dest="input", help="A file containing MathML to convert.")
    p.add_argument("--markdown", dest="markdown", help="Markdown file whose MathML blocks to convert.")
    p.add_argument("--lines", help="Line range for --markdown: 'L' or 'L1:L2' (1-based inclusive).")
    p.add_argument("--delimiter", choices=DELIMITERS, default="dollar",
                   help="Output delimiter style (default: dollar -> $..$ / $$..$$).")
    p.add_argument("-o", "--output", dest="output", help="Write the corrected Markdown to a separate file.")
    p.add_argument("--in-place", action="store_true",
                   help="Rewrite the Markdown file in place (a .mathml-bak backup is kept).")
    p.add_argument("-j", "--json-report", dest="json_report", help="Write a per-block JSON audit report.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.markdown:
        return _markdown_fix(args)
    return _standalone(args)


if __name__ == "__main__":
    sys.exit(main())
