---
name: deep-research
description: This skill should be used when the user asks to "dive deep", "research options", "compare approaches", "verify assumptions", "look up reliable sources", or needs evidence-backed synthesis for a technical or product decision.
version: 1.0.0
context: fork
agent: general-purpose
---

# Deep Research

Research the user’s question thoroughly. If arguments were provided, treat `$ARGUMENTS` as the primary query. Otherwise infer the research question from the active request.

Use ultrathink.

## Workflow

1. State the primary research question and the decision it will inform.
2. Break the question into evidence axes such as vendor docs, changelogs, benchmarks, price, compatibility, security, operations, or migration cost.
3. Prioritize primary sources first:
   - official documentation
   - vendor announcements and changelogs
   - standards, papers, and maintainers
   - first-party benchmarks or issue trackers
4. Search iteratively instead of relying on one round of results.
5. For every material claim, capture:
   - the claim
   - the source
   - the date
   - whether it is directly stated or inferred
6. Keep searching until two consecutive rounds produce no materially new high-confidence findings.
7. Remove low-signal, duplicative, or off-scope results before answering.
8. Preserve meaningful disagreement between sources instead of flattening it away.

## Output

Return in this structure:

## Research Question

State the question in one sentence.

## Executive Answer

Give the shortest defensible answer.

## Key Findings

List the highest-signal facts with citations.

## Implications

Explain what the findings mean for the user’s decision.

## Remaining Unknowns

List what could not be verified confidently.

## Sources

List the URLs actually used.
