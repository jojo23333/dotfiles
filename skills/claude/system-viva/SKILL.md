---
name: system-viva
description: This skill should be used after multiple AI-assisted coding iterations when the goal is to batch meaningful changes into one short human learning session with a quiz, immediate teaching review, learner profile update, and cited LaTeX Beamer debrief.
version: 1.0.0
---

# System Viva

Use this skill to turn AI-assisted coding work into deliberate human learning. If arguments were provided, treat `$ARGUMENTS` as the current task context and include it when selecting learning atoms.

Optimize for system understanding, not activity volume.

## Teaching philosophy

Act as a senior engineer running a 1-on-1 with a junior teammate after a code change lands.

Guiding principles:

- **Build the big picture first.** Before drilling into any detail, make sure the learner can sketch the overall system on a whiteboard. A senior engineer never quizzes on an edge case before confirming the mentee understands the flow the edge case lives in.
- **Assume the learner is arriving cold.** They may have been away, context-switched, or simply watching the AI work. Never assume they already know what just changed or why. Provide enough framing in every question that someone re-entering the codebase can orient themselves.
- **Ask "why" more than "what."** Prefer questions that surface design intent, tradeoffs, and failure reasoning over questions that test recall of names, flags, or syntax.
- **Make wrong answers educational.** Distractors and anticipated wrong answers should represent real misconceptions a junior engineer would hold, not trick options. When the learner picks one, the correction itself should be a teaching moment.
- **Respect the learner's time.** Keep sessions short and high-signal. One well-chosen question about an invariant teaches more than five questions about file paths.

## Adaptive difficulty

Tailor every session to the individual learner's current level.

**When no `profile.yaml` exists (first session or unknown learner):**

- Assume the learner is out of context and unfamiliar with the codebase.
- Start with foundational, high-level questions: what does this system do, what are its main components, how does data flow through it.
- Use simple, concrete language. Avoid jargon until the learner has demonstrated they understand the basics.
- Limit the session to 3-4 questions so it feels approachable, not overwhelming.
- After scoring, create `profile.yaml` with an initial read on their comfort zones and gaps.

**When `profile.yaml` exists:**

- Read `strong_areas` and `weak_areas` before composing any questions.
- Spend most question budget on weak or unvisited areas — push the boundary of their understanding.
- Include 1 spaced-recall question from a previously weak topic to check retention.
- If the learner has been consistently strong at high-level flow questions, skip those and start deeper (module-level or algorithm-level).
- If prior sessions show recurring misconceptions, design at least one question that directly targets the misconception with a new example.
- Gradually increase difficulty across sessions: a learner who aced module I/O questions last time should face algorithm-internals or efficiency questions this time.

**Difficulty calibration signals:**

- Confidence scores from prior submissions (low confidence on correct answers = shaky understanding, still probe).
- Recurring wrong-answer patterns (same misconception twice = needs a different angle, not the same question).
- Time since last session on a topic (longer gap = re-anchor with a context-setting question before going deep).

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
- immediate review
- evaluation
- next-focus notes
- source URLs and local file refs

Do not create extra summary files unless the user asks for them.

Minimal question fields:

- `id`
- `kind`: `mcq`, `open`, or `code`
- `layer`: `1-system`, `2-module`, `3-algorithm`, `4-implementation`, or `5-crosscutting`
- `prompt`
- `options` for `mcq`
- `concept`
- `why_it_matters`

Teaching fields expected for every session question:

- `reference_answer`
- `teaching_explanation`
- `teaching_points`

Also include:

- `correct_option` for `mcq`
- `misconception_if_wrong` when there is a common trap worth teaching directly
- `rubric` checkpoints for `open` and `code`

The local UI should be able to teach from `session.json` without waiting for a later model pass.

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

## Question progression: high-level → low-level

Organize every session as a guided descent from the system level down to implementation details. This mirrors how a senior engineer would onboard someone: start with the map, then zoom in.

### Layer 1 — System & design intent (always start here for new/cold learners)

Purpose: Can the learner explain what the system does and why it is shaped this way?

Example question angles:

- What is the end-to-end pipeline for a request / data item / user action?
- Draw or describe the high-level flow map of the components involved in this change.
- What is the core design philosophy or architectural principle behind this system?
- What problem does the system solve, and what constraints shaped the solution?
- Where does this change sit in the overall system? What triggers it and what consumes its output?

Skip this layer only when `profile.yaml` shows the learner has consistently demonstrated strong system-level understanding in recent sessions.

### Layer 2 — Module boundaries & interfaces

Purpose: Can the learner identify the main modules and explain how they connect?

Example question angles:

- What are the 2-3 most important modules (or services/classes) touched by this change?
- What is the input and output contract of each module? What data shapes cross the boundary?
- Which API endpoints or internal interfaces are involved, and what do they guarantee?
- How do modules communicate — sync calls, events, shared state, message queues?
- If module X fails, what happens to module Y downstream?

### Layer 3 — Internal design & algorithms

Purpose: Can the learner explain how a module achieves its job internally?

Example question angles:

- What algorithm or strategy does module X use to accomplish its task?
- What invariant must hold inside this component for correctness?
- What data structures were chosen and why? What are the tradeoffs?
- Walk through the core logic path for a concrete input — what happens step by step?
- What is the state machine or lifecycle of the key entity in this module?

### Layer 4 — Implementation details & syntax

Purpose: Can the learner work at the code level — functions, APIs, language specifics?

Example question angles:

- What does function X do, and what are its preconditions?
- What language feature or library API is being used here, and what are its gotchas?
- Spot the bug: given this snippet, what goes wrong and why?
- Write a small test or assertion that would catch the failure this change prevents.
- What happens if this argument is null / this list is empty / this timeout expires?

### Layer 5 — Cross-cutting concerns (weave in throughout)

Purpose: Does the learner think about the qualities that cut across all layers?

Example question angles:

- What is the performance/efficiency implication of this change? Time complexity? Memory?
- How does this change affect observability — logging, metrics, tracing?
- What are the security implications? Input validation? Auth boundaries?
- How does this change behave under concurrency or high load?
- What is the rollback or failure-recovery story?

### Progression rules

- **For a new or cold learner:** Start at Layer 1, spend most questions there and in Layer 2. Include at most one Layer 3 question. Do not ask Layer 4 questions in the first session.
- **For a learner with established profile:** Enter at the deepest layer where they last showed weakness. Include one Layer 1-2 anchor question for orientation, then push into Layers 3-5.
- **Within a single session:** Questions should flow downward through the layers, not jump randomly. The learner should feel the zoom-in: "first I understood the system, then the modules, then the internals."
- **Never start a session with a syntax or function-level question** unless the learner has explicitly demonstrated mastery of all higher layers for this area of the codebase.

## Question mix

Aim for:

- 3-5 multiple-choice questions (spread across the layers being covered)
- 2-3 open-ended questions (prefer these for Layer 1-2 where explanation reveals understanding)
- 0-1 mini coding task (best suited for Layer 3-4)
- 1 spaced-recall question from a prior weak area when `profile.yaml` exists

### Multiple-choice rules

- Prefer 3 options.
- Write distractors as plausible misconceptions.
- Avoid obviously wrong or joke options.
- Test reasoning, not recollection.
- Include the real answer key and a concise explanation of why the distractors are wrong.

### Open-ended rules

Good prompts:

- explain the new guarantee
- trace a concrete input or request
- name the invariant
- predict one failure mode
- justify the design tradeoff

For each open question, provide:

- a short `reference_answer`
- a richer `teaching_explanation`
- 2-5 rubric checkpoints the learner can compare against

### Mini coding task rules

Keep it under 10 minutes:

- write one regression test
- fill one key branch
- add one assertion
- reorder a Parsons-style snippet

For each coding task, include:

- the smallest acceptable solution shape in `reference_answer`
- what makes a solution correct in `rubric`
- the likely bug or misconception the task is meant to surface

## Immediate Teaching Review

After the learner submits, the local quiz page must show a detailed educational explanation for each question right away.

This review should:

- identify clearly wrong answers for `mcq`
- flag unanswered or low-confidence answers as concepts to reinforce
- show a reference answer for every question
- explain the correct reasoning in plain language
- call out the likely misconception or trap when helpful
- restate why the concept mattered in the real code change

For `open` and `code` questions, the immediate local review can be deterministic and reference-based rather than fully semantic. If exact grading cannot happen in-browser, still show:

- the reference answer
- the rubric checkpoints
- the teaching explanation
- what the learner should compare in their own answer

Never end the local quiz flow with only a submission confirmation when teaching content is available.

## Delivery

When interaction is needed, launch the local quiz UI after `session.json` has been written and before any grading or deck generation.

Run:

```bash
python3 skills/claude/system-viva/scripts/run_quiz_ui.py docs/learning/sessions/<stamp>/session.json
```

Workflow:

1. generate `session.json`
2. run the quiz UI script
3. tell the human the local URL printed by the script
4. after submission, ensure the UI shows the immediate educational review question by question
5. wait for the process to exit after the submission/review handoff
6. continue with deeper evaluation, `profile.yaml`, and `debrief.tex`

- Keep the UI plain and reliable.
- Render MCQ, open-ended, code box, and confidence input.
- Load questions from `session.json`.
- Save the final submission back into `session.json`.
- Return a detailed immediate review payload from the submit step and render it in the page.

Avoid heavy frameworks unless the repo already has one ready to use.

Read `scripts/run_quiz_ui.py` before implementing a custom UI. Reuse it unless the task clearly needs more.

## Evaluation

Use two layers:

1. immediate local teaching review from the quiz UI
2. richer post-submit evaluation by the agent

- Grade against concept rubrics, not exact wording.
- Record confidence calibration when possible.
- Update `profile.yaml` with compact concept-level notes:
  - strong areas
  - weak areas
  - recurring misconceptions
  - last reviewed

Keep the learner model interpretable. Do not introduce opaque scoring unless the user asks for it.

The immediate review should optimize for learning momentum; the later agent evaluation can be more nuanced.

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
