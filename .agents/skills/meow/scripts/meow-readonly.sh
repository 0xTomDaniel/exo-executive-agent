#!/usr/bin/env bash
set -euo pipefail

SERVICE="com.exocortex.meow.hamilton"
EMAIL="${MEOW_EXO_EMAIL:-tom@hamiltonspice.com}"

if [[ $# -lt 1 ]]; then
  printf 'Usage: %s <read-only-meow-command> [options...]\n' "$0" >&2
  exit 2
fi

COMMAND="$1"
shift

# Technical read-only gate. Do not expand this list merely to satisfy a prompt;
# create a separately reviewed action path when Tom explicitly authorizes a
# state-changing capability.
case "$COMMAND" in
  get-my-entity|get-next-step|get-onboarding-status|get-info-requests|list-bank-accounts|get-bank-account|get-account-balances|list-account-payment-networks|search-tax-forms|get-tax-form|list-account-transactions|get-usdc-transaction|get-wire-transfer|get-ach-transfer|list-scheduled-ach-transfers|list-contacts|get-contact|list-products|get-product|list-invoicing-customers|get-invoicing-customer|list-payment-method-types|list-invoices|get-invoice|list-invoice-line-items|get-invoice-line-item|list-collection-accounts|list-bills|get-bill|list-security-policies|get-approval|list-cards|list-card-transactions|get-card-insights|get-card|get-card-details|validate-routing-number)
    ;;
  *)
    printf 'Blocked: %s is not in Exo\x27s Meow read-only allowlist. Use a separately reviewed action flow with explicit confirmation.\n' "$COMMAND" >&2
    exit 3
    ;;
esac

API_KEY="$(security find-generic-password -a "$EMAIL" -s "$SERVICE" -w 2>/dev/null)" || {
  printf 'No Hamilton Meow credential found in macOS Keychain. Run authenticate-macos.sh first.\n' >&2
  exit 1
}

meow "$COMMAND" "$@" --api-key "$API_KEY"
STATUS=$?
unset API_KEY
exit "$STATUS"
