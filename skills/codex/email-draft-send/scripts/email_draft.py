#!/usr/bin/env python3
"""Shared parser for .mail.txt draft files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REQUIRED_HEADERS = ("To", "Subject")
OPTIONAL_HEADERS = ("Cc", "Bcc", "Attachments")
ALL_HEADERS = REQUIRED_HEADERS + OPTIONAL_HEADERS


@dataclass
class EmailDraft:
    path: Path
    to: list[str]
    cc: list[str]
    bcc: list[str]
    subject: str
    attachments: list[Path]
    body: str


def _split_csv(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_draft(path: str | Path) -> EmailDraft:
    draft_path = Path(path).expanduser().resolve()
    text = draft_path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")

    if "\n---\n" not in text and not text.startswith("---\n"):
        raise ValueError("Missing body separator line '---'.")

    header_block, body = text.split("\n---\n", 1) if "\n---\n" in text else ("", text[4:])
    header_lines = [line.rstrip("\n") for line in header_block.splitlines() if line.strip()]
    parsed: dict[str, str] = {}

    for line in header_lines:
        if ":" not in line:
            raise ValueError(f"Invalid header line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in ALL_HEADERS:
            raise ValueError(f"Unknown header: {key!r}")
        if key in parsed:
            raise ValueError(f"Duplicate header: {key!r}")
        parsed[key] = value.strip()

    missing = [key for key in REQUIRED_HEADERS if not parsed.get(key)]
    if missing:
        raise ValueError(f"Missing required header(s): {', '.join(missing)}")

    attachments = [Path(item).expanduser() for item in _split_csv(parsed.get("Attachments", ""))]
    body = body.rstrip("\n")
    if not body.strip():
        raise ValueError("Email body is empty.")

    return EmailDraft(
        path=draft_path,
        to=_split_csv(parsed["To"]),
        cc=_split_csv(parsed.get("Cc", "")),
        bcc=_split_csv(parsed.get("Bcc", "")),
        subject=parsed["Subject"],
        attachments=attachments,
        body=body,
    )
