#!/usr/bin/env python3
"""Open one or more .mail.txt drafts in Apple Mail without auto-sending.

The default mode shows a small Tkinter queue window. The window lets the user
open the current Mail draft, mark it done and open the next draft, or skip the
current draft. A Markdown run log is written at the end.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from email_draft import EmailDraft, parse_draft


STATUS_LABELS = {
    "pending": "Pending",
    "opened": "Opened in Mail",
    "marked_done": "Marked done by user",
    "skipped": "Skipped",
    "skipped_after_open": "Skipped after opening",
    "error": "Error",
}


@dataclass
class QueueRecord:
    path: Path
    draft: EmailDraft
    status: str = "pending"
    opened_at: str = ""
    note: str = ""


def _apple_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _apple_text_expression(value: str) -> str:
    parts = value.split("\n")
    escaped = [f'"{_apple_escape(part)}"' for part in parts]
    return " & return & ".join(escaped)


def _resolve_inputs(paths: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for raw in paths:
        candidate = Path(raw).expanduser()
        if candidate.is_dir():
            resolved.extend(sorted(candidate.glob("*.mail.txt")))
        else:
            resolved.append(candidate)
    return [path.resolve() for path in resolved]


def _build_applescript(draft: EmailDraft) -> str:
    lines = [
        'tell application "Mail"',
        "activate",
        (
            'set newMessage to make new outgoing message with properties '
            f'{{visible:true, subject:\"{_apple_escape(draft.subject)}\", '
            f'content:{_apple_text_expression(draft.body)}}}'
        ),
        "tell newMessage",
    ]

    for address in draft.to:
        lines.append(
            f'make new to recipient at end of to recipients with properties {{address:\"{_apple_escape(address)}\"}}'
        )
    for address in draft.cc:
        lines.append(
            f'make new cc recipient at end of cc recipients with properties {{address:\"{_apple_escape(address)}\"}}'
        )
    for address in draft.bcc:
        lines.append(
            f'make new bcc recipient at end of bcc recipients with properties {{address:\"{_apple_escape(address)}\"}}'
        )
    for attachment in draft.attachments:
        lines.append(
            'make new attachment with properties '
            f'{{file name:(POSIX file \"{_apple_escape(str(attachment.resolve()))}\")}} '
            "at after the last paragraph"
        )

    lines.extend(["save", "end tell", "end tell"])
    return "\n".join(lines)


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _validate_queue(paths: list[str]) -> list[QueueRecord]:
    queue = _resolve_inputs(paths)
    if not queue:
        raise ValueError("No draft files found.")

    records: list[QueueRecord] = []
    for draft_path in queue:
        draft = parse_draft(draft_path)
        for attachment in draft.attachments:
            if not attachment.exists():
                raise ValueError(f"Missing attachment: {attachment}")
        records.append(QueueRecord(path=draft_path, draft=draft))
    return records


def _open_draft_in_mail(draft: EmailDraft) -> None:
    script = _build_applescript(draft)
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "AppleScript command failed."
        raise RuntimeError(stderr)


def _readme_default_path(records: list[QueueRecord], explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    parents = {record.path.parent for record in records}
    if len(parents) == 1:
        return next(iter(parents)) / "README.sent-emails.md"
    return Path.cwd().resolve() / "README.sent-emails.md"


def _md_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def _draft_recipients(draft: EmailDraft) -> str:
    return ", ".join(draft.to)


def _write_readme(records: Iterable[QueueRecord], readme_path: Path) -> Path:
    rows = list(records)
    readme_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Email Manual Send Log",
        "",
        f"Generated: {_now()}",
        "",
        "Important: this script only opened and saved Apple Mail drafts. It never clicked Send. Status values reflect what the user marked in the queue window or terminal prompt.",
        "",
        "| Status | To | Subject | Opened At | Draft File | Note |",
        "|---|---|---|---|---|---|",
    ]

    for record in rows:
        status = STATUS_LABELS.get(record.status, record.status)
        lines.append(
            "| "
            + " | ".join(
                [
                    _md_cell(status),
                    _md_cell(_draft_recipients(record.draft)),
                    _md_cell(record.draft.subject),
                    _md_cell(record.opened_at or ""),
                    _md_cell(str(record.path)),
                    _md_cell(record.note),
                ]
            )
            + " |"
        )

    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return readme_path


def _print_queue(records: list[QueueRecord], readme_path: Path) -> None:
    print(f"Queue: {len(records)} draft(s)")
    print(f"README log: {readme_path}")
    for index, record in enumerate(records, start=1):
        print(f"[{index}/{len(records)}] {record.path.name} -> {_draft_recipients(record.draft)}")


def _run_terminal(records: list[QueueRecord], readme_path: Path) -> int:
    print("Terminal mode. This will create visible Apple Mail drafts only; it will not send.")
    print(f"README log will be written to: {readme_path}")

    for index, record in enumerate(records, start=1):
        while True:
            action = input(
                f"[{index}/{len(records)}] {record.path.name} -> {_draft_recipients(record.draft)} "
                "[o]pen, [s]kip, [q]uit: "
            ).strip().lower()
            if action in {"", "o", "open"}:
                try:
                    _open_draft_in_mail(record.draft)
                except Exception as exc:
                    record.status = "error"
                    record.note = str(exc)
                    print(f"[ERROR] {exc}", file=sys.stderr)
                    _write_readme(records, readme_path)
                    return 1
                record.status = "opened"
                record.opened_at = _now()
                input("Send or close the Mail draft manually, then press Enter to mark done and continue...")
                record.status = "marked_done"
                break
            if action in {"s", "skip"}:
                record.status = "skipped_after_open" if record.status == "opened" else "skipped"
                break
            if action in {"q", "quit"}:
                _write_readme(records, readme_path)
                print(f"Wrote README log: {readme_path}")
                return 0
            print("Choose o, s, or q.")

    _write_readme(records, readme_path)
    print(f"Wrote README log: {readme_path}")
    return 0


def _run_gui(records: list[QueueRecord], readme_path: Path) -> int:
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception as exc:
        print(f"[WARN] Tkinter GUI unavailable: {exc}", file=sys.stderr)
        return _run_terminal(records, readme_path)

    class DraftQueueApp:
        def __init__(self) -> None:
            self.root = tk.Tk()
            self.root.title("Email Draft Queue")
            self.index = 0

            self.summary_var = tk.StringVar()
            self.current_var = tk.StringVar()
            self.readme_var = tk.StringVar(value=f"Log: {readme_path}")

            frame = tk.Frame(self.root, padx=12, pady=12)
            frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(frame, textvariable=self.summary_var, anchor="w").pack(fill=tk.X)
            tk.Label(frame, textvariable=self.current_var, anchor="w").pack(fill=tk.X, pady=(4, 8))

            list_frame = tk.Frame(frame)
            list_frame.pack(fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
            self.listbox = tk.Listbox(list_frame, height=min(12, max(5, len(records))), width=110)
            self.listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=self.listbox.yview)
            self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            button_frame = tk.Frame(frame)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            self.open_button = tk.Button(button_frame, text="Open current in Mail", command=self.open_current)
            self.done_button = tk.Button(button_frame, text="Mark done and open next", command=self.mark_done_open_next)
            self.skip_button = tk.Button(button_frame, text="Skip current", command=self.skip_current)
            self.finish_button = tk.Button(button_frame, text="Finish and write README", command=self.finish)
            for button in [self.open_button, self.done_button, self.skip_button, self.finish_button]:
                button.pack(side=tk.LEFT, padx=(0, 8))

            tk.Label(frame, textvariable=self.readme_var, anchor="w").pack(fill=tk.X, pady=(10, 0))
            self.root.protocol("WM_DELETE_WINDOW", self.finish)
            self.refresh()

        def current(self) -> QueueRecord | None:
            if 0 <= self.index < len(records):
                return records[self.index]
            return None

        def first_pending_from(self, start: int) -> bool:
            for idx in range(start, len(records)):
                if records[idx].status == "pending":
                    self.index = idx
                    return True
            self.index = len(records)
            return False

        def row_label(self, index: int, record: QueueRecord) -> str:
            marker = ">" if index == self.index else " "
            status = STATUS_LABELS.get(record.status, record.status)
            return f"{marker} {index + 1:02d}. {status}: {_draft_recipients(record.draft)} — {record.draft.subject}"

        def refresh(self) -> None:
            completed = sum(1 for record in records if record.status != "pending")
            self.summary_var.set(f"{completed}/{len(records)} handled. Script opens Mail drafts only; you send manually.")

            self.listbox.delete(0, tk.END)
            for idx, record in enumerate(records):
                self.listbox.insert(tk.END, self.row_label(idx, record))

            current = self.current()
            if current is None:
                self.current_var.set("Current: none. Finish to write the README log.")
                self.open_button.config(state=tk.DISABLED)
                self.done_button.config(state=tk.DISABLED)
                self.skip_button.config(state=tk.DISABLED)
            else:
                self.current_var.set(f"Current: {_draft_recipients(current.draft)}")
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(self.index)
                self.listbox.see(self.index)
                self.open_button.config(state=tk.NORMAL if current.status == "pending" else tk.DISABLED)
                self.done_button.config(state=tk.NORMAL if current.status == "opened" else tk.DISABLED)
                self.skip_button.config(state=tk.NORMAL if current.status in {"pending", "opened"} else tk.DISABLED)

        def open_current(self) -> None:
            current = self.current()
            if current is None:
                return
            try:
                _open_draft_in_mail(current.draft)
            except Exception as exc:
                current.status = "error"
                current.note = str(exc)
                self.refresh()
                messagebox.showerror("Apple Mail Error", str(exc))
                return
            current.status = "opened"
            current.opened_at = _now()
            self.refresh()

        def mark_done_open_next(self) -> None:
            current = self.current()
            if current is None:
                return
            current.status = "marked_done"
            if self.first_pending_from(self.index + 1):
                self.refresh()
                self.open_current()
            else:
                self.refresh()

        def skip_current(self) -> None:
            current = self.current()
            if current is None:
                return
            current.status = "skipped_after_open" if current.status == "opened" else "skipped"
            self.first_pending_from(self.index + 1)
            self.refresh()

        def finish(self) -> None:
            _write_readme(records, readme_path)
            messagebox.showinfo("Email Draft Queue", f"Wrote README log:\n{readme_path}")
            self.root.destroy()

        def run(self) -> None:
            self.root.mainloop()

    try:
        DraftQueueApp().run()
    except Exception as exc:
        print(f"[WARN] GUI failed: {exc}", file=sys.stderr)
        return _run_terminal(records, readme_path)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open .mail.txt drafts in Apple Mail one at a time without auto-sending."
    )
    parser.add_argument("paths", nargs="+", help="Draft files or directories containing *.mail.txt drafts")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print queue without opening Mail")
    parser.add_argument("--terminal", action="store_true", help="Use terminal prompts instead of the Tkinter queue window")
    parser.add_argument("--readme", help="Path for the Markdown send log; defaults to README.sent-emails.md beside the drafts")
    args = parser.parse_args()

    try:
        records = _validate_queue(args.paths)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    readme_path = _readme_default_path(records, args.readme)
    if args.dry_run:
        _print_queue(records, readme_path)
        return 0

    if args.terminal:
        return _run_terminal(records, readme_path)

    return _run_gui(records, readme_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
