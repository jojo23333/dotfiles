---
name: read-arxiv-paper
description: This skill should be used when the user shares an arXiv or AlphaXiv URL, gives a paper ID like `2401.12345`, or asks to read, summarize, critique, compare, or apply a research paper.
version: 1.0.0
---

# Read arXiv Paper

Read a paper with the user’s goal in mind. Focus on what the user needs: summary, critique, implementation guidance, comparison, or applicability to local work.

## Resolve the paper

Support these inputs:

- `https://arxiv.org/abs/<id>`
- `https://arxiv.org/pdf/<id>`
- `https://alphaxiv.org/overview/<id>`
- Bare IDs such as `2401.12345` or `2401.12345v2`

Extract the canonical paper identifier first.

## Work in two passes

### Pass 1: Fast orientation

Start with the abstract, introduction, figures, conclusion, and any machine-readable overview if available.

Use this pass to answer:

- What problem does the paper solve?
- What is the main technical idea?
- What are the claimed contributions?
- What evidence is offered?
- What are the obvious limitations?

### Pass 2: Deep read

If the user needs more than a high-level summary:

1. Read the method section carefully.
2. Inspect experiments, baselines, datasets, and ablations.
3. Check whether the claimed improvement is large, narrow, or conditional.
4. Read appendices or source files when critical details are missing from the main text.

Download and inspect TeX source when the paper structure or equations matter and the HTML or PDF view is insufficient.

## Evaluation checklist

Always track:

- Problem and assumptions
- Core method
- Data and benchmark setting
- Main results
- Baselines and fairness of comparison
- Failure modes and limitations
- What would be required to reproduce or adapt it

## Project relevance

When the paper is being read for an existing codebase or product idea:

1. Map the paper’s inputs and outputs to the local problem.
2. Identify the minimum part worth copying.
3. Call out missing infrastructure, data, or compute assumptions.
4. Separate “interesting idea” from “practical next step”.

## Output

Return:

1. A short plain-language summary.
2. The method and why it works.
3. The strongest evidence and the biggest caveats.
4. What matters for implementation or adoption.
5. Open questions or unverifiable claims.

Do not write a summary file to disk unless the user asks for one.
