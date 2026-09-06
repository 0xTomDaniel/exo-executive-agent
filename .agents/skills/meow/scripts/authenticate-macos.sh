#!/usr/bin/env bash
set -euo pipefail

EMAIL="${1:-tom@hamiltonspice.com}"
SERVICE="com.exocortex.meow.hamilton"
STATUS_FILE="${TMPDIR:-/tmp}/meow-exo-auth-status"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/meow-exo-auth.XXXXXX")"
chmod 700 "$TMP"
trap 'rm -rf "$TMP"' EXIT
umask 077

printf 'waiting_for_code\n' > "$STATUS_FILE"

CODE="$(osascript <<'APPLESCRIPT'
set response to display dialog "Enter the newest 6-digit Meow API-key verification code sent to tom@hamiltonspice.com. It will be used locally and will not be written to chat or the vault." default answer "" with title "Connect Exo to Meow" with hidden answer buttons {"Cancel", "Connect"} default button "Connect"
return text returned of response
APPLESCRIPT
)" || {
  printf 'cancelled\n' > "$STATUS_FILE"
  exit 1
}

if ! [[ "$CODE" =~ ^[0-9]{6}$ ]]; then
  printf 'invalid_code_format\n' > "$STATUS_FILE"
  exit 1
fi

# Existing Meow accounts use request-verification-code followed directly by
# issue-onboarding-key. Do not run verify-email first; that path is for a new,
# not-yet-verified email and can reject an existing-account code as expired.
meow issue-onboarding-key --email "$EMAIL" --verification-code "$CODE" --output json > "$TMP/key.json" 2>/dev/null || true

if ! API_KEY="$(python3 - "$TMP/key.json" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1]))
except (OSError, json.JSONDecodeError):
    raise SystemExit(1)

def find(obj):
    if isinstance(obj, dict):
        value = obj.get("api_key")
        if isinstance(value, str) and value:
            return value
        for value in obj.values():
            found = find(value)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find(value)
            if found:
                return found
    return None

key = find(data)
if not key:
    raise SystemExit(1)
print(key)
PY
)"; then
  printf 'authentication_failed_code_rejected_or_expired\n' > "$STATUS_FILE"
  exit 1
fi

security add-generic-password -U -a "$EMAIL" -s "$SERVICE" -w "$API_KEY" >/dev/null

if meow get-my-entity --api-key "$API_KEY" --output json > "$TMP/entity.json" 2>/dev/null && python3 -m json.tool "$TMP/entity.json" >/dev/null 2>&1; then
  printf 'connected_entity_read_verified\n' > "$STATUS_FILE"
else
  printf 'key_stored_entity_read_not_verified\n' > "$STATUS_FILE"
fi

unset CODE API_KEY
