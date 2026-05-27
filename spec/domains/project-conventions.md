# Project Conventions

This repository is a Hermes profile-distribution/setup repository. Conventions
below apply to repo-owned distribution material and local validation tooling.

## Paths

- Distribution-owned material lives in git under `distribution.yaml`, `SOUL.md`,
  `profiles/`, `schemas/`, `exo_distribution/`, `scripts/`, `tests/`, and
  `spec/`.
- User-owned/runtime material must stay outside git. This includes Hermes
  homes, memories, sessions, logs, backups, state databases, mounted personal
  files, Phase service tokens, generated secret bridge files, and
  machine-specific paths.
- Profile directories in this repo are templates or examples, not live Hermes
  homes.

## Config

- Non-secret config is TOML and must validate through
  `uv run python scripts/validate_profile.py`.
- Hermes-native config output is rendered from TOML and template material with
  `uv run python scripts/render_hermes_config.py`.
- Unknown or misplaced TOML fields should fail validation before deployment or
  smoke execution.

## Secrets

- `.env.example` is secret-only, blank, and limited to required provider bridge
  variables.
- Ordinary config must not be added to `.env.example`.
- Real env files, Phase exports, service tokens, and generated secret bridges
  are ignored runtime artifacts.
- Prefer Phase injection and native runtime env ingestion. Do not add `dotenv`
  by default.
- Do not use `VITE_` prefixes for secrets.

## Runtime Defaults

- Local/dev automated validation uses fake Telegram, fake model mode, fake Phase
  fixtures, and local storage fixtures.
- The default profile enables safe/core tools only.
- External-action tools require explicit per-instance opt-in, Phase-managed
  secrets, and approval/audit documentation.
