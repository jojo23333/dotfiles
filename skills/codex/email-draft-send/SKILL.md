---
name: email-draft-send
description: Save email drafts as deterministic plain-text files and open them in Apple Mail for manual review and sending on macOS. Use when Codex needs to draft outreach emails, cold emails, follow-ups, or batch email queues; store them in a reusable text format; validate the drafts before sending; or open one or more drafts in Mail without auto-sending.
---

# Email Draft Send

## Overview

Use this skill to keep email work reproducible and safe. Draft emails into `.mail.txt` files first, then open them in Apple Mail one at a time for the user to review and send manually.

## Workflow

1. Decide whether the user wants to create drafts, send existing drafts, or both.
2. For draft creation, write one `.mail.txt` file per message in a draft directory.
3. Validate the draft file with `scripts/validate_email_draft.py`.
4. For manual sending, run `scripts/open_mail_drafts.py` with a file path or draft directory. This opens a small queue window that controls Apple Mail drafts while the user sends messages manually.

## Draft Creation

Default to a draft directory named `email-drafts/` under the current workspace unless the user specifies another location.

Use sortable ASCII filenames:

```text
YYYY-MM-DD-recipient-slug-topic.mail.txt
```

Examples:

```text
2026-04-02-carolina-tropini-customer-interview.mail.txt
2026-04-02-megan-levings-follow-up.mail.txt
```

Create one file per recipient unless the user explicitly wants a shared multi-recipient email.

Use the exact file structure documented in [format.md](./references/format.md). Keep the header block compact and place the body after the `---` separator.

## Validation

Validate every draft file before opening Mail:

```bash
python3 /Users/jojo/.codex/skills/email-draft-send/scripts/validate_email_draft.py path/to/draft.mail.txt
```

If validation fails, fix the file rather than guessing during send.

## Manual Sending In Mail

Open drafts only after validation. By default, the sender opens a small queue window with:

- current draft and queue list
- `Open current in Mail`
- `Mark done and open next`
- `Skip current`
- `Finish and write README`

```bash
python3 /Users/jojo/.codex/skills/email-draft-send/scripts/open_mail_drafts.py path/to/draft.mail.txt
python3 /Users/jojo/.codex/skills/email-draft-send/scripts/open_mail_drafts.py path/to/email-drafts
```

Behavior:

- Open a visible Apple Mail compose window for each draft
- Fill `To`, `Cc`, `Bcc`, `Subject`, and body
- Attach files if listed in the draft and present on disk
- Save the message to Drafts
- Let the user open, skip, or advance through drafts from the queue window
- Write a Markdown run log at `README.sent-emails.md` beside the draft files by default

Do not auto-send. The user sends each message manually in Mail. The README log records what was opened, skipped, or marked done; it cannot prove that a user clicked Send inside Mail.

The first GUI choice is Python `tkinter`. If unavailable, the script falls back to macOS AppleScript dialogs so it still works without extra Python GUI dependencies. For terminal-only operation, pass `--terminal`. Opening Mail requires GUI access.

## Format Rules

The draft format is intentionally strict so it is easy to parse and review.

- Required headers: `To`, `Subject`
- Optional headers: `Cc`, `Bcc`, `Attachments`
- Use comma-separated email addresses inside a header when needed
- Use absolute attachment paths when possible
- Put `---` on its own line to start the body
- Keep body text exactly as the user should send it

Read [format.md](./references/format.md) when writing or fixing draft files.

## Operational Rules

- Prefer editing the text draft first, not the Mail compose window
- Preserve the user’s wording when revising an existing draft unless asked to improve it
- Ask only when key message intent is unclear; otherwise make reasonable assumptions and draft
- Keep the skill macOS-only because it depends on Apple Mail through AppleScript
- Never claim an email was sent; at most state that a Mail compose window or saved draft was opened
