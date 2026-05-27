# Repository Regression Suite

Run these commands before handing off changes that affect distribution
material, profile TOML, templates, validator logic, smoke behavior, or docs that
name supported local commands.

```bash
uv run python scripts/validate_profile.py
uv run python scripts/validate_profile.py --all
uv run python scripts/render_hermes_config.py
uv run python scripts/install_skills.py --profile tom-local-dev
uv run python scripts/render_compose.py
uv run python scripts/smoke_tom_local.py
uv run python -m unittest discover -s tests
```

Expected coverage:

- the Tom local/dev profile validates against the checked-in schema contract;
- Tom Daniel, Sebastian Varela, and Noah Ranch owner templates validate against
  the checked-in schema contract;
- the rendered Hermes config matches the committed generated example and
  contains no secret values;
- the skills manifest parses, selects only approved Tom profile skills, plans
  `/opt/data/skills` installs, and excludes unapproved private external-action
  fallback sources;
- the rendered Compose example declares one Hermes container per profile and
  rejects shared Hermes homes, Telegram token paths, logs, backups, and restart
  boundaries;
- fake Phase fixtures provide only minimal required secret bridge names;
- fake Telegram smoke replies to the owner-only text interaction and ignores a
  non-owner message;
- no live Telegram, model provider, Phase service, ESXi host, or private storage
  access is required.
- committed files do not include private runtime homes, logs, backups, sessions,
  personal files, Phase exports, or generated secret bridge values.
