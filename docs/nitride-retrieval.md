# Headless reminder retrieval

The direct-vault Voice deployment now ships Node 22.23.2 and Nitride pinned to
`EmberAGI/nitride-cli` commit `7ffaf4109efde8f3fca75e4840d8860104000c25`.
See the [deployment recipe](../deploy/voice/vault/README.md#pinned-nitride-retrieval)
and [host Adapter](../deploy/voice/vault/HOST-AGENTS.md#reminder-scan-route).
This is independent of the Hermes profile skill installer.

## Ownership and behavior

Nitride owns interpretation of its documented read-only Base subset. Exo's
host Adapter owns concrete vault paths, source/view selection and runtime
invocation. The planning rhythm owns surfacing and coverage reporting. The
saved Bases own the current predicates; this integration does not change them.

The daily reminder scan executes the task fall-through view and all-note
attention view using the same live date and owner timezone. Preserve each
source membership and deduplicate identical paths for a combined count.
Different paths remain separate records even when content shows one obligation.
A reminder need not be a task. Source errors remain incomplete coverage, never
empty results or permission to substitute yesterday's scan.

The task/all-note terminal-state exclusions currently differ. Preserve and
report that difference until the owner resolves it. Linked-week/sprint
traversal remains unsupported; query explicit supported views instead of the
Base's default first view, and retain any required unsupported view as open
coverage. A reminder-only scan does not complete the broader steering workflow.

## Validation — September 7, 2026

- Before implementation, the prior image failed the public runtime command
  check with `node: not found`.
- The new image built successfully and verified the pinned Nitride archive's
  SHA-256. Its bundled executable matched the upstream artifact byte-for-byte.
- All 71 upstream conformance cases plus package failure checks passed in a
  disposable Debian container using Node 22.23.2, with networking disabled and
  read-only input mounts. These native recordings establish a bounded subset.
- Exo's 128 repository tests, shell syntax and rendered Compose validation passed.
- Both actual daily reminder queries succeeded against a read-only vault mount.
  Per-source membership, overlap and combined path count were checked. Personal
  results and runtime evidence are private and are not source fixtures.
- The deployed Voice container exposes `node`, `nitride`, and the pinned skill
  through Codex discovery. Retained Codex 0.153.4 daemon state and remote-control
  enablement survived recreation. Sessions/model settings were not reset.
- A fresh Astra/low acceptance turn in a disposable instance of the same image,
  using the installed instructions and actual vault mounted read-only, selected
  Nitride, inspected the saved definitions, ran both current queries, read
  selected context, and reported matching overlap/counts and remaining limits.
  No private notes were changed. This is model execution evidence, not just an
  instruction walkthrough or deterministic test.

The first model test requested Codex's `read-only` sandbox inside the container;
its shell failed because the host disallowed unprivileged namespaces. It
correctly reported unknown counts and incomplete coverage. The successful test
used the container's existing isolation with a read-only vault mount instead.
Production sandbox settings were not changed.

## Remaining acceptance and scope

The model test was a fresh CLI backing turn, not a phone-originated realtime
audio turn. Resumed phone threads may retain stale instructions or model
overrides; fresh phone acceptance remains outstanding. Full planning coverage
still needs the linked-period views and resolution of status policy. Non-Markdown
membership and additional Base coercions beyond Nitride's recordings remain
outside the compatibility claim. No npm publication or full Obsidian CLI
replacement is required for this deployed reminder route.
