# Hermes Personal Agent Distribution

## Intended Behavior

`exo-executive-agent` defines a reusable Hermes-based personal executive
assistant distribution. The distribution can be instantiated as separate
private Hermes agents, initially for Tom Daniel and Sebastian Varela.

The repository owns non-secret, redeployable source material: Hermes profile
distribution manifests, identity and config templates, optional profile
variants, portable skills, skill source manifests, cron and MCP templates,
Docker Compose templates, remote deployment scripts, health checks, and setup
documentation.

The repository does not own live instance state. Credentials, private memories,
sessions, logs, backups, mounted personal files, private machine-specific
paths, and instantiated per-user Hermes homes stay outside git.

## Domain Concepts

**Personal-agent instance**: One running Hermes agent for one owner. Each
instance has its own Hermes data directory, Telegram identity/token path,
memory, sessions, logs, storage mounts, backup boundary, and lifecycle.

**Distribution-owned material**: Source-controlled material that should be
updated through git, such as manifests, templates, shared skills, optional
profile variants, scripts, and docs.

**User-owned material**: Runtime-local or private material that must not be
committed, such as `.env`, credentials, Hermes memories, sessions, logs,
state databases, backups, mounted personal files, and local paths.

**Optional profile variant**: A reusable Hermes profile template or
distribution variant with a documented role, required env vars, enabled tools,
and privacy boundaries. A variant is not a live profile directory.

**Skills source manifest**: A source-controlled manifest listing approved skill
sources across repositories. Entries include repo, path, ref, intended
profiles, collision policy, and source-of-truth expectations.

**Skill installer/package manager**: The mechanism that installs approved
skills into each personal-agent instance, preferably into that instance's
`/opt/data/skills` directory, without treating writable repo-mounted skill
directories as the production source of truth.

**Three-zone storage model**: The storage contract for each instance:
per-user Hermes runtime state, agent-owned writable Markdown memory/vault
area, and broader personal files mounted read-only by default.

**Remote SSH deployment**: The preferred operator deployment path. Scripts
should be able to prepare or update the VM, copy or render non-secret
templates, install or update profiles and skills, start or restart Docker
Compose services, and run health checks over SSH.

## Rules and Invariants

- Hermes Agent is the v1 runtime.
- `exo-executive-agent` is the shared git-owned distribution/setup repository.
- Durable changes to distribution-owned material must be git changes committed
  to this repository.
- Runtime Hermes instances must not silently mutate repo-owned skills,
  profiles, templates, or deployment artifacts as the durable source of truth.
- v1 runs one Docker container per personal-agent instance.
- Active Hermes gateway containers must not share one Hermes home or one
  persistent data directory.
- Each instance must have distinct Telegram token/identity paths, runtime data,
  logs, restart boundaries, and backup boundaries.
- Deployment templates must support redeploying from scratch on a fresh VM,
  not only updating an already-working host.
- Production skill installation should copy, sync, or install approved skills
  into each instance's `/opt/data/skills`.
- Hermes `skills.external_dirs` may be used as a dev/operator convenience, but
  writable repo-owned external skill directories are not the production
  source-of-truth path.
- The default distribution enables only safe/core tools.
- External-action tools that can send email, book calendar events, spend
  money, trade, post publicly, mutate broad cloud storage, or call sensitive
  provider APIs are opt-in per instance.
- v1 user-facing runtime is owner-only Telegram text chat.
- CLI, Docker, and SSH commands are operator setup, debug, and recovery
  surfaces, not equal first-class v1 user surfaces.
- Voice, file/photo/document ingestion, OCR/PDF processing, arbitrary Telegram
  attachments, group chat, and multi-principal memory boundaries are out of v1
  scope.
- v1 memory uses Hermes built-in memory/session/context behavior plus Markdown
  vault/files as the shared durable memory baseline.
- External memory providers such as Honcho are optional future or per-instance
  adapters and do not block v1.

## Interfaces/Contracts

### Distribution Interface

The distribution should expose Hermes-compatible profile material such as
`distribution.yaml`, `SOUL.md`, `config.yaml`, `skills/`, `cron/`, optional
`mcp.json`, and `.env.example` files. The final layout may include profile
variant subdirectories if the selected Hermes-compatible installer path
requires it.

Each variant must document:

- intended role;
- required and optional env vars;
- enabled safe/core tools;
- optional external-action tools, if any;
- privacy boundaries;
- install/update command;
- whether it is a template, an installable distribution, or both.

### Deployment Interface

Deployment templates and scripts should support remote SSH operation against
the ESXi guest VM. The operator path should include:

- prerequisite checks;
- directory layout creation;
- rendering or copying non-secret templates;
- profile install or update;
- skill install or sync;
- Docker Compose start/restart;
- health and status checks;
- log inspection;
- backup/restore procedure references.

Secrets and private runtime state are materialized outside git.

### Skills Interface

The repository should include a skills source manifest. A required spike must
choose the best skill installer/package-manager approach by comparing Hermes
native skill install/update behavior, agentskills.io/Skills Hub compatibility,
manifest formats, pinned refs, collision handling, profile-specific installs,
and promotion of runtime-created skills back to git.

Production instances receive approved skills in their local Hermes skill
directory. Runtime-local skill edits are not authoritative unless intentionally
promoted through a git commit.

### Storage Interface

The parent PRD defines the storage contract; EMB-317 chooses the provider and
topology. Each instance should declare mounts for:

- per-user Hermes runtime state;
- agent-owned writable Markdown memory/vault area;
- general personal files mounted read-only by default.

Any write access to broader personal files must be narrowed to explicit folders
or workflows. Sync health and backup/recovery behavior must be visible to the
operator and to the agent where relevant.

### Telegram Runtime Interface

V1 supports owner-only Telegram text chat for each user instance. Tom and
Varela should have separate owner identity/token paths. Automated tests use
fake or mocked Telegram. A manual live Telegram smoke test with a real token
and owner account is required during Human Review before the deployed runtime
is considered usable.

## Edge Cases

- A skill name exists in multiple source repositories.
- A runtime-created skill should become durable distribution material.
- A repo-owned skill directory is accidentally mounted writable through
  `skills.external_dirs`.
- The ESXi guest is reachable by SSH but lacks Docker, Compose, or required
  filesystem mounts.
- One personal-agent instance starts while another is unhealthy.
- Telegram tokens are swapped, duplicated, or assigned to the wrong owner.
- General personal files are accidentally mounted read-write.
- Storage sync is stale, unavailable, or in conflict.
- The distribution updates while an instance has local user-owned config.
- Restore from backup is required on a fresh VM.

## Constraints

- Do not commit credentials, live env files, private memories, sessions, logs,
  state databases, backups, mounted personal files, or private machine paths.
- Do not depend on concrete ESXi details in the parent PRD; EMB-276 gathers
  and validates those facts as a HITL spike.
- Do not choose the storage provider in this parent spec; EMB-317 owns that
  provider/topology decision.
- Do not rely on writable external skill directories as a production
  source-of-truth boundary.
- Do not require real Telegram, model, cloud storage, or ESXi access in
  automated CI.
- Do not enable external-action tools by default in the shared distribution.

## Non-Goals

- Building a full web admin dashboard for v1.
- Supporting Telegram voice, media, documents, OCR, PDFs, arbitrary
  attachments, group chats, or multi-user memory boundaries in v1.
- Selecting the final cloud filesystem provider in EMB-261.
- Committing Tom's or Varela's private runtime profile data.
- Requiring Honcho or another external memory provider for v1.
- Using the old Pi package/adapter acceptance criteria as executable v1 scope.

## Open Questions About System Behavior

- Which skill installer/package-manager approach should become the durable
  profile skill installation contract?
- Which storage provider/topology will EMB-317 select?
- Which ESXi guest OS, resources, network exposure, and backup/restore details
  will EMB-276 validate?
- Which optional profile variants should ship first?
- Which exact env var names should be standardized for per-instance Telegram,
  model/provider, storage, and optional external-action credentials?
- Which implementation choices require target-repo ADRs after spikes resolve?

## Decision Log Or Links To ADRs

- 2026-05-25: Use Hermes Agent as the v1 runtime and `exo-executive-agent` as
  the shared distribution/setup repo.
- 2026-05-25: Model Tom and Varela as separate personal-agent instances, not
  one shared runtime.
- 2026-05-25: Prefer one Docker container and one persistent Hermes data
  directory per personal-agent instance.
- 2026-05-25: Prefer remote SSH deployment scripts that can run the full
  deployment/update/health-check flow.
- 2026-05-25: Define the three-zone storage contract in EMB-261 and leave
  provider/topology selection to EMB-317.
- 2026-05-25: Treat the skill installer/package-manager choice as a required
  child spike.
- 2026-05-25: No ADR yet. Create target-repo ADRs later only when a
  hard-to-reverse or surprising implementation choice is selected.

## References To Source Issues

- EMB-261: PRD: Rework Exo as Hermes-based personal executive assistant agent
- EMB-276: Set up ESXi VM for personal Hermes agents
- EMB-317: Select privacy-preserving filesystem for personal agents
