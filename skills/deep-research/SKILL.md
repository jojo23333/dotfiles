---
name: deep-research
description: Extensive web research and evidence synthesis for ambiguous or high-impact questions. Use when design choices, requirements, or technical facts are unclear and external validation is needed. Search iteratively until new high-confidence findings stop appearing, then return a filtered, source-backed conclusion.
---

# Deep Research

## Workflow

1. Define the research target.
- Write one primary question and the decision it affects.
- Capture constraints such as recency, cost, platform, compliance, or geography.

2. Build a search map.
- Break the problem into 4-8 evidence axes.
- Prefer primary sources first:
  - official documentation, specs, and changelogs
  - maintainer or vendor announcements
  - peer-reviewed papers or authoritative reports
  - first-party benchmarks, repos, or issue trackers

3. Search iteratively.
- Start broad, then narrow to unresolved gaps.
- For every material claim, record:
  - the claim
  - the source
  - the date
  - whether it is directly stated or inferred

4. Stop at saturation.
- Continue until two consecutive rounds add no materially new high-confidence findings.
- Ignore duplicate, off-scope, or weakly sourced claims.

5. Filter before answering.
- Remove irrelevant and low-signal results.
- Preserve real disagreement between credible sources.
- Separate facts from inference.

## Single-source deep dive

If the user wants one source studied deeply:

1. Map the source structure.
2. Extract key claims and assumptions.
3. Cross-check important claims against independent sources when the stakes justify it.
4. Report what is confirmed, contradicted, and still unverified.

## Output format

Return in this structure:

```markdown
## Research Question
...

## Executive Answer
...

## Key Findings
1. ...
2. ...

## Implications
- ...

## Remaining Unknowns
- ...

## Sources
1. [Title](URL) - why it matters
2. ...
```

## Quality bar

- Cite every material claim.
- Prefer at least 3 independent high-quality sources for major conclusions.
- Use exact dates for time-sensitive information.
- Keep searching until saturation, not a fixed query count.
