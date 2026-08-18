"""Behavior checks for the Markdown duplication and residue audit tools."""

import importlib


DUP = importlib.import_module("audit_markdown_duplication")
RESIDUE = importlib.import_module("audit_markdown_residue")


def test_line_duplicates_detects_genuine_stutter() -> None:
	"""A content-word phrase repeated adjacently is a duplication, not an idiom."""
	assert DUP.line_duplicates(["very", "difficult", "very", "difficult"]) == [(2, "very difficult")]


def test_content_segments_split_at_connectors() -> None:
	"""An X-to-X phrase splits at the connector, so no false adjacent duplicate."""
	assert DUP.content_segments("research group to research group") == [
		["research", "group"],
		["research", "group"],
	]


def test_content_segments_drop_equation_speech() -> None:
	"""Single-letter math tokens are dropped and short tokens never register."""
	segments = DUP.content_segments("big R big R and mu m mu m")
	assert all(DUP.line_duplicates(segment) == [] for segment in segments)


def test_content_segments_drop_publisher_imprint() -> None:
	"""Title-page imprints such as a repeated press line do not report as stutter."""
	segments = DUP.content_segments("Princeton University Press Princeton University Press")
	assert all(DUP.line_duplicates(segment) == [] for segment in segments)


def test_dedupe_line_collapses_one_duplicate() -> None:
	"""One adjacent duplicate collapses to the first occurrence without a double space."""
	deduped, removed = DUP.dedupe_line("very difficult very difficult to read")
	assert removed == 1
	assert deduped == "very difficult to read"


def test_dedupe_line_preserves_idiom_and_case() -> None:
	"""Idioms stay untouched and the first occurrence keeps its capitalization."""
	deduped, removed = DUP.dedupe_line("One by one, Very difficult Very difficult to read")
	assert removed == 1
	assert deduped == "One by one, Very difficult to read"


def test_audit_skips_code_and_table_content() -> None:
	"""Duplication inside fenced code and pipe tables is not flagged."""
	text = "# Title\n\n```\ntoken token token token\n```\n\n| left | left |\n"
	result = DUP.audit_markdown(text)
	assert result.status == "CLEAN"


def test_glossary_definition_label_is_not_stutter() -> None:
	"""A bold definition term restated at the start of its entry is not duplication."""
	text = "- **Network monitoring:** Network monitoring takes advantage of the architecture\n"
	assert DUP.audit_markdown(text).status == "CLEAN"


def test_dedupe_preserves_link_and_offsets() -> None:
	"""Links stay intact and dedup offsets remain aligned around them."""
	line = "See [this guide](http://example.com) then very difficult very difficult to read"
	deduped, removed = DUP.dedupe_line(line)
	assert removed == 1
	assert "[this guide](http://example.com)" in deduped
	assert "very difficult very difficult" not in deduped


def test_audit_counts_bigram_trigram_and_fourgram() -> None:
	"""Each n-gram size reports its own count."""
	text = "very difficult very difficult\n" \
		"double bonds separated double bonds separated\n" \
		"primer extension method locate primer extension method locate\n"
	result = DUP.audit_markdown(text)
	assert result.bigram_dup == 1
	assert result.trigram_dup == 1
	assert result.fourgram_dup == 1


def test_count_residue_detects_garbled_classes() -> None:
	"""Replacement chars, setext garbage, and dot leaders are each counted."""
	text = "clean\ufffd line\n\n=====\n\n.... .... .... .... .... .... ....\n"
	counts = RESIDUE.count_residue(text)
	assert counts.fffd == 1
	assert counts.setext_garbage_lines == 1
	assert counts.dot_leader_runs == 1


def test_strip_markdown_preserves_length_and_offsets() -> None:
	"""Markdown blanking keeps string length and word offsets, so dedup stays aligned."""
	line = "See [this guide](http://example.com) and **bold** very difficult very difficult"
	stripped = DUP.strip_markdown(line)
	assert len(stripped) == len(line)
	assert stripped.find("very") == line.find("very")
