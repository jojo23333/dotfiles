#!/usr/bin/env python3
"""Serve a local quiz UI for one system-viva session.

The server reads a session JSON file, renders the questions in a small local
web app, writes the human submission back into the same file, then exits.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Event


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>System Viva</title>
  <style>
    :root {{
      --bg: #f4f1ea;
      --panel: #fffdf8;
      --ink: #14213d;
      --muted: #5f6b7a;
      --line: #ded7ca;
      --accent: #005f73;
      --accent-2: #ca8a04;
      --good: #0f766e;
      --shadow: 0 18px 48px rgba(20, 33, 61, 0.08);
      --radius: 18px;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(202, 138, 4, 0.10), transparent 30rem),
        linear-gradient(180deg, #f8f5ef 0%, #f1ece4 100%);
    }}

    .shell {{
      max-width: 960px;
      margin: 0 auto;
      padding: 40px 20px 72px;
    }}

    .hero {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: calc(var(--radius) + 6px);
      box-shadow: var(--shadow);
      padding: 28px 30px;
      margin-bottom: 24px;
    }}

    .eyebrow {{
      margin: 0 0 8px;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.12em;
      font-size: 0.78rem;
      font-weight: 700;
    }}

    h1 {{
      margin: 0 0 10px;
      font-size: clamp(2rem, 4vw, 3.1rem);
      line-height: 1.02;
    }}

    .subtitle {{
      margin: 0;
      color: var(--muted);
      font-size: 1.02rem;
      line-height: 1.55;
      max-width: 64ch;
    }}

    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}

    .pill {{
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #faf7f1;
      padding: 8px 12px;
      color: var(--muted);
      font-size: 0.92rem;
    }}

    form {{
      display: grid;
      gap: 18px;
    }}

    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 22px;
    }}

    .card-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 12px;
    }}

    .card h2 {{
      margin: 0;
      font-size: 1.18rem;
      line-height: 1.3;
    }}

    .badge {{
      flex: 0 0 auto;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: white;
      background: var(--accent);
    }}

    .context, .note {{
      color: var(--muted);
      line-height: 1.55;
      margin: 0 0 12px;
    }}

    .why {{
      margin: 14px 0 0;
      padding: 12px 14px;
      border-left: 4px solid var(--accent-2);
      background: #f9f4e7;
      color: #5f4b16;
      border-radius: 10px;
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    fieldset {{
      border: 0;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 10px;
    }}

    label.option {{
      display: flex;
      gap: 10px;
      align-items: flex-start;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fcfbf7;
      cursor: pointer;
    }}

    textarea, select {{
      width: 100%;
      border: 1px solid #cbd2d9;
      border-radius: 12px;
      padding: 12px 14px;
      font: inherit;
      color: var(--ink);
      background: white;
    }}

    textarea {{
      min-height: 138px;
      resize: vertical;
      line-height: 1.5;
    }}

    .confidence {{
      margin-top: 14px;
      display: grid;
      gap: 6px;
    }}

    .actions {{
      position: sticky;
      bottom: 16px;
      display: flex;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
      background: rgba(255, 253, 248, 0.92);
      border: 1px solid var(--line);
      border-radius: calc(var(--radius) + 2px);
      box-shadow: var(--shadow);
      padding: 14px 16px;
      backdrop-filter: blur(14px);
    }}

    button {{
      border: 0;
      border-radius: 999px;
      background: var(--accent);
      color: white;
      font: inherit;
      font-weight: 700;
      padding: 12px 18px;
      cursor: pointer;
    }}

    button:disabled {{
      opacity: 0.55;
      cursor: not-allowed;
    }}

    #status {{
      color: var(--muted);
      min-height: 1.2rem;
    }}

    .success {{
      color: var(--good);
      font-weight: 700;
    }}

    @media (max-width: 720px) {{
      .shell {{
        padding: 22px 14px 48px;
      }}

      .hero, .card {{
        padding: 18px;
      }}

      .actions {{
        flex-direction: column;
        align-items: stretch;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <p class="eyebrow">System Viva</p>
      <h1 id="theme"></h1>
      <p class="subtitle" id="summary"></p>
      <div class="meta" id="meta"></div>
    </section>

    <form id="quiz-form"></form>

    <div class="actions">
      <div id="status">Complete the questions, then submit once.</div>
      <button id="submit-btn" type="button">Submit Answers</button>
    </div>
  </div>

  <script id="session-data" type="application/json">{session_json}</script>
  <script>
    const payload = JSON.parse(document.getElementById("session-data").textContent);
    const form = document.getElementById("quiz-form");
    const statusEl = document.getElementById("status");
    const submitBtn = document.getElementById("submit-btn");

    document.getElementById("theme").textContent = payload.theme || "Learning Session";
    document.getElementById("summary").textContent =
      payload.summary || "Answer the questions in your own words. Short, concrete reasoning is better than polished prose.";

    const meta = document.getElementById("meta");
    const questionCount = Array.isArray(payload.questions) ? payload.questions.length : 0;
    const metaBits = [
      questionCount ? String(questionCount) + " questions" : null,
      payload.session_id ? "session " + String(payload.session_id) : null,
      payload.generated_at ? "generated " + String(payload.generated_at) : null
    ].filter(Boolean);
    metaBits.forEach((bit) => {{
      const pill = document.createElement("div");
      pill.className = "pill";
      pill.textContent = bit;
      meta.appendChild(pill);
    }});

    const kindLabel = (kind) => {{
      if (kind === "mcq") return "Multiple choice";
      if (kind === "code") return "Mini coding";
      return "Open response";
    }};

    const addConfidence = (question) => {{
      const wrap = document.createElement("div");
      wrap.className = "confidence";

      const label = document.createElement("label");
      label.textContent = "Confidence";
      label.setAttribute("for", "confidence-" + String(question.id));

      const select = document.createElement("select");
      select.id = "confidence-" + String(question.id);
      select.name = "confidence-" + String(question.id);

      const options = [
        ["", "Select confidence"],
        ["1", "1 - guessing"],
        ["2", "2 - low"],
        ["3", "3 - medium"],
        ["4", "4 - high"],
        ["5", "5 - certain"]
      ];

      options.forEach(([value, text]) => {{
        const option = document.createElement("option");
        option.value = value;
        option.textContent = text;
        select.appendChild(option);
      }});

      wrap.appendChild(label);
      wrap.appendChild(select);
      return wrap;
    }};

    (payload.questions || []).forEach((question, index) => {{
      const card = document.createElement("section");
      card.className = "card";

      const head = document.createElement("div");
      head.className = "card-head";

      const titleWrap = document.createElement("div");
      const title = document.createElement("h2");
      title.textContent = String(index + 1) + ". " + String(question.prompt);
      titleWrap.appendChild(title);

      if (question.context) {{
        const context = document.createElement("p");
        context.className = "context";
        context.textContent = question.context;
        titleWrap.appendChild(context);
      }}

      const badge = document.createElement("div");
      badge.className = "badge";
      badge.textContent = kindLabel(question.kind);

      head.appendChild(titleWrap);
      head.appendChild(badge);
      card.appendChild(head);

      if (question.kind === "mcq") {{
        const fieldset = document.createElement("fieldset");
        (question.options || []).forEach((option, optionIndex) => {{
          const label = document.createElement("label");
          label.className = "option";

          const radio = document.createElement("input");
          radio.type = "radio";
          radio.name = "answer-" + String(question.id);
          radio.value = option.value || String(optionIndex);

          const text = document.createElement("span");
          text.textContent = option.label || String(option);

          label.appendChild(radio);
          label.appendChild(text);
          fieldset.appendChild(label);
        }});
        card.appendChild(fieldset);
      }} else {{
        const textarea = document.createElement("textarea");
        textarea.name = "answer-" + String(question.id);
        textarea.placeholder = question.kind === "code"
          ? "Write the smallest useful code or pseudo-code here."
          : "Answer in your own words.";
        card.appendChild(textarea);
      }}

      card.appendChild(addConfidence(question));

      if (question.why_it_matters) {{
        const why = document.createElement("div");
        why.className = "why";
        why.textContent = "Why this matters: " + String(question.why_it_matters);
        card.appendChild(why);
      }}

      form.appendChild(card);
    }});

    submitBtn.addEventListener("click", async () => {{
      submitBtn.disabled = true;
      statusEl.textContent = "Submitting answers...";

      const answers = (payload.questions || []).map((question) => {{
        const answerName = "answer-" + String(question.id);
        const confidenceName = "confidence-" + String(question.id);
        const answerField = form.querySelector('[name="' + answerName + '"]:checked')
          || form.querySelector('[name="' + answerName + '"]');
        const confidenceField = form.querySelector('[name="' + confidenceName + '"]');
        return {{
          id: question.id,
          kind: question.kind,
          answer: answerField ? answerField.value : "",
          confidence: confidenceField ? confidenceField.value : ""
        }};
      }});

      const response = await fetch("/submit", {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{ answers }})
      }});

      if (!response.ok) {{
        statusEl.textContent = "Submission failed. Keep the page open and try again.";
        submitBtn.disabled = false;
        return;
      }}

      statusEl.textContent = "Submission saved. You can close this page.";
      statusEl.className = "success";
    }});
  </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve a local System Viva quiz UI.")
    parser.add_argument("session", help="Path to session.json")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host")
    parser.add_argument("--port", type=int, default=8765, help="Bind port")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_session(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("session.json must contain an object")
    if not isinstance(data.get("questions"), list) or not data["questions"]:
        raise ValueError("session.json must contain a non-empty questions array")
    return data


def write_session(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def make_handler(session_path: Path, done: Event):
    class Handler(BaseHTTPRequestHandler):
        def _send_html(self, html_text: str) -> None:
            body = html_text.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, status: HTTPStatus, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path != "/":
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                return

            session_data = load_session(session_path)
            html_text = HTML_TEMPLATE.format(
                session_json=json.dumps(session_data).replace("</", "<\\/")
            )
            self._send_html(html_text)

        def do_POST(self) -> None:
            if self.path != "/submit":
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                return

            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)

            try:
                payload = json.loads(raw_body.decode("utf-8"))
                answers = payload["answers"]
                if not isinstance(answers, list):
                    raise ValueError
            except Exception:
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid submission"})
                return

            session_data = load_session(session_path)
            session_data["human_answers"] = answers
            session_data["submitted_at"] = utc_now()
            session_data["status"] = "submitted"
            write_session(session_path, session_data)

            self._send_json(HTTPStatus.OK, {"ok": True})
            done.set()

        def log_message(self, format: str, *args) -> None:
            return

    return Handler


def main() -> int:
    args = parse_args()
    session_path = Path(args.session).expanduser().resolve()

    if not session_path.exists():
        print(f"Session file not found: {session_path}", file=sys.stderr)
        return 1

    try:
        load_session(session_path)
    except Exception as exc:
        print(f"Invalid session file: {exc}", file=sys.stderr)
        return 1

    done = Event()
    try:
        server = ThreadingHTTPServer((args.host, args.port), make_handler(session_path, done))
    except OSError as exc:
        print(f"Could not start quiz UI on {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1
    server.timeout = 0.5
    url = f"http://{args.host}:{args.port}"

    print(f"System Viva UI: {url}")
    print(f"Session: {session_path}")
    print("Waiting for one submission. Press Ctrl-C to stop.")

    try:
        while not done.is_set():
            server.handle_request()
    except KeyboardInterrupt:
        print("\nStopped without submission.", file=sys.stderr)
        return 130
    finally:
        server.server_close()

    print("Submission received.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
