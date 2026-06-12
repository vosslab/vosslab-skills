#!/usr/bin/env python3
"""
Post a local PG/PGML file to the renderer API and report lint findings,
the full JSON response, or rendered HTML.
"""

# Standard Library
import json
import time
import random
import argparse
import urllib.request
import html
import re

BASE_URL = "http://localhost:3000"
TEMPLATE_CHOICES = ("static", "default", "debug")

JWT_PATTERN = re.compile(
	r"(?<![A-Za-z0-9_-])"
	r"([A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})"
	r"(?![A-Za-z0-9_-])"
)
JWT_INPUT_PATTERN = re.compile(
	r"<input\b[^>]*\bname=[\"'][A-Za-z]+JWT[\"'][^>]*\bvalue=[\"'][^\"']+[\"'][^>]*>",
	re.IGNORECASE,
)

# Literal exact-match keys to drop from JSON output. Exact match only: a future
# server-side field like "hasJWT" or "jwtExpiry" must not silently disappear.
# "JWT" is the observed wrapper dict ({answer, problem, session}) in the
# renderer response as of 2026-04-22; the 2-part "problem" token inside it is
# what defeats the three-dot regex and bloats --json. The other three are
# defensive coverage for hypothetical flat keys seen in lib/RenderApp.
JWT_KEYS_TO_DROP = {"JWT", "sessionJWT", "answerJWT", "problemJWT"}


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
		"-s",
		"--seed",
		dest="problem_seed",
		type=int,
		default=None,
		help="Problem seed (default: random).",
	)
	parser.add_argument(
		"-t",
		"--template",
		dest="template",
		choices=TEMPLATE_CHOICES,
		default="debug",
		help="Renderer template id (default: debug). Choices: static, default, debug.",
	)
	# Output mode group: default (no flag) = lint report.
	mode_group = parser.add_mutually_exclusive_group()
	mode_group.add_argument(
		"--json",
		dest="output_mode",
		action="store_const",
		const="json",
		help="Print full JSON response, pretty-printed, JWT-redacted.",
	)
	mode_group.add_argument(
		"--html",
		dest="output_mode",
		action="store_const",
		const="html",
		help="Print rendered HTML extracted from the JSON response, JWT-redacted.",
	)
	parser.set_defaults(output_mode="lint")
	# --no-html: drop the renderedHTML key from JSON output (only meaningful
	# with --json; errors at parse time if combined with --html).
	parser.add_argument(
		"--no-html",
		dest="no_html",
		action="store_true",
		help="Omit renderedHTML from --json output (only valid with --json).",
	)
	args = parser.parse_args()
	# Enforce --no-html only applies to --json mode.
	if args.no_html and args.output_mode != "json":
		parser.error("--no-html requires --json")
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
def build_payload(source_text: str, problem_seed: int, template: str) -> dict:
	"""
	Build the JSON payload for the render request.
	"""
	payload = {
		"problemSource": source_text,
		"problemSeed": problem_seed,
		"outputFormat": template,
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
def strip_jwt_tree(value: object) -> object:
	"""
	Walk a decoded JSON tree and delete any dict key in JWT_KEYS_TO_DROP.
	Exact-match, case-sensitive. Recurses into remaining dicts and lists.

	Observed shape in the renderer response on 2026-04-22: top-level key
	"JWT" is a dict {answer, problem, session}; "problem" is a 2-part token
	that the three-dot JWT_PATTERN does not match, which is the reason
	--json output carries ~2 KB of base64 despite the existing redaction.
	Dropping the wrapper outright removes all three tokens at once.
	"""
	if isinstance(value, dict):
		cleaned = {}
		for key, item in value.items():
			if key in JWT_KEYS_TO_DROP:
				continue
			cleaned[key] = strip_jwt_tree(item)
		return cleaned
	if isinstance(value, list):
		return [strip_jwt_tree(item) for item in value]
	return value


#============================================
def redact_tree(value: object) -> object:
	"""
	Walk a decoded JSON tree and apply redact_jwt to every string value.
	Non-string values (numbers, None, bools, nested containers) pass through.
	"""
	if isinstance(value, str):
		return redact_jwt(value)
	if isinstance(value, dict):
		return {key: redact_tree(item) for key, item in value.items()}
	if isinstance(value, list):
		return [redact_tree(item) for item in value]
	return value


#============================================
def request_render(base_url: str, payload: dict) -> dict:
	"""
	Post to /render-api and return the decoded JSON response.
	"""
	# _format must be a query param; the renderer ignores it in the JSON body.
	url = f"{base_url}/render-api?_format=json"
	body = json.dumps(payload).encode("utf-8")
	headers = {"Content-Type": "application/json"}

	# Throttle API calls per repo guidance.
	time.sleep(random.random())

	# Guard against file:// or other unexpected schemes
	if not (url.startswith("https://") or url.startswith("http://")):
		raise ValueError(f"Only HTTP/HTTPS URLs are allowed, got: {url}")
	request = urllib.request.Request(url, data=body, headers=headers, method="POST")
	with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310
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
def normalize_messages(value: object) -> list[str]:
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
def print_json_response(response: dict, drop_html: bool = False) -> None:
	"""
	Print the full JSON response, JWT-stripped, pretty-printed.

	strip_jwt_tree drops the known JWT-bearing keys outright. redact_tree
	then walks remaining strings as a belt-and-suspenders backstop (catches
	any inline JWT inside other fields and strips `<input name="...JWT" ...>`
	tags embedded inside the renderedHTML string).
	"""
	stripped = strip_jwt_tree(response)
	if drop_html:
		stripped.pop("renderedHTML", None)
	redacted = redact_tree(stripped)
	serialized = json.dumps(redacted, indent=2, sort_keys=True)
	print(serialized)


#============================================
def main() -> None:
	"""
	Run the lint or render workflow.
	"""
	args = parse_args()
	source_text = read_source(args.input_file)
	seed_value = args.problem_seed
	if seed_value is None:
		seed_value = random.randint(1, 999999)
		# Only print the seed notice in lint mode so --json and --html
		# produce clean, parseable stdout.
		if args.output_mode == "lint":
			print(f"Using random seed: {seed_value}")
	payload = build_payload(source_text, seed_value, args.template)
	response = request_render(BASE_URL, payload)

	if args.output_mode == "html":
		print_rendered_html(response)
		return
	if args.output_mode == "json":
		print_json_response(response, drop_html=args.no_html)
		return

	messages = collect_lint_messages(response)
	print_lint_report(messages)
	if is_error_flagged(response):
		raise RuntimeError("renderer reported errors")


if __name__ == "__main__":
	main()
