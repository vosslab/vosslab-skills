#!/usr/bin/env python3

"""
Report the last-change date, version hash, and age in days of a screenshot.

Git is the source of truth: the commit that last touched the file carries both
its date and its short hash. A file with no commit yet is reported as
uncommitted.
"""

# Standard Library
import os
import datetime
import argparse
import subprocess


#============================================
def parse_args() -> argparse.Namespace:
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(
		description="Report a screenshot's last-change date, version, and age in days.",
	)
	parser.add_argument(
		'-i', '--input', dest='input_file', required=True,
		help="Path to the screenshot file to inspect",
	)
	args = parser.parse_args()
	return args


#============================================
def git_last_commit(file_path: str) -> tuple[str, str] | None:
	"""
	Return (commit_date, short_hash) for the last commit touching file_path.

	commit_date is an ISO YYYY-MM-DD string. Return None when the file has no
	commit yet (untracked or staged-only).
	"""
	# run git from the file's own directory so the correct repo is used
	work_dir = os.path.dirname(os.path.abspath(file_path)) or '.'
	command = ['git', '-C', work_dir, 'log', '-1', '--format=%cs%n%h', '--', file_path]
	result = subprocess.run(command, capture_output=True, text=True)
	output = result.stdout.strip()
	if not output:
		return None
	parts = output.splitlines()
	commit_date = parts[0].strip()
	short_hash = parts[1].strip()
	return (commit_date, short_hash)


#============================================
def age_in_days(commit_date: str) -> int:
	"""
	Return the number of whole days between commit_date and today.
	"""
	commit_day = datetime.date.fromisoformat(commit_date)
	today = datetime.date.today()
	delta = today - commit_day
	return delta.days


#============================================
def main() -> None:
	"""
	Inspect one screenshot and print its date, version, and age.
	"""
	args = parse_args()
	last_commit = git_last_commit(args.input_file)
	if last_commit is None:
		print(f"{args.input_file}: uncommitted (no version yet)")
		return
	commit_date, short_hash = last_commit
	age = age_in_days(commit_date)
	# assemble the report line first, then print it
	report = f"{args.input_file}: date={commit_date} version={short_hash} age={age} days"
	print(report)


#============================================
if __name__ == '__main__':
	main()
