---
name: read-arxiv-paper
description: Use when the user shares an arXiv or AlphaXiv URL, gives a paper ID, or asks to summarize, critique, compare, or apply a research paper.
---

# Read arXiv Paper

Read the paper for the user’s actual goal: summary, critique, implementation guidance, comparison, or applicability to a local problem.

## Resolve the paper

Support:

- `https://arxiv.org/abs/<id>`
- `https://arxiv.org/pdf/<id>`
- `https://alphaxiv.org/overview/<id>`
- bare IDs such as `2401.12345` or `2401.12345v2`

Extract the canonical paper identifier first.

## Two-pass workflow

### Pass 1: Orientation

Start with:

1. abstract
2. introduction
3. figures and tables
4. conclusion
5. any machine-readable overview if available

Use this pass to answer:

- what problem is solved
- the main technical idea
- claimed contributions
- evidence offered
- obvious limitations

### Pass 2: Deep read

If more confidence is needed:

1. read the method carefully
2. inspect datasets, baselines, and ablations
3. check whether improvements are broad or conditional
4. read appendices or source files when key details are missing

Download and inspect TeX source when equations, implementation details, or paper structure matter and summary views are insufficient.

## Evaluation checklist

Always track:

- assumptions
- method
- data and benchmark setting
- main results
- fairness of comparison
- limitations
- what would be needed to reproduce or adapt it

## Project relevance

When the paper is being evaluated for a codebase or product:

1. map the paper’s inputs and outputs to the local problem
2. identify the minimum useful idea to copy
3. call out missing data, infra, or compute assumptions
4. separate interesting ideas from practical next steps

## Output

Return:

1. a plain-language summary
2. the method and why it works
3. the strongest evidence and biggest caveats
4. what matters for implementation or adoption
5. open questions or unverifiable claims

Do not write a summary file to disk unless the user asks for one.
