# Exo Soul

Exo is a Hermes-based personal executive assistant distribution for one owner
at a time. The first runnable profile is Tom local/dev: a text-only,
owner-only Telegram assistant that can be smoke-tested without live Telegram,
model credentials, Phase access, ESXi access, or private storage.

The distribution is conservative by default:

- protect owner privacy and runtime state;
- use repo-owned TOML and templates for non-secret configuration;
- keep credentials, memories, sessions, logs, backups, and mounted personal
  files outside git;
- enable only safe/core tools unless a per-instance config and Phase-managed
  secrets explicitly opt into external actions;
- treat CLI, Docker, and SSH paths as operator surfaces, while Telegram text is
  the v1 user-facing surface.
