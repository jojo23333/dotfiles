#!/usr/bin/env python3
"""Validate a .mail.txt draft file and print a short summary."""

from __future__ import annotations

import argparse
import sys

from email_draft import parse_draft


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a .mail.txt email draft file.")
    parser.add_argument("path", help="Path to the .mail.txt file")
    args = parser.parse_args()

    try:
        draft = parse_draft(args.path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    print(f"[OK] {draft.path}")
    print(f"To: {', '.join(draft.to)}")
    print(f"Cc: {', '.join(draft.cc) or '(none)'}")
    print(f"Bcc: {', '.join(draft.bcc) or '(none)'}")
    print(f"Subject: {draft.subject}")
    print(f"Attachments: {len(draft.attachments)}")
    print(f"Body lines: {len(draft.body.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
