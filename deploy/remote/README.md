# Remote Deploy Template

This directory contains the non-secret remote SSH deployment template for the
Hermes Exo distribution. It is safe to validate in CI or by Octo agents because
the default target is `deploy/remote/mock-target.toml` and the workflow emits a
dry-run plan instead of opening SSH sessions.

Live ESXi deployment evidence is Human Review/HITL through EMB-276 unless a
later issue explicitly grants remote access and the required Phase secrets.

## Dry Run And Mock Validation

Render the deploy plan without live SSH, Phase, Telegram, model, or cloud
credentials:

```bash
uv run python scripts/remote_deploy.py --config deploy/remote/mock-target.toml
```

Include fixture-backed health/status/log failure reporting:

```bash
uv run python scripts/remote_deploy.py --config deploy/remote/mock-target.toml --mock-check
```

Use `--strict` only when a caller wants fixture failures to produce a non-zero
exit code. The committed fake health fixture intentionally includes a critical
storage-safety problem so failure reporting stays covered without live services.

The plan covers:

- prerequisite checks for Docker, Compose, Python, uv, Phase CLI, rsync,
  deploy root, and runtime root;
- TOML profile validation through `scripts/validate_profile.py --all`;
- Hermes config and Compose rendering;
- copying distribution-owned material with secret, runtime, Phase export, log,
  backup, session, memory, and personal-file exclusions;
- per-profile runtime directory creation;
- profile TOML install/update into each instance config boundary;
- Phase-backed secret bridge materialization;
- profile skill install/sync into each instance's skills directory;
- Docker Compose pull, start, restart, status, health, and logs commands;
- backup-boundary discovery and restore/redeploy references.

## Target TOML

`mock-target.toml` documents the expected remote target shape:

- `[target]` names only non-secret SSH and path metadata.
- `[ssh]` records operator SSH options.
- `[phase]` records the materialization strategy and the instance-local bridge
  directory pattern.
- `[health]` points at a fake local fixture for mock checks.

Committed target templates must keep `target.mode = "mock"` and
`phase.live_secret_policy = "human-review-only"`. Real VM hostnames, private
paths, Phase service tokens, exported secrets, generated env files, and runtime
state stay outside git.

## Phase Secret Materialization

Profile TOML files own the non-secret Phase metadata:

- Phase app: `exo-executive-agent`
- Phase environment: profile-specific, currently `prod` for owner templates
- Phase path: one per personal-agent instance
- Secret names: profile-specific Telegram bot token, Telegram owner id, and
  model provider key names

The dry-run plan runs `deploy/remote/materialize-secret-bridge.sh` from the
copied deploy root under `phase run`. That script writes only instance-local
bridge files under
`${EXO_RUNTIME_ROOT}/<profile>/secret-bridge/`:

- `telegram-bot-token`, for providers that require a token file;
- `provider.env`, a smallest-available dotenv-compatible bridge containing only
  the profile's owner id and model key when a provider requires env ingestion.

The materializer fails closed if Phase does not inject every required secret
name for the profile. Generated bridges are ignored runtime artifacts. Compose
connects `provider.env` through the profile-local `env_file`; other local
ingestion should use Phase runtime injection, Vite built-in env loading for
Vite surfaces, or Node built-in DotEnv support for Node services/CLIs. Do not
add broad committed env catalogs or raw secret values.

## Instance Boundaries

The generated multi-owner Compose template runs one container per
personal-agent instance. Every profile has separate runtime directories for:

- Hermes home;
- workspace;
- secret bridge;
- skills;
- writable vault;
- read-only personal files;
- logs;
- backup boundary;
- placeholder read-only mounts.

No active Hermes gateway containers may share a Hermes home, Telegram token
path, log boundary, backup boundary, skills directory, or restart/container
boundary.

## Operator Update And Redeploy

For a fresh VM or update, the operator flow is:

1. Review the dry-run plan.
2. Ensure Docker Compose, Python, uv, rsync, SSH, and Phase CLI are available.
3. Validate profiles and render templates locally.
4. Copy distribution material to the deploy root with the plan's rsync command.
5. Create runtime directories and install/update profile TOML into each
   profile config boundary.
6. Materialize Phase secret bridges.
7. Install or sync approved skills for each profile.
8. Run Compose pull and `up -d --remove-orphans`.
9. Inspect status, health, and logs.

To redeploy after a distribution update, repeat the same plan. Compose restart
boundaries are per service/container, so one profile can be restarted without
sharing active Hermes home state with another.

## Backup And Restore

Backup tooling should treat each profile's `backup-boundary` as the unit of
restore. At template level, a restore onto a fresh VM should:

1. Recreate the deploy root from git.
2. Recreate `${EXO_RUNTIME_ROOT}/<profile>/` directories.
3. Restore only that profile's Hermes home, writable vault, and required
   runtime config into the matching profile boundary.
4. Re-run Phase bridge materialization instead of restoring old secret exports.
5. Re-run skill install/sync from the pinned manifest.
6. Start only the restored profile's Compose service first, then inspect health
   and logs before starting the rest.
