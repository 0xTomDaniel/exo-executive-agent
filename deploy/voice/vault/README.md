# Direct vault voice deployment

This replaces the Hermes-connected sidecar for an instance that should execute
in a real Syncthing vault. The Codex backing agent reads and edits the vault
itself; there is no runs proxy, exoctl binary, Hermes API credential, shared
Hermes network namespace or messaging bridge in this deployment.

The older `../sidecar` recipe and native-integration documents describe the
historical Hermes-connected architecture. They remain useful for that separate
mode, but are not the instructions for this deployment.

## Runtime layout

Keep source here and private configuration, login state, sessions and backups
outside the repository and outside the synced vault. Render `compose.yaml` with
these operator-selected bootstrap values using `docker compose config`:

- `VOICE_RUNTIME_ROOT`: private state/workspace directory.
- `VOICE_VAULT_PATH`: existing absolute Syncthing vault path, mounted at the same
  path inside the container and used as the container working directory.
- `VOICE_UID` and `VOICE_GID`: vault owner's IDs. State ownership must match.
- `VOICE_TIMEZONE`: owner's timezone for dated memory operations.

The host's approved `/usr/local/bin/uv` executable is mounted read-only; confirm
it executes in the image. Python and ripgrep are installed in the image.
The image seeds Codex 0.153.1 with the existing checked installer; retained
state supplies the installed version, which may be newer. Preserve that state
and verify the running version instead of claiming a fresh seed matches it.

## Backing-agent model

[config.toml.example](config.toml.example) records the backing-agent defaults:
`gpt-6-astra` with `model_reasoning_effort = "low"`. Merge these top-level
settings into the private `state/config.toml`; do not replace the whole file
and lose its prompts or trusted projects. These settings select the Codex
backing agent, not the realtime speech model.

After changing an existing deployment's settings, restart its Codex app-server
daemon and start a fresh voice conversation. Phone/thread overrides or resumed
threads may retain another model; inspect the actual turn context to confirm.
The live deployment's model catalog and configuration parsing accepted these
settings; that alone does not prove the next phone turn uses them.

## Adoption from the existing sidecar

1. Build the new image and validate rendered Compose configuration before the
   outage. Keep a private, restorable copy of the existing Compose and prompts.
2. Stop the voice container and its runs proxy, leaving the Hermes service
   itself alone. Copy the stopped state into the new runtime root, preserving
   login, remote-control identity, sessions and database consistency. Keep the
   original private runtime as rollback material.
3. Set the new state's ownership to the vault UID/GID. Render
   `HOST-AGENTS.md`, replacing `__VAULT_PATH__` with the selected path, into
   `state/AGENTS.md`. Use it as the bootstrap instruction in `workspace/AGENTS.md`
   too: phone-created/resumed conversations may supply their own CWD. They must
   still load the canonical vault instructions before substantive work.
4. Replace the old `developer_instructions` with a short instruction to use the
   actual vault and its AGENTS.md. Replace
   `experimental_realtime_ws_backend_prompt` with `REALTIME-PROMPT.md`. Preserve
   unrelated settings and history. Trust the canonical vault path. Parse the
   resulting TOML before startup, including the backing-agent defaults from
   `config.toml.example`. Add links under `state/skills` to the vault's
   actual `.agents/skills` packages so discovery works outside the vault too.
5. Do not copy the old workspace's `bin/exoctl` or persistent Hermes
   instructions into the new workspace. Retain their old versions only in the
   private rollback copy. No Hermes secret is needed by the new deployment.
6. Recreate voice with the existing Compose project identity and remove the
   stopped proxy container. Check restart policy, login, daemon version and
   remote-control connection. Do not run both old and new daemons against the
   same identity or state.
7. Verify vault read/write as the runtime UID, native prompt assembly from the
   vault and a phone-style alternate CWD, skill discovery and the note metadata
   validator. Use a temporary file for a two-way Syncthing check and remove it
   afterward. A phone voice round trip remains a separate acceptance check.

## Instruction migration

The vault's AGENTS.md owns identity, memory, planning and evidence policy. Keep
voice-specific pacing, spoken summaries, truthful delivery/cancellation claims,
steering and interruption handling in the host/realtime adapter. The old Hermes
run IDs, ownership transfer, event paging, API approvals, Telegram sender and
no-vault-access statements do not apply and must not migrate.

The Debian host adapter explicitly accounts for the absence of the Obsidian
desktop CLI. Filesystem edits and metadata validation are available; application
Base queries, automatic link maintenance and UI readback are not established.
Do not silently weaken the shared vault's Mac workflow or claim those checks
passed. Existing conversation history is retained, but start a fresh voice
conversation after switching to avoid reusing stale per-thread instructions.

## Rollback

Stop the new voice daemon before switching. Restore the old source/settings
and user mapping only through an explicit operator decision: this restores the
retired Hermes connection. Keep any sessions, saved vault work and action
receipts produced since the switch; do not reset state to an old snapshot and
blindly retry external actions.

## Validation of the direct-vault migration

The image build, rendered Compose validation, shell syntax check and 112
repository unit tests passed. Live checks established retained ChatGPT login,
Codex 0.153.4 daemon operation, connected remote control, canonical vault CWD,
native instruction/skill assembly from both vault and alternate workspace,
metadata validation and bidirectional Syncthing read/write. The temporary sync
file was removed. Phone audio and a new voice conversation require the final
interactive acceptance check; server checks do not establish audible delivery.
