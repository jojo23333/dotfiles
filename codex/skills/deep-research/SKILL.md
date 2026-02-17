---
name: deep-research
description: Extensive web research and evidence synthesis for ambiguous or high-impact questions. Use only in Plan mode when design choices, requirements, or technical facts are unclear and external validation is needed. Search iteratively until information saturation (no materially new high-confidence findings across two consecutive rounds), then return filtered, source-backed conclusions with irrelevant results removed.
---

# Deep Research

## Workflow

1. Confirm mode and trigger.
- Run this skill only in Plan mode.
- Apply when a plan-critical question is unclear, contested, or high impact.
- Typical triggers: "dive deep", "research options", "compare approaches", "verify assumptions", "find reliable sources".

2. Define the research target.
- Write one primary question and optional sub-questions.
- State the decision that depends on the answer.
- Capture constraints: date sensitivity, budget, platform, compliance, geography, performance targets.

3. Build a search map before browsing.
- Break the problem into 4-8 evidence axes.
- Prioritize primary sources first:
  - Official docs/specs/changelogs
  - Maintainer or vendor announcements
  - Peer-reviewed papers or authoritative technical reports
  - First-party benchmark repos/issues
- Add secondary sources only to fill gaps or cross-check.

4. Execute iterative search rounds.
- Start broad in round 1, then narrow based on unresolved gaps.
- For each source, extract:
  - Atomic claim
  - Evidence location
  - Recency
  - Credibility
  - Relevance to the target decision
- Track a running "new findings" list per round.

5. Stop at information saturation.
- Continue searching until two consecutive rounds add no materially new high-confidence findings.
- Treat as non-new:
  - Duplicates of already captured claims
  - Low-credibility or unsourced assertions
  - Off-scope details that do not affect the target decision

6. Filter and synthesize before returning.
- Remove irrelevant, noisy, or low-signal results.
- Preserve meaningful disagreement between sources.
- Mark uncertain claims explicitly.
- Separate facts from inferences.

## Single-Source Deep Dive

If the user asks to dive deep into one source (site, paper, docs page):
- Map the source structure first.
- Extract key claims and assumptions.
- Cross-check critical claims against independent sources when stakes are high.
- Report what is confirmed, contradicted, and still unverified.

## Output Format

Return in this structure:

```markdown
## Research Question
...

## Executive Answer
...

## Key Findings
1. ...
2. ...

## Design Implications
- Option A: ...
- Option B: ...
- Recommended: ... (with reason)

## Excluded Results
- ... (irrelevant, low credibility, or out of scope)

## Remaining Unknowns
- ...

## Sources
1. [Title](URL) - why it matters
2. ...
```

## Quality Bar

- Cite every material claim.
- Prefer at least 3 independent high-quality sources for major conclusions.
- Use exact dates for time-sensitive information.
- Keep searching until saturation, not a fixed query count.
