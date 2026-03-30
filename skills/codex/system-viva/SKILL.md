---
name: system-viva
description: Use after multiple AI-assisted coding iterations when the goal is to batch important changes into one short human learning session. Generate a compact quiz, collect answers in a local web page, evaluate understanding, update a learner profile, and produce a cited LaTeX Beamer debrief.
---

# System Viva

Use this skill to turn AI-assisted coding work into deliberate human learning.

Optimize for system understanding, not activity volume.

## Modes

1. Capture
- Extract 1-5 learning atoms from the current task.
- Append them to `docs/learning/queue.jsonl`.
- Do not run a quiz.

2. Session
- Batch queued atoms plus the current task if relevant.
- Build one short learning session.
- Default target: 1-2 sessions per day, not one session per generation.

## Canonical storage

Keep storage minimal. Persist only:

- `docs/learning/profile.yaml`
- `docs/learning/queue.jsonl`
- `docs/learning/sessions/<stamp>/session.json`
- `docs/learning/sessions/<stamp>/debrief.tex`
- `docs/learning/sessions/<stamp>/refs.bib`

`session.json` is the session source of truth. Store:

- theme
- selected atoms
- questions
- human answers
- evaluation
- next-focus notes
- source URLs and local file refs

Do not create extra summary files unless the user asks for them.

Minimal question fields:

- `id`
- `kind`: `mcq`, `open`, or `code`
- `prompt`
- `options` for `mcq`
- `concept`
- `why_it_matters`

## Session composition

- Cluster queued atoms into 1-3 themes.
- Select only high-value concepts:
  - core algorithm or invariant
  - request, state, or data flow
  - module boundary or contract
  - failure mode or risk
  - tradeoff behind the design
  - test logic that protects the change
- Skip trivia such as filenames, raw commit history, or syntax recall.

## Question mix

Aim for:

- 3-5 multiple-choice questions
- 2-3 open-ended questions
- 0-1 mini coding task
- 1 spaced-recall question from a prior weak area when `profile.yaml` exists

### Multiple-choice rules

- Prefer 3 options.
- Write distractors as plausible misconceptions.
- Avoid obviously wrong or joke options.
- Test reasoning, not recollection.

### Open-ended rules

Good prompts:

- explain the new guarantee
- trace a concrete input or request
- name the invariant
- predict one failure mode
- justify the design tradeoff

### Mini coding task rules

Keep it under 10 minutes:

- write one regression test
- fill one key branch
- add one assertion
- reorder a Parsons-style snippet

## Delivery

When interaction is needed, launch the local quiz UI after `session.json` has been written and before any grading or deck generation.

Run:

```bash
python3 skills/codex/system-viva/scripts/run_quiz_ui.py docs/learning/sessions/<stamp>/session.json
```

Workflow:

1. generate `session.json`
2. run the quiz UI script
3. tell the human the local URL printed by the script
4. wait for the process to exit after submission
5. continue with evaluation, `profile.yaml`, and `debrief.tex`

- Keep the UI plain and reliable.
- Render MCQ, open-ended, code box, and confidence input.
- Load questions from `session.json`.
- Save the final submission back into `session.json`.

Avoid heavy frameworks unless the repo already has one ready to use.

Read `scripts/run_quiz_ui.py` before implementing a custom UI. Reuse it unless the task clearly needs more.

## Evaluation

- Grade against concept rubrics, not exact wording.
- Record confidence calibration when possible.
- Update `profile.yaml` with compact concept-level notes:
  - strong areas
  - weak areas
  - recurring misconceptions
  - last reviewed

Keep the learner model interpretable. Do not introduce opaque scoring unless the user asks for it.

## Debrief deck

After answers are submitted, generate `debrief.tex` as a cited Beamer deck.

Use Beamer, not PPTX.

Deck shape:

1. Title and session theme
2. What changed across the batch
3. One slide per question:
- question
- answer summary
- correct reasoning
- misconception diagnosis
- why it matters here
- citations
4. Closing slide:
- strengths
- weak areas
- next session focus

Read `assets/debrief-template.tex` before generating a new deck.

## Beamer guidance

Use the design direction from:

- [K-Dense scientific-slides](https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/scientific-slides)

Apply it in a lean way:

- visual-first
- minimal text
- strong hierarchy
- citations on-slide when useful
- appendix or final references slide for overflow

Prefer diagrams over long bullets. Use code snippets only when they teach the concept.

## Source order

Prefer sources in this order:

1. local code, tests, docs, ADRs
2. official framework or library docs
3. specs or papers
4. blog posts only when they add real context

Use exact dates for time-sensitive web sources.

## Output expectations

When the user asks for a session:

1. build or update the canonical files
2. keep the session compact
3. clearly separate facts from inference
4. say if web research or PDF compilation could not be completed
