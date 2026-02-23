#!/usr/bin/env python3
"""
Post a local PG/PGML file to the renderer API and report lint findings or HTML.
"""

# Standard Library
import json
import time
import random
import argparse
import urllib.request
import html
import re

JWT_PATTERN = re.compile(
	r"(?<![A-Za-z0-9_-])"
	r"([A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})"
	r"(?![A-Za-z0-9_-])"
)
JWT_INPUT_PATTERN = re.compile(
	r"<input\b[^>]*\bname=[\"'][A-Za-z]+JWT[\"'][^>]*\bvalue=[\"'][^\"']+[\"'][^>]*>",
	re.IGNORECASE,
)


#============================================
def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Lint a PG/PGML file via the renderer API."
	)
	parser.add_argument(
		"-i",
		"--input",
		dest="input_file",
		required=True,
		help="Local PG/PGML file to send as problemSource.",
	)
	parser.add_argument(
		"-b",
		"--base-url",
		dest="base_url",
		default="http://localhost:3000",
		help="Renderer base URL (default: http://localhost:3000).",
	)
	parser.add_argument(
		"-s",
		"--seed",
		dest="problem_seed",
		type=int,
		default=None,
		help="Problem seed (default: random).",
	)
	parser.add_argument(
		"-o",
		"--output-format",
		dest="output_format",
		default="classic",
		help="Output format template id (default: classic).",
	)
	parser.add_argument(
		"-r",
		"--render",
		dest="render_html",
		action="store_true",
		help="Print rendered HTML instead of lint findings.",
	)
	parser.add_argument(
		"-n",
		"--no-render",
		dest="render_html",
		action="store_false",
		help="Print lint findings instead of rendered HTML.",
	)
	parser.set_defaults(render_html=False)
	args = parser.parse_args()
	return args


#============================================
def read_source(path: str) -> str:
	"""
	Read the local PG/PGML source file.
	"""
	with open(path, "r", encoding="utf-8") as handle:
		content = handle.read()
	return content


#============================================
def build_payload(source_text: str, problem_seed: int, output_format: str) -> dict:
	"""
	Build the JSON payload for the render request.
	"""
	payload = {
		"problemSource": source_text,
		"problemSeed": problem_seed,
		"outputFormat": output_format,
	}
	return payload


#============================================
def redact_jwt(text: str) -> str:
	"""
	Redact JWT-like strings from output to keep logs readable.
	"""
	if not text:
		return text
	redacted = JWT_INPUT_PATTERN.sub("", text)
	redacted = JWT_PATTERN.sub("<REDACTED_JWT>", redacted)
	return redacted


#============================================
def request_render(base_url: str, payload: dict) -> dict:
	"""
	Post to /render-api and return the decoded JSON response.
	"""
	url = f"{base_url}/render-api"
	body = json.dumps(payload).encode("utf-8")
	headers = {"Content-Type": "application/json"}

	# Throttle API calls per repo guidance.
	time.sleep(random.random())

	request = urllib.request.Request(url, data=body, headers=headers, method="POST")
	with urllib.request.urlopen(request, timeout=60) as response:
		raw_body = response.read().decode("utf-8")
		try:
			json_body = json.loads(raw_body)
			return json_body
		except json.JSONDecodeError:
			return {
				"renderedHTML": raw_body,
				"warnings": ["renderer returned non-JSON response; parsing HTML only"],
			}


#============================================
def normalize_messages(value) -> list[str]:
	"""
	Normalize response fields into a list of strings.
	"""
	if value is None:
		return []
	if isinstance(value, list):
		return [str(item) for item in value if item is not None]
	return [str(value)]


#============================================
def collect_lint_messages(response: dict) -> list[str]:
	"""
	Collect lint messages from the layered response fields.
	"""
	messages: list[str] = []
	messages += normalize_messages(response.get("errors"))
	messages += normalize_messages(response.get("warnings"))
	messages += normalize_messages(response.get("error"))
	messages += normalize_messages(response.get("warning"))
	messages += normalize_messages(response.get("message"))

	debug = response.get("debug", {}) if isinstance(response.get("debug"), dict) else {}
	messages += normalize_messages(debug.get("pg_warn"))
	messages += normalize_messages(debug.get("internal"))
	messages += normalize_messages(debug.get("debug"))

	if messages:
		return messages

	rendered_html = response.get("renderedHTML", "")
	if not rendered_html:
		return messages
	error_match = re.search(
		r'id=[\'"]error-block[\'"][^>]*text="([^"]+)"',
		rendered_html,
		flags=re.IGNORECASE,
	)
	if error_match:
		messages.append(f"renderer error page: {html.unescape(error_match.group(1))}")

	warning_terms = ("Translator errors", "Warning messages")
	for term in warning_terms:
		if term in rendered_html:
			messages.append(f"renderedHTML contains '{term}' section")

	return messages


#============================================
def is_error_flagged(response: dict) -> bool:
	"""
	Check whether the response flags an error.
	"""
	flags = response.get("flags", {}) if isinstance(response.get("flags"), dict) else {}
	error_flag = bool(flags.get("error_flag"))
	if error_flag:
		return True
	if response.get("errors"):
		return True
	if response.get("error"):
		return True
	return False


#============================================
def print_lint_report(messages: list[str]) -> None:
	"""
	Print a lint report to stdout.
	"""
	if not messages:
		print("No lint messages detected.")
		return
	print("Lint messages:")
	for message in messages:
		print(f"- {redact_jwt(message)}")


#============================================
def print_rendered_html(response: dict) -> None:
	"""
	Print rendered HTML to stdout.
	"""
	rendered_html = response.get("renderedHTML", "")
	if not rendered_html:
		raise RuntimeError("renderedHTML missing from response")
	print(redact_jwt(rendered_html))


#============================================
def main() -> None:
	"""
	Run the lint or render workflow.
	"""
	args = parse_args()
	base_url = args.base_url.rstrip("/")
	source_text = read_source(args.input_file)
	seed_value = args.problem_seed
	if seed_value is None:
		seed_value = random.randint(1, 999999)
		print(f"Using random seed: {seed_value}")
	payload = build_payload(source_text, seed_value, args.output_format)
	response = request_render(base_url, payload)

	if args.render_html:
		print_rendered_html(response)
		return

	messages = collect_lint_messages(response)
	print_lint_report(messages)
	if is_error_flagged(response):
		raise RuntimeError("renderer reported errors")


if __name__ == "__main__":
	main()
