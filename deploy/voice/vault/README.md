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
desktop CLI. Filesystem edits, metadata validation and Nitride's supported
headless Base queries are available; automatic link maintenance and UI readback
are not established.
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

## Pinned Nitride retrieval

The image now includes Node 22.23.2 and the portable Nitride skill from
`0xTomDaniel/nitride-cli` commit `0c33c7adb2f034d20ffeb60b825170c0fdf39018`.
The Dockerfile verifies the source archive SHA-256 and installs the bundled
executable as `nitride`; there is no npm install at runtime. Startup exposes
`/opt/nitride` through the retained Codex state's `skills/nitride` link, refusing
an existing conflicting skill rather than overwriting it. This direct-vault
image integration does not activate the separate Hermes profile installer.

Build the new image before recreating Voice. Preserve its existing Compose
project, mounts, UID/GID, timezone, login, model settings and sessions. Update
only the image reference in the rendered private Compose to
`exo-codex-vault-voice:0.153.1-nitride-d20fb50`; back up and install the rendered
`HOST-AGENTS.md` in both documented bootstrap locations. Deploy the updated
`planning-rhythm-os/references/resurfacing.md` after checking the current copy
for owner changes. Also reconcile the shared repository `AGENTS.md` tool-selection row/policy and
the Obsidian skill overview/native-workflow routing into the corresponding vault
files. Back up both files, compare against the previous deployed content, and
preserve owner additions; neither the image build nor entrypoint installs those
shared instructions. Verify all four deployed instruction surfaces against the
intended targeted changes. Do not replace the entire vault instruction/skill tree.

The host Adapter owns concrete Nitride invocations and source membership.
Status-filter differences are preserved pending owner resolution. Saved Bases
remain authoritative and are not copied into a new task database. The pinned version supports the linked-week/sprint views. Other unsupported
views remain incomplete coverage; this deployment does not make every planning
view executable. Metadata/query errors must be reported,
not bypassed through stale scans or weakened filters.

Validate the built image without credentials first: `node --version`,
`nitride --version`, and the upstream isolated package suite against synthetic
fixtures. Then query the two actual daily reminder views read-only and inspect
errors/counts without publishing personal note contents. After recreation,
verify the versions, skill link, daemon/remote-control health and a fresh
Astra/low backing-agent scan. A CLI/model check does not prove a phone audio
round trip or that a resumed phone thread has refreshed its instructions.

Rollback to the prior image and backed-up adapter if startup fails. Remove only
the image-owned Nitride discovery link when rolling back to an image without
`/opt/nitride`; retain all sessions and saved vault work.
