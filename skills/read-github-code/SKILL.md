---
name: read-github-code
description: Use when the user shares a GitHub URL, names an owner/repo, or asks to inspect how a public repository works. Start with fast orientation, then switch to direct source reading when implementation detail matters.
---

# Read GitHub Code

Read repositories with a concrete question in mind. Start broad, narrow quickly, and ground claims in actual files.

## Define the question

Before reading, state what must be understood:

- architecture
- entrypoints
- build system
- plugin or extension model
- data flow
- a specific subsystem

Use that question to decide how deep to go.

## Resolve the repository

Accept:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo/tree/main/path`
- `owner/repo`

Extract `owner/repo` first. Treat any provided path as an initial clue, not the entire scope.

## Two-pass workflow

### Pass 1: Survey

Start with the fastest high-signal material:

1. README and docs
2. package or build manifests
3. top-level tree
4. obvious entrypoints
5. DeepWiki or other generated summaries only as orientation aids

At the end of the survey, identify:

- the likely entrypoint
- the relevant directories
- the files to read next
- unresolved questions

### Pass 2: Source read

If the question needs implementation-level confidence:

1. Read the relevant source files.
2. Follow imports, registrations, routes, hooks, or interfaces inward.
3. Use search to trace symbols and feature flags.
4. Skip unrelated, vendored, or generated code unless it answers the question.

Clone only when repository browsing is not enough or local search is needed. Prefer a shallow clone.

## Reading heuristics

- Start from public surfaces before internal helpers.
- Find the orchestrator before reading leaf utilities.
- Distinguish facts from inferences.
- For large repos, read a representative slice rather than everything.

## Output

Return:

1. The repository and the question being answered.
2. A concise architecture summary.
3. The exact files or modules that answer the question.
4. Any inferred behavior, clearly labeled.
5. Remaining unknowns.

Do not write a summary file to disk unless the user asks for one.
