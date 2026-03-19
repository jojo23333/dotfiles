---
name: read-github-code
description: This skill should be used when the user shares a GitHub URL, names an `owner/repo`, asks how an open-source repository works, or wants architecture or implementation details from code hosted on GitHub.
version: 1.0.0
---

# Read GitHub Code

Read a GitHub repository with a clear question in mind. Start broad, then narrow down until the answer is grounded in real files.

## Define the target

Before reading, state what must be learned. Examples:

- Authentication flow
- Build pipeline
- Plugin architecture
- Data model or storage layer
- A specific subsystem or file path

Use that question to decide how deep to go.

## Resolve the repository

Support these inputs:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo/tree/main/path`
- `owner/repo`

Extract the repository root first. Preserve any provided subpath as an initial clue, not the full scope by default.

## Work in two passes

### Pass 1: Survey

Start with the fastest high-signal sources:

1. Read the repository README.
2. Read docs or top-level design files if they exist.
3. Inspect the top-level tree and obvious entrypoints.
4. Use DeepWiki or a repo wiki only as a fast orientation aid, not as the final source of truth.

At the end of the survey, identify:

- The likely entrypoint
- The directories that matter
- The files worth reading next
- Any gaps that still require source inspection

### Pass 2: Source reading

If the question needs implementation-level confidence, read the actual source:

1. Prefer the exact files tied to the target question.
2. Follow imports, calls, registrations, and config references inward.
3. Use search tools to find symbols, feature flags, routes, hooks, and interfaces.
4. Skip unrelated folders, vendored code, generated code, and tests unless they answer the question.

Clone only when repository-level browsing is not enough or local search is required. Use a shallow clone when possible.

## Reading heuristics

- Start from public surfaces: README, CLI, routes, exported APIs, config, package manifests.
- Follow the control flow toward the implementation.
- When there are multiple layers, identify the orchestrator first, then helpers.
- Distinguish facts from inferences. Cite files for facts.
- If the repo is large, read a representative slice rather than everything.

## Output

Return:

1. The repository and question being analyzed.
2. A concise architecture summary.
3. The exact files or modules that answer the question.
4. Any inferred behavior, clearly labeled as inference.
5. Remaining unknowns or parts not verified.

Do not write a summary file to disk unless the user asks for one.
