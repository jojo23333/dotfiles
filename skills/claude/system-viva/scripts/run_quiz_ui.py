#!/usr/bin/env python3
"""Serve a local System Viva quiz UI with immediate teaching review.

The server reads a session JSON file, renders the questions in a small local
web app, writes the human submission back into the same file, computes a
deterministic educational review from the stored answer key and teaching
metadata, returns that review to the page, then exits.
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
      --warn: #b45309;
      --bad: #b91c1c;
      --info: #1d4ed8;
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

    h2 {{
      margin: 0;
      font-size: 1.18rem;
      line-height: 1.3;
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

    .card,
    .review-shell,
    .review-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}

    .card,
    .review-card {{
      padding: 22px;
    }}

    .review-shell {{
      padding: 24px;
      margin-top: 22px;
    }}

    .review-head {{
      margin-bottom: 18px;
    }}

    .review-grid {{
      display: grid;
      gap: 16px;
    }}

    .card-head,
    .review-card-head {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 12px;
    }}

    .badge,
    .status-tag {{
      flex: 0 0 auto;
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: white;
    }}

    .badge {{
      background: var(--accent);
    }}

    .status-tag[data-status="correct"] {{
      background: var(--good);
    }}

    .status-tag[data-status="review"] {{
      background: var(--warn);
    }}

    .status-tag[data-status="needs_review"] {{
      background: var(--bad);
    }}

    .status-tag[data-status="unanswered"] {{
      background: var(--muted);
    }}

    .status-tag[data-status="self_check"] {{
      background: var(--info);
    }}

    .context,
    .note,
    .review-intro,
    .summary-note {{
      color: var(--muted);
      line-height: 1.55;
      margin: 0 0 12px;
    }}

    .why,
    .teaching-block,
    .answer-block {{
      margin: 14px 0 0;
      padding: 12px 14px;
      border-radius: 12px;
      font-size: 0.95rem;
      line-height: 1.55;
    }}

    .why {{
      border-left: 4px solid var(--accent-2);
      background: #f9f4e7;
      color: #5f4b16;
    }}

    .answer-block {{
      background: #f7f5ef;
      border: 1px solid var(--line);
    }}

    .teaching-block {{
      background: #eef6f8;
      border-left: 4px solid var(--accent);
      color: var(--ink);
    }}

    .misconception {{
      background: #fff3f1;
      border-left: 4px solid #dc2626;
      color: #7f1d1d;
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

    textarea,
    select {{
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

    .review-list {{
      margin: 10px 0 0;
      padding-left: 18px;
      color: var(--ink);
      line-height: 1.55;
    }}

    .review-list li + li {{
      margin-top: 6px;
    }}

    .answer-text {{
      white-space: pre-wrap;
      word-break: break-word;
      margin-top: 4px;
    }}

    .detail-label {{
      display: block;
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 2px;
      font-weight: 700;
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
      margin-top: 24px;
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

      .hero,
      .card,
      .review-shell,
      .review-card {{
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

    <section id="review-shell" class="review-shell" hidden>
      <div class="review-head">
        <p class="eyebrow">Immediate Review</p>
        <h2 id="review-title">Educational Review</h2>
        <p id="review-intro" class="review-intro"></p>
        <div id="review-meta" class="meta"></div>
      </div>
      <div id="review-content" class="review-grid"></div>
    </section>

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
    const reviewShell = document.getElementById("review-shell");
    const reviewIntro = document.getElementById("review-intro");
    const reviewContent = document.getElementById("review-content");
    const reviewMeta = document.getElementById("review-meta");

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

    const statusLabel = (status) => {{
      if (status === "correct") return "Correct";
      if (status === "review") return "Reinforce";
      if (status === "needs_review") return "Needs review";
      if (status === "unanswered") return "Unanswered";
      return "Self-check";
    }};

    const makePill = (text) => {{
      const pill = document.createElement("div");
      pill.className = "pill";
      pill.textContent = text;
      return pill;
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

    const makeTextBlock = (label, text, className = "answer-block") => {{
      if (!text) return null;
      const block = document.createElement("div");
      block.className = className;
      const title = document.createElement("span");
      title.className = "detail-label";
      title.textContent = label;
      const value = document.createElement("div");
      value.className = "answer-text";
      value.textContent = text;
      block.appendChild(title);
      block.appendChild(value);
      return block;
    }};

    const makeListBlock = (label, items) => {{
      if (!Array.isArray(items) || items.length === 0) return null;
      const block = document.createElement("div");
      block.className = "answer-block";
      const title = document.createElement("span");
      title.className = "detail-label";
      title.textContent = label;
      const list = document.createElement("ul");
      list.className = "review-list";
      items.forEach((item) => {{
        const li = document.createElement("li");
        li.textContent = item;
        list.appendChild(li);
      }});
      block.appendChild(title);
      block.appendChild(list);
      return block;
    }};

    const disableForm = () => {{
      form.querySelectorAll("input, textarea, select, button").forEach((element) => {{
        element.disabled = true;
      }});
      submitBtn.disabled = true;
      submitBtn.textContent = "Submitted";
    }};

    const renderReview = (review) => {{
      if (!review || !Array.isArray(review.questions)) return;

      reviewShell.hidden = false;
      reviewContent.replaceChildren();
      reviewMeta.replaceChildren();

      const counts = review.summary && review.summary.counts ? review.summary.counts : {{}};
      const countBits = [
        counts.correct ? String(counts.correct) + " solid" : null,
        counts.review ? String(counts.review) + " reinforce" : null,
        counts.needs_review ? String(counts.needs_review) + " revisit" : null,
        counts.unanswered ? String(counts.unanswered) + " unanswered" : null,
        counts.self_check ? String(counts.self_check) + " self-check" : null
      ].filter(Boolean);

      reviewIntro.textContent = (review.summary && review.summary.headline)
        || "Use these cards as a guided teach-back for the concepts you missed or felt shaky on.";

      countBits.forEach((bit) => {{
        reviewMeta.appendChild(makePill(bit));
      }});

      review.questions.forEach((item, index) => {{
        const card = document.createElement("section");
        card.className = "review-card";

        const head = document.createElement("div");
        head.className = "review-card-head";

        const titleWrap = document.createElement("div");
        const title = document.createElement("h2");
        title.textContent = String(index + 1) + ". " + String(item.prompt || "Question");
        titleWrap.appendChild(title);

        const summary = document.createElement("p");
        summary.className = "summary-note";
        summary.textContent = item.headline || "Compare your answer with the reference reasoning below.";
        titleWrap.appendChild(summary);

        const tag = document.createElement("div");
        tag.className = "status-tag";
        tag.dataset.status = item.status || "self_check";
        tag.textContent = item.status_label || statusLabel(item.status);

        head.appendChild(titleWrap);
        head.appendChild(tag);
        card.appendChild(head);

        const yourAnswer = makeTextBlock("Your answer", item.your_answer || "");
        if (yourAnswer) card.appendChild(yourAnswer);

        const referenceAnswer = makeTextBlock("Reference answer", item.reference_answer || "");
        if (referenceAnswer) card.appendChild(referenceAnswer);

        const explanation = makeTextBlock(
          "Teaching explanation",
          item.teaching_explanation || "",
          "teaching-block"
        );
        if (explanation) card.appendChild(explanation);

        const misconception = makeTextBlock(
          "Likely misconception",
          item.misconception || "",
          "teaching-block misconception"
        );
        if (misconception) card.appendChild(misconception);

        const checkpoints = makeListBlock(
          item.kind === "mcq" ? "Key takeaways" : "Checkpoints to compare against",
          item.checkpoints || []
        );
        if (checkpoints) card.appendChild(checkpoints);

        const teachingPoints = makeListBlock("What to remember", item.teaching_points || []);
        if (teachingPoints) card.appendChild(teachingPoints);

        const confidenceNote = makeTextBlock("Confidence note", item.confidence_note || "");
        if (confidenceNote) card.appendChild(confidenceNote);

        const why = makeTextBlock("Why it mattered here", item.why_it_matters || "", "why");
        if (why) card.appendChild(why);

        reviewContent.appendChild(card);
      }});

      reviewShell.scrollIntoView({{ behavior: "smooth", block: "start" }});
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

    if (payload.status === "submitted" && payload.immediate_review) {{
      form.hidden = true;
      disableForm();
      statusEl.textContent = "Submission already recorded. Review is shown below.";
      statusEl.className = "success";
      renderReview(payload.immediate_review);
    }}

    submitBtn.addEventListener("click", async () => {{
      submitBtn.disabled = true;
      statusEl.textContent = "Submitting answers and building your review...";

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

      const result = await response.json().catch(() => null);

      if (!response.ok || !result) {{
        statusEl.textContent = "Submission failed. Keep the page open and try again.";
        submitBtn.disabled = false;
        return;
      }}

      disableForm();
      form.hidden = true;
      statusEl.textContent = "Submission saved. Your educational review is below.";
      statusEl.className = "success";
      renderReview(result.review);
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


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def parse_confidence(value: object) -> int | None:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if 1 <= parsed <= 5 else None


def listify(value: object) -> list[str]:
    if isinstance(value, list):
        return [normalize_text(item) for item in value if normalize_text(item)]
    text = normalize_text(value)
    return [text] if text else []


def option_value(option: object, index: int) -> str:
    if isinstance(option, dict):
        return str(option.get("value", index))
    return str(index)


def option_label(option: object, index: int) -> str:
    if isinstance(option, dict):
        return normalize_text(
            option.get("label")
            or option.get("text")
            or option.get("value")
            or index
        )
    return normalize_text(option)


def find_option(question: dict, answer_value: str) -> dict | None:
    for index, option in enumerate(question.get("options", [])):
        if option_value(option, index) == answer_value:
            if isinstance(option, dict):
                return option
            return {"value": answer_value, "label": option_label(option, index)}
    return None


def status_label(status: str) -> str:
    labels = {
        "correct": "Correct",
        "review": "Reinforce",
        "needs_review": "Needs review",
        "unanswered": "Unanswered",
        "self_check": "Self-check",
    }
    return labels.get(status, "Review")


def confidence_note(status: str, confidence: int | None) -> str:
    if confidence is None:
        return ""
    if status == "correct" and confidence <= 2:
        return "You were right, but low confidence suggests this concept still needs one more clean rehearsal."
    if status in {"needs_review", "unanswered"} and confidence >= 4:
        return "High confidence with a miss is a strong clue that the mental model, not just recall, needs correction."
    if status in {"review", "self_check"} and confidence <= 2:
        return "Low confidence is useful signal. Rehearse this flow again soon while the context is still fresh."
    if status == "correct" and confidence >= 4:
        return "High confidence plus a correct answer usually means this concept is stabilizing."
    return ""


def question_reference_answer(question: dict, fallback: str = "") -> str:
    answer = normalize_text(
        question.get("reference_answer")
        or question.get("ideal_answer")
        or question.get("correct_answer")
    )
    if answer:
        return answer

    rubric_points = listify(question.get("rubric"))
    if rubric_points:
        return "A strong answer should cover: " + "; ".join(rubric_points)

    return normalize_text(fallback)


def question_teaching_explanation(question: dict) -> str:
    explanation = normalize_text(
        question.get("teaching_explanation")
        or question.get("correct_reasoning")
        or question.get("explanation")
        or question.get("answer_explanation")
    )
    if explanation:
        return explanation

    reference = question_reference_answer(question)
    why = normalize_text(question.get("why_it_matters"))
    if reference and why:
        return f"{reference} This mattered in the session because {why}"
    if reference:
        return reference
    return why


def question_misconception(question: dict) -> str:
    return normalize_text(
        question.get("misconception_if_wrong")
        or question.get("common_misconception")
        or question.get("misconception")
    )


def build_mcq_review(question: dict, answer_entry: dict) -> dict:
    answer_value = normalize_text(answer_entry.get("answer"))
    confidence = parse_confidence(answer_entry.get("confidence"))
    correct_value = normalize_text(question.get("correct_option"))

    selected = find_option(question, answer_value) if answer_value else None
    correct = find_option(question, correct_value) if correct_value else None

    selected_label = normalize_text(selected.get("label")) if selected else ""
    correct_label = normalize_text(correct.get("label")) if correct else ""

    if not answer_value:
        status = "unanswered"
        headline = "You left this blank, so start by studying the reference answer and explanation."
    elif correct_value and answer_value == correct_value:
        status = "review" if confidence is not None and confidence <= 2 else "correct"
        if status == "correct":
            headline = "You got the main reasoning. Use the explanation below as a compact reinforcement pass."
        else:
            headline = "You likely knew this, but low confidence suggests the concept is still a little fragile."
    else:
        status = "needs_review"
        headline = "This answer points to a misconception or boundary you should correct before the pattern hardens."

    misconception = ""
    if status == "needs_review":
        misconception = normalize_text(
            (selected or {}).get("misconception")
            or (selected or {}).get("teaching_note")
            or (selected or {}).get("explanation")
        ) or question_misconception(question)

    reference_answer = question_reference_answer(question, correct_label)
    teaching_points = listify(question.get("teaching_points"))

    if not teaching_points and correct_label:
        teaching_points = [f"Correct answer: {correct_label}"]

    return {
        "id": question.get("id"),
        "prompt": normalize_text(question.get("prompt")),
        "kind": "mcq",
        "concept": normalize_text(question.get("concept")),
        "status": status,
        "status_label": status_label(status),
        "headline": headline,
        "your_answer": selected_label or "",
        "reference_answer": reference_answer,
        "teaching_explanation": question_teaching_explanation(question),
        "misconception": misconception,
        "teaching_points": teaching_points,
        "checkpoints": listify(question.get("rubric")),
        "why_it_matters": normalize_text(question.get("why_it_matters")),
        "confidence_note": confidence_note(status, confidence),
    }


def build_subjective_review(question: dict, answer_entry: dict) -> dict:
    answer_text = normalize_text(answer_entry.get("answer"))
    confidence = parse_confidence(answer_entry.get("confidence"))

    if not answer_text:
        status = "unanswered"
        headline = "You skipped this, so use the reference answer and checkpoints as the study guide."
    elif confidence is not None and confidence <= 2:
        status = "review"
        headline = "Your low confidence is the cue here. Compare your reasoning against the reference answer and checkpoints."
    else:
        status = "self_check"
        headline = "Use the reference answer below to compare structure, missing ideas, and depth against your own response."

    return {
        "id": question.get("id"),
        "prompt": normalize_text(question.get("prompt")),
        "kind": normalize_text(question.get("kind")) or "open",
        "concept": normalize_text(question.get("concept")),
        "status": status,
        "status_label": status_label(status),
        "headline": headline,
        "your_answer": answer_text,
        "reference_answer": question_reference_answer(question),
        "teaching_explanation": question_teaching_explanation(question),
        "misconception": question_misconception(question),
        "teaching_points": listify(question.get("teaching_points")),
        "checkpoints": listify(question.get("rubric")),
        "why_it_matters": normalize_text(question.get("why_it_matters")),
        "confidence_note": confidence_note(status, confidence),
    }


def build_immediate_review(session_data: dict, answers: list[dict]) -> dict:
    answers_by_id = {
        normalize_text(answer.get("id")): answer
        for answer in answers
        if isinstance(answer, dict) and normalize_text(answer.get("id"))
    }

    review_questions: list[dict] = []
    counts = {
        "correct": 0,
        "review": 0,
        "needs_review": 0,
        "unanswered": 0,
        "self_check": 0,
    }

    for question in session_data.get("questions", []):
        if not isinstance(question, dict):
            continue

        answer_entry = answers_by_id.get(normalize_text(question.get("id")), {})
        if normalize_text(question.get("kind")) == "mcq":
            item = build_mcq_review(question, answer_entry)
        else:
            item = build_subjective_review(question, answer_entry)

        counts[item["status"]] = counts.get(item["status"], 0) + 1
        review_questions.append(item)

    if counts["needs_review"] or counts["unanswered"]:
        headline = (
            "Start with the cards marked Needs review or Unanswered. They are the fastest route "
            "to correcting the concepts that could trip you up again."
        )
    elif counts["review"]:
        headline = (
            "You were mostly on track, but some concepts still look shaky. Use the review cards "
            "to turn partial recall into clean understanding."
        )
    else:
        headline = (
            "Strong pass. Use these cards as compact retrieval notes so the reasoning stays easy "
            "to reconstruct later."
        )

    return {
        "generated_at": utc_now(),
        "summary": {
            "headline": headline,
            "counts": counts,
        },
        "questions": review_questions,
    }


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
            review = build_immediate_review(session_data, answers)

            session_data["human_answers"] = answers
            session_data["submitted_at"] = utc_now()
            session_data["status"] = "submitted"
            session_data["immediate_review"] = review
            write_session(session_path, session_data)

            self._send_json(HTTPStatus.OK, {"ok": True, "review": review})
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
    print("Waiting for one submission. The page will show an immediate educational review.")

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
