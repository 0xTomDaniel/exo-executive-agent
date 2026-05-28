#!/usr/bin/env sh
set -eu

profile_id="${1:?profile id is required}"
bot_token_name="${2:?bot token secret name is required}"
owner_id_name="${3:?owner id secret name is required}"
model_api_key_name="${4:?model api key secret name is required}"
runtime_root="${EXO_RUNTIME_ROOT:?EXO_RUNTIME_ROOT is required}"
bridge_dir="${runtime_root}/${profile_id}/secret-bridge"

umask 077
mkdir -p "${bridge_dir}"

# This script is intentionally a template. Operators run it under `phase run`
# so profile-specific variables are provided by Phase at process start and
# never by git.
bot_token="$(printenv "${bot_token_name}" || true)"
owner_id="$(printenv "${owner_id_name}" || true)"
model_api_key="$(printenv "${model_api_key_name}" || true)"

if [ -n "${bot_token}" ]; then
  printf '%s' "${bot_token}" > "${bridge_dir}/telegram-bot-token"
fi

provider_env="${bridge_dir}/provider.env"
: > "${provider_env}"
if [ -n "${owner_id}" ]; then
  printf '%s=%s\n' "${owner_id_name}" "${owner_id}" >> "${provider_env}"
fi
if [ -n "${model_api_key}" ]; then
  printf '%s=%s\n' "${model_api_key_name}" "${model_api_key}" >> "${provider_env}"
fi

chmod 0600 "${bridge_dir}/telegram-bot-token" 2>/dev/null || true
chmod 0600 "${provider_env}"
