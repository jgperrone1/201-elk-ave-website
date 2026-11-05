# 201–207 Elk Ave S Medical & Executive Leasing Website (`201-elk-ave-website`)

This project builds and serves a local-first, static-compatible marketing and due-diligence web application for **207 Elk Ave S (201–207 Elk Ave S Medical Campus)** in historic downtown Fayetteville, TN. It serves prospective medical, dental, specialty outpatient, behavioral health, rehabilitation, and healthcare education tenants evaluating single-floor, phased, or full-building lease structures with ownership (**207 Elk LLC**). The primary technology stack is a zero-dependency Python 3.9+ static site builder and local HTTP server (`src/elk_ave/`) paired with semantic HTML5, modern CSS3 custom properties, and progressive vanilla JavaScript (`ES2022`).

---

# Primary Objectives

This project exists to:

- Present an Apple/Google-caliber interactive property showcase and clinical due-diligence portal generalized for all prospective medical and healthcare tenants.
- Quantify speed-to-market and Tenant Improvement (TI) capital preservation advantages (35+ plumbed clinical rooms, 7 procedure suites, X-ray/lab spaces, 12 ADA restrooms, central elevator, IBC Group B occupancy, and 0.5-acre dedicated parking lot).
- Maintain a zero-external-dependency, deterministically testable local build and preview workflow with strict provenance tracking back to source ownership materials.

---

# Repository Scope

This repository owns:

- Domain models, generalized property catalog, deterministic TI calculator, static HTML/JSON-LD renderer, and local preview HTTP server in `src/elk_ave/` and `main.py`
- Extracted, web-optimized property photographs, renovation renderings, drone aerials, architectural floorplans, and boundary surveys in `src/elk_ave/static/assets/images/`
- Automated unit and integration tests in `tests/`
- Project documentation and completion reports in `README.md` and `docs/`

This repository does **not** own:

- Raw upstream Canva design files or external graphic design authoring suites
- External CRM, lead-capture cloud databases, or third-party analytics pipelines
- Production DNS, CDN, or cloud hosting infrastructure (first draft is strictly local-only)

Do not modify systems or resources outside this ownership boundary unless the
user explicitly requests it. Permission to use a tool is not permission to
expand product scope.

---

# Current Development Scope

Current active work:

- Local-first MVP & executive web application on branch `feature/prototype-local`
- Approved scope: Initial generalized medical-tenant website built from `references/207 Elk Ave for TWU.pdf`, authorized by user on 2026-11-04 (`docs/completion-report.md`)

Deferred or out of scope:

- Cloud deployment, external form backend persistence, or third-party analytics tracking
- Interactive CAD/BIM editing or online lease execution/payment processing

Do not implement deferred work merely because a placeholder or extension point
exists. Record approvals with enough specificity that a later agent can tell
what was authorized, by whom, and when.

---

# High-Level Architecture

```text
[Reference Briefing & Extracted Property Assets]
        |
[Domain Models & Generalized Catalog (src/elk_ave/models.py, catalog.py)]
        |
[Deterministic TI Estimator & Static Renderer (src/elk_ave/calculator.py, renderer.py)]
        |
[Static Web Bundle (dist/) + Local HTTP Preview & JSON API (src/elk_ave/server.py, main.py)]
```

Dependencies flow strictly downward: `models.py` defines immutable data contracts; `catalog.py` and `calculator.py` implement pure domain data and business logic with zero UI or HTTP coupling; `renderer.py` compiles the catalog and static assets into a self-contained web bundle; `server.py` and `main.py` provide thin CLI and local HTTP orchestration.

---

# Repository Layout

```text
201-elk-ave-website/
├── main.py          # Thin CLI entrypoint (build, check, serve)
├── src/             # Production Python package (src/elk_ave/) and static web assets
├── tests/           # Automated unit and integration tests (unittest)
├── docs/            # Project documentation and completion reports
├── references/      # Local reference PDFs (Git-ignored via references/*.pdf)
└── tmp/             # Disposable scratch files; Git-ignored
```

Keep new files within the established layout. Add a new top-level directory
only when it represents a durable architectural boundary. Use the scratch
directory for disposable work only; never let it become an informal second
source of truth.

Reference material is not automatically authoritative. Confirm a file's role
before treating it as a template, contract, or source of record. Note that raw
Canva slides targeted at a single prospective tenant (`TWU`) must be generalized
for broad medical-tenant applicability before inclusion in `src/elk_ave/catalog.py`.

---

# Architecture Principles

- Favor reusable components over one-off implementations.
- Keep orchestration thin; place business logic in focused, testable modules.
- Maintain one canonical implementation for each business rule or behavior.
- Prefer composition over inheritance; avoid deep inheritance trees.
- Keep layers independent and dependencies flowing in the documented direction.
- Keep business logic portable: it should not depend on the CLI, UI, database,
  or a cloud service.
- Avoid duplicated business, validation, and integration logic.
- Preserve public contracts unless an intentional breaking change is approved.
  Public interfaces should change rarely; internal implementations may evolve.
- Make side effects explicit and isolate them from pure logic where practical.
- Build only what is needed now. Future flexibility comes from clean interfaces,
  not speculative abstractions. Design extension points early; do not implement
  plugin machinery prematurely.
- Assume any subsystem may eventually be replaced. Keep replaceable concerns
  behind interfaces and avoid vendor lock-in.
- Preserve provenance: carry source identity, derivation, and review history
  through each processing stage rather than reconstructing it later.
- Prefer deterministic algorithms over model- or LLM-based ones where a
  deterministic method is practical.

## Decision Framework

When multiple implementations are viable, choose in this order:

1. simplest
2. most maintainable
3. easiest to test
4. least coupled
5. most extensible

Choose clarity over cleverness. Readable code beats concise code.

---

# Coding Standards

Follow the conventions already established in the codebase. When no convention
exists:

- Use descriptive names and avoid unnecessary abbreviations.
- Keep functions and modules focused on one responsibility.
- Use the language's type system; avoid unsafe casts and untyped escape hatches.
- Prefer explicit control flow over clever or implicit behavior.
- Minimize mutable global state, singletons, and hidden side effects.
- Add comments only when they explain intent, constraints, or non-obvious logic.
- Validate inputs at system boundaries and report invalid states clearly.
- Do not swallow errors or return success-shaped fallbacks after failures.
- Reuse existing helpers and abstractions before adding new ones.

## Error Handling

- Fail loudly; never silently ignore an exception.
- Raise meaningful, specific exception types (`CalculatorValidationError`, `AssetVerificationError`).
- Include enough context in error messages to diagnose the failure without
  reproducing it.
- Report per-item failures and continue processing other items where the
  operation is batch-oriented; summarize failures in the final output.

## Performance

Do not optimize prematurely. Establish correctness, clarity, and interfaces
first, then profile and optimize measured bottlenecks. Measure; do not guess.

## Language- or Framework-Specific Rules

- **Python (`>=3.9`)**: Use `from __future__ import annotations`, `@dataclass(frozen=True)` for domain objects, explicit type annotations, and `logging` instead of `print()`.
- **HTML5 / CSS3 / JS**: Use semantic landmarks (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`), WCAG AA+ contrast, CSS custom properties (`:root` and `[data-theme="dark"]`), and zero external CDN runtime dependencies so the site runs 100% offline/locally.
- **Disallowed anti-patterns**: Do not hardcode single-tenant pitch copy (`TWU`, `Tennessee Wesleyan`, `Wilhelm`) in rendered output; do not use `mv` or `rm` commands outside the repository root.

---

# Dependencies

- Reuse installed dependencies before introducing new packages.
- Ask before adding a runtime dependency unless the user explicitly requested
  it.
- Use the repository's existing package manager (`uv`) and `pyproject.toml`.
- Before adding a dependency, ask: can the standard library solve this? Is it
  actively maintained? Does it simplify the architecture and reduce long-term
  complexity? If not, do not introduce it.
- Do not replace a library or framework without documenting the motivation and
  migration impact.
- Remove a dependency only after confirming that no supported code path uses it.

---

# Data, Security, and Privacy

- Never commit credentials, tokens, private keys, or sensitive data.
- Load configuration and secrets from the repository's approved mechanism (for
  example, an ignored `.env` read at runtime). Never hardcode hosts, usernames,
  passwords, API keys, or connection strings.
- Never print or log credentials, authorization payloads, or full connection
  strings, including into generated output files.
- Treat production data and external systems as read-only unless writes are an
  explicit project responsibility and the user has requested them.
- Never silently switch environments, accounts, or endpoints after a connection,
  authentication, or authorization failure. Report the error and stop.
- Human authentication, MFA, and consent remain human. Never bypass or automate
  around identity controls.
- Use synthetic or sanitized fixtures in tests.
- Apply least privilege to new integrations and deployment permissions; retain
  TLS verification.
- Keep vendor inputs, generated findings, run artifacts, and machine-local paths
  out of Git. Configure ignore rules before generating such artifacts (`dist/`, `tmp/`, `references/*.pdf`).
- Do not transmit source documents or private data to external services without
  explicit approval.

---

# Testing and Validation

Every behavior change should include or update the smallest useful automated
test. Cover applicable cases:

- expected behavior
- boundary and edge cases
- invalid input and failure behavior
- regression for the reported defect
- compatibility of public contracts

Favor unit tests over integration tests; keep integration tests deterministic
and avoid brittle snapshot tests. When a bug is found: write a failing test,
fix the bug, and keep the regression test.

Use the repository's existing validation tools. Run the narrowest relevant
tests, formatter, linter, type checker, and build first; expand validation only
when the change or initial results justify it.

Do not claim success without evidence. If validation cannot run, state exactly
what was not verified and why. Synthetic or fixture-based results are not
production acceptance; live acceptance requires explicit authorization and
independent reconciliation of counts, sizes, or hashes against the source.

Project validation commands:

```bash
# Format command: NOT CONFIGURED (Ruff is not installed in the offline local environment)
# Lint command: NOT CONFIGURED (Ruff is not installed in the offline local environment)
# Type-check command: NOT CONFIGURED (Pyright is not installed in the offline local environment)
# Bytecode & syntax check command (configured):
uv run python3 -m compileall -q src tests main.py
# Automated unit & integration test command (configured):
uv run python3 -m unittest discover -s tests -v
# Catalog & asset verification gate (configured):
uv run python3 main.py check
# Static build validation gate (configured):
uv run python3 main.py build
```

List every gate this repository actually has, and state explicitly which gates
are **not configured** rather than deleting the line or leaving it as an
unfilled placeholder. An agent must be able to tell the difference between a
gate that is missing and a gate that is merely undocumented. If a gate is not
configured, do not invent a command for it, and do not treat Definition of Done
as satisfied by a gate that does not exist.

> **Organization convention (not a requirement of this template):** Python
> projects here have standardized on `uv` with Ruff (format and lint), Pyright
> (types), and pytest. In this offline local environment, `uv` is active with
> Python's standard library `unittest` and `compileall` gates configured above.

---

# Documentation

- Keep documentation synchronized with behavior, configuration, and public
  interfaces.
- Update examples when the API or workflow changes.
- Record durable architectural decisions in the project's established location.
- Do not create planning or summary documents unless the user requests them or
  the repository requires them.
- Keep README usage honest about planned versus implemented behavior.
- Store feature plans in `docs/<feature-name>/` with a brief `README.md` that
  links each plan, its status, and the current feature contract. Read that
  README before planning or changing the feature; update it when plans are
  added or superseded. Preserve historical decisions while clearly labeling
  superseded behavior; the current contract remains authoritative.
- For every major development effort, create or update a concise completion
  report in `docs/completion-report.md` before declaring the work done.
  Include scope and key changes, commit references, validation commands and
  results, execution outcomes, limitations, and follow-up work. Reuse the
  effort's existing report rather than creating duplicates.
- Keep tracked reports sanitized: aggregate results only, with no private
  excerpts, sensitive identifiers, or machine-local paths. Keep detailed
  evidence in ignored output directories or outside the repository.
- Distinguish an operational artifact produced by the product from a development
  report about the product; do not conflate the two.

---

# Knowledge Reuse

Treat prior validated findings as repository knowledge. Before investigating,
querying an external system, or rediscovering structure:

1. Search existing documentation, findings, and prior work directories.
2. Reuse established relationships, keys, semantics, filters, validation
   methods, and derived datasets.
3. Investigate live only for information not already captured.

When an investigation validates a relationship, measures a cost, or uncovers a
trap, record it in the repository's durable location so it is not rediscovered.
Findings that stay in a one-off working directory will be lost.

Distinguish observed facts from inferred meaning. Do not present an inference as
an established fact.

---

# Observability and Operations

For operational code, expose enough information to diagnose failures without
reproducing them locally. As applicable, record:

- execution or request identifiers
- runtime and status
- meaningful counts or outcomes (`verified_assets`, `html_bytes`, `floors`, `archetypes`)
- validation failures and warnings
- deployment version or environment
- inputs, versions, and outputs sufficient to reproduce a run

Use structured logging and existing telemetry patterns; never use `print()` for
application behavior. Do not add noisy logs or expose sensitive data.

Do not equate partial success with complete coverage — report bounded or limited
results as bounded. Listing, discovery, and retrieval failures must remain
explicit; never silently substitute stale or cached results for a failed read.

---

# Development Workflow

```text
Create or update feature branch
        |
Implement an atomic change
        |
Run targeted validation
        |
Update related documentation
        |
Review the diff
        |
Commit locally
        |
Push and open or update the pull request only when requested
```

- Work on a feature or fix branch; do not commit directly to the default branch.
- Agree on the branch before implementation. Planning approval is not
  implementation approval.
- Branch from the current default branch unless the documented release workflow
  requires another base.
- Keep pull requests small enough to review as one coherent change; prefer small
  commits and frequent integration over long-lived branches.
- Do not mix unrelated cleanup or future work into the current change.
- Preserve user-authored changes already present in the working tree.
- After completing and validating requested changes, create focused local
  commits unless the user instructs otherwise. Push or publish a branch only
  when the user explicitly requests it; otherwise leave commits local.

---

# Git and Conventional Commits

When creating a commit, agents must use Conventional Commits 1.0.0. This is an
agent-session convention only; do not add commit hooks, CI enforcement, release
automation, or rewrite existing history unless explicitly requested.

Use this header format:

```text
<type>[optional scope][optional !]: <concise description>
```

Allowed types:

- `feat`: add a user- or business-facing capability
- `fix`: correct a defect
- `docs`: change documentation only
- `test`: add or correct tests without changing production behavior
- `refactor`: restructure code without changing intended behavior
- `ci`: change continuous integration configuration
- `chore`: perform repository maintenance not covered by another type
- `perf`: improve performance without changing intended behavior
- `build`: change dependencies, packaging, or the build system

Commit-message rules:

- Use lowercase types.
- Choose the type that best describes the commit's primary intent.
- Add a concise noun scope when it provides useful context, for example
  `feat(web): add interactive medical leasing platform`. Scopes are optional; do not maintain a
  fixed scope list unless the repository benefits from one.
- Write a specific, action-oriented description after the required colon and
  space.
- Do not use vague descriptions such as `updates`, `changes`, `fixes`, or
  `miscellaneous`.
- Keep logically inseparable implementation, tests, and directly related
  documentation in one atomic commit.
- Split independent changes into separate commits.
- Add a body when the motivation, constraints, or non-obvious implementation
  details will help future readers. Explain **why**, not merely **what**.
- Add issue references and other metadata as Git trailers when useful.
- Separate the header, body, and footers with blank lines.

For an intentional incompatible change to a published API, schema,
configuration contract, command-line interface, event format, or other
consumer-facing behavior:

- add `!` immediately before the colon
- add a `BREAKING CHANGE:` footer
- describe the impact and required migration

Example:

```text
feat(api)!: replace legacy account identifier

BREAKING CHANGE: API responses now expose `account_id` instead of `id`.
Update consumers to read `account_id` before deploying this version.
```

When a pull request contains clean, atomic commits, recommend rebase and merge
to retain a linear, searchable default-branch history. If the repository uses
squash merging instead, ensure the pull request title is a valid Conventional
Commit header.

---

# AI Development Guidelines

When acting as an AI software engineer:

1. Read the relevant code, tests, configuration, and documentation before
   changing behavior.
2. Search for reusable implementations before writing new code.
3. Extend existing abstractions rather than duplicating logic.
4. Form a falsifiable hypothesis and validate the smallest useful change.
5. Prefer precise changes over broad rewrites.
6. Do not modify unrelated code or revert changes you did not make.
7. Preserve backward compatibility unless the user approves a breaking change.
8. Make routine in-scope decisions independently; escalate only critical
   blockers or changes of scope. Ask before a significant product, architecture,
   dependency, or data-ownership decision.
9. Follow established repository patterns for errors, logging, tests, and
   configuration.
10. Update directly related tests and documentation with the implementation.
11. Verify the actual requested outcome, not merely a proxy such as compilation.
12. Report assumptions, validation performed, and any remaining risk clearly.
13. Produce maintainable, production-quality code rather than a prototype.

## Agent Working Style

- Be concise and execution-oriented.
- Do not repeatedly rediscover information already captured in the repository.
- Do not write a script when a direct command or query is sufficient, and do not
  generate large intermediate artifacts when the result can be computed directly.
- Prefer one well-designed operation over several redundant ones.
- Before an expensive, slow, or high-impact operation, briefly explain why it is
  necessary.
- Preserve reusable findings when finishing, so the next agent does not repeat
  the work.

---

# Human-in-the-Loop

Where the workflow requires human review or acceptance:

- Require explicit human acceptance of the exact artifact used downstream; never
  infer acceptance from a filename, timestamp, or directory name.
- Keep human-supplied decisions bound to the specific record and evidence they
  apply to, and retain the reviewer's basis alongside automated results.
- Support repeated review cycles and preserve the pre-review snapshot for
  comparison.
- Never convert an assumption or contextual inference into a confirmed,
  human-verified value.
- Block final output on unresolved required values; report optional gaps as
  warnings.

---

# Definition of Done

A change is complete when all applicable conditions are met:

- requested behavior is implemented
- relevant tests pass
- formatting, linting, type checks, and builds pass (where configured; unconfigured gates explicitly reported)
- errors and edge cases are handled
- public interfaces are reviewed and unnecessary complexity is removed
- directly related documentation is current
- a concise completion report is current for major development efforts (`docs/completion-report.md`)
- no secrets, private data, or unintended files are included
- the final diff contains no unrelated changes
- deployment or runtime behavior is verified when required
- known limitations and unverified checks are reported

---

# Project-Specific References

- Product & Property Briefing Source: `references/207 Elk Ave for TWU.pdf` (generalized in `src/elk_ave/catalog.py`)
- Architecture & Usage Documentation: `README.md`
- Completion Report: `docs/completion-report.md`
- Domain & Rendering Implementation: `src/elk_ave/`
- Automated Test Suite: `tests/test_elk_ave.py`
