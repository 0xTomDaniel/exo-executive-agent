# exo-executive-agent

Exo is a Hermes-first personal executive assistant distribution. This
repository owns non-secret distribution/setup material that can be installed as
private Hermes instances. It does not own live user runtime state.

The first runnable slice is `tom-local-dev`: a Tom-oriented local/dev profile
that validates TOML config, renders a Hermes-native config example, and proves a
mocked owner-only Telegram text loop without live Telegram, model credentials,
Phase access, ESXi access, or private storage.

## Repository Boundary

Distribution-owned paths in git:

- `distribution.yaml`: Hermes-compatible distribution manifest shape;
- `SOUL.md`: identity and behavioral direction for Exo;
- `profiles/tom-local-dev/`: non-secret Tom local/dev profile template,
  fixtures, and rendered Hermes config example;
- `schemas/profile-config.schema.json`: checked-in config contract;
- `exo_distribution/` and `scripts/`: validator, renderer, and smoke tooling;
- `tests/`: fake/no-credentials regression coverage;
- `spec/`: durable product and regression docs.

User-owned/runtime paths outside git:

- real Hermes homes, `/opt/data` instance directories, memories, sessions,
  logs, backups, state databases, and mounted personal files;
- credentials, Phase service tokens, exported secrets, and generated secret
  bridge files;
- machine-specific storage mount paths and private owner data.

## Config and Secrets

Non-secret config lives in TOML:

```bash
uv run python scripts/validate_profile.py profiles/tom-local-dev/profile.toml
```

Render the committed Hermes config example from TOML:

```bash
uv run python scripts/render_hermes_config.py
```

Secrets are Phase-backed and documented only as a blank bridge inventory in
`.env.example`. The example intentionally contains only required secret keys
for the local/dev runtime path: Telegram token, Telegram owner id, and model API
key. Ordinary profile, storage, tool, and deployment config belongs in TOML,
not `.env`.

Production/operator runs should prefer Phase injection, such as:

```bash
phase run --app exo-executive-agent --env dev --path /tom/local -- <command>
```

If a local dotenv-compatible bridge is required by a provider, keep it
generated, instance-local, ignored by git, and limited to the smallest required
secret interface. Use native Phase, Vite, or Node env ingestion where relevant;
do not add `dotenv` by default and do not use `VITE_` prefixes for secrets.

## Local Smoke

Run the no-credentials Tom local/dev smoke:

```bash
uv run python scripts/smoke_tom_local.py
```

Run the regression suite:

```bash
uv run python -m unittest discover -s tests
```

The smoke uses:

- fake Telegram updates from
  `profiles/tom-local-dev/fixtures/fake_telegram_owner_text.json`;
- fake Phase/minimal secret bridge values from
  `profiles/tom-local-dev/fixtures/fake_phase_minimal.json`;
- local storage fixtures under `profiles/tom-local-dev/fixtures/storage`;
- fake model mode, with no live provider calls.

The expected behavior is one reply to the owner chat and no reply to a
non-owner chat.

## Tools and External Actions

The default Tom local/dev profile enables only safe/core tools:

- `memory.read`;
- `memory.write_markdown`;
- `files.read_workspace`;
- `telegram.reply_text`.

External-action tools that can send email, book calendar events, spend money,
trade, post publicly, mutate broad cloud storage, or call sensitive provider
APIs are disabled by default. They require explicit per-instance opt-in,
Phase-managed secrets, and approval/audit documentation.

## Human Review Live Smoke

Automated checks do not use live Telegram. Human Review remains responsible for
one manual live Telegram smoke with a real bot token and owner account before a
deployed personal-agent runtime is considered usable.
