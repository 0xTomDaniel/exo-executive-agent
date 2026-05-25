# Spec Index

Canonical specs in this repository describe durable Exo/personal-agent product
behavior and deployment contracts. Linear issues hold workflow state; this
directory holds the durable source of truth that implementers, reviewers, and
operators should read when changing the agent distribution.

## Domains

- [Hermes Personal Agent Distribution](./domains/hermes-personal-agent-distribution.md):
  shared Hermes profile-distribution, optional profile variants, multi-repo
  skill installation, one-container-per-agent deployment, remote SSH
  redeployability, storage-zone contracts, and v1 Telegram/runtime boundaries
  for Tom and Varela personal agents.
