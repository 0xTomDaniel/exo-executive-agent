from __future__ import annotations

import json
import shlex
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from exo_distribution.config import ProfileConfig, ValidationError


PlanMode = Literal["dry-run", "mock-check"]

RUNTIME_RSYNC_EXCLUDES = (
    ".git",
    ".venv",
    ".env*",
    ".phase",
    "phase-export*",
    "runtime",
    "data",
    "secret-bridge",
    "provider.env",
    "hermes-home",
    "memories",
    "sessions",
    "logs",
    "backups",
    "personal-files",
)


@dataclass(frozen=True)
class DeployTarget:
    path: Path
    name: str
    host: str
    user: str
    port: int
    deploy_root: str
    runtime_root: str
    compose_project: str
    mode: str
    connect_timeout_seconds: int
    strict_host_key_checking: str
    phase_materialization: str
    dotenv_bridge_dir: str
    live_secret_policy: str
    health_fixture: str

    @property
    def ssh_destination(self) -> str:
        return f"{self.user}@{self.host}"


def load_deploy_target(path: Path) -> DeployTarget:
    with path.open("rb") as config_file:
        data = tomllib.load(config_file)

    _require_exact_keys(data, ("target", "ssh", "phase", "health"), "root")
    target = _table(data, "target")
    ssh = _table(data, "ssh")
    phase = _table(data, "phase")
    health = _table(data, "health")

    _require_exact_keys(
        target,
        (
            "name",
            "host",
            "user",
            "port",
            "deploy_root",
            "runtime_root",
            "compose_project",
            "mode",
        ),
        "target",
    )
    _require_exact_keys(
        ssh,
        ("connect_timeout_seconds", "strict_host_key_checking"),
        "ssh",
    )
    _require_exact_keys(
        phase,
        ("materialization", "dotenv_bridge_dir", "live_secret_policy"),
        "phase",
    )
    _require_exact_keys(health, ("fixture",), "health")

    _require_non_empty_strings(
        target,
        ("name", "host", "user", "deploy_root", "runtime_root", "compose_project", "mode"),
        "target",
    )
    _require_non_empty_strings(
        phase,
        ("materialization", "dotenv_bridge_dir", "live_secret_policy"),
        "phase",
    )
    _require_non_empty_strings(health, ("fixture",), "health")
    port = _positive_int(target["port"], "target.port")
    timeout = _positive_int(ssh["connect_timeout_seconds"], "ssh.connect_timeout_seconds")
    strict_host_key_checking = _non_empty_string(
        ssh["strict_host_key_checking"],
        "ssh.strict_host_key_checking",
    )

    if target["mode"] != "mock":
        raise ValidationError("target.mode must be mock for committed deploy target templates")
    if phase["materialization"] != "operator-phase-cli":
        raise ValidationError("phase.materialization must be operator-phase-cli")
    if phase["live_secret_policy"] != "human-review-only":
        raise ValidationError("phase.live_secret_policy must be human-review-only")
    if not str(target["deploy_root"]).startswith("/"):
        raise ValidationError("target.deploy_root must be an absolute remote path")
    if not str(target["runtime_root"]).startswith("/"):
        raise ValidationError("target.runtime_root must be an absolute remote path")
    if "${EXO_RUNTIME_ROOT}" not in str(phase["dotenv_bridge_dir"]):
        raise ValidationError("phase.dotenv_bridge_dir must stay under EXO_RUNTIME_ROOT")

    return DeployTarget(
        path=path,
        name=str(target["name"]),
        host=str(target["host"]),
        user=str(target["user"]),
        port=port,
        deploy_root=str(target["deploy_root"]),
        runtime_root=str(target["runtime_root"]),
        compose_project=str(target["compose_project"]),
        mode=str(target["mode"]),
        connect_timeout_seconds=timeout,
        strict_host_key_checking=strict_host_key_checking,
        phase_materialization=str(phase["materialization"]),
        dotenv_bridge_dir=str(phase["dotenv_bridge_dir"]),
        live_secret_policy=str(phase["live_secret_policy"]),
        health_fixture=str(health["fixture"]),
    )


def build_deploy_plan(
    target: DeployTarget,
    profiles: list[ProfileConfig],
    *,
    mode: PlanMode = "dry-run",
    compose_output: Path = Path("deploy/compose/generated/hermes-multi-owner.compose.yaml"),
) -> dict[str, object]:
    installable = [
        config
        for config in profiles
        if config.data["profile"]["intended_profile"]  # type: ignore[index]
        == "installable-template"
    ]
    if not installable:
        raise ValidationError(
            "remote deployment requires at least one installable-template profile"
        )

    profile_ids = [config.profile_id for config in installable]
    compose_remote = f"{target.deploy_root}/{compose_output}"
    ssh_prefix = _ssh_prefix(target)
    compose = _compose_prefix(target, compose_remote)

    steps: list[dict[str, object]] = [
        {
            "name": "prerequisite-checks",
            "kind": "remote",
            "commands": [
                _ssh(target, "command -v docker"),
                _ssh(target, "docker compose version"),
                _ssh(target, "command -v python3"),
                _ssh(target, "command -v uv"),
                _ssh(target, "command -v phase"),
                _ssh(target, f"mkdir -p {target.deploy_root} {target.runtime_root}"),
                _ssh(target, f"test -w {target.deploy_root} && test -w {target.runtime_root}"),
            ],
        },
        {
            "name": "validate-toml-configs",
            "kind": "local",
            "commands": ["uv run python scripts/validate_profile.py --all"],
        },
        {
            "name": "render-compose-and-profile-templates",
            "kind": "local",
            "commands": [
                "uv run python scripts/render_hermes_config.py",
                "uv run python scripts/render_compose.py",
            ],
            "outputs": [str(compose_output)],
        },
        {
            "name": "copy-distribution-material",
            "kind": "remote-copy",
            "commands": [
                (
                    "rsync -az --delete "
                    f"-e {shlex.quote(_rsync_ssh(target))} "
                    f"{_rsync_exclude_args()} ./ "
                    f"{target.ssh_destination}:{target.deploy_root}/"
                ),
            ],
        },
        {
            "name": "create-instance-runtime-boundaries",
            "kind": "remote",
            "commands": [
                _ssh(target, "mkdir -p " + " ".join(_runtime_dirs(target, config)))
                for config in installable
            ],
        },
        {
            "name": "install-or-update-profile-material",
            "kind": "remote",
            "commands": [
                _ssh(
                    target,
                    (
                        f"install -d -m 0750 {target.runtime_root}/{config.profile_id}/config && "
                        "install -m 0640 "
                        f"{target.deploy_root}/profiles/{config.profile_id}/profile.toml "
                        f"{target.runtime_root}/{config.profile_id}/config/profile.toml"
                    ),
                )
                for config in installable
            ],
        },
        {
            "name": "materialize-phase-secret-bridges",
            "kind": "operator-phase",
            "commands": [
                _secret_bridge_command(target, config)
                for config in installable
            ],
            "notes": [
                "Plan records only Phase app/environment/path metadata and secret names.",
                "Raw secrets, Phase service tokens, and generated bridge files stay outside git.",
            ],
        },
        {
            "name": "install-or-sync-profile-skills",
            "kind": "remote",
            "commands": [
                _ssh(
                    target,
                    (
                        f"cd {target.deploy_root} && "
                        "uv run python scripts/install_skills.py "
                        f"--profile {config.profile_id} "
                        f"--install-root {target.runtime_root}/{config.profile_id}/skills --apply"
                    ),
                )
                for config in installable
            ],
        },
        {
            "name": "compose-start-or-restart",
            "kind": "remote",
            "commands": [
                _ssh(target, f"cd {target.deploy_root} && {compose} pull"),
                _ssh(target, f"cd {target.deploy_root} && {compose} up -d --remove-orphans"),
            ],
        },
        {
            "name": "health-checks",
            "kind": "remote",
            "commands": [
                _ssh(target, f"{compose} ps --format json"),
                *[
                    _ssh(
                        target,
                        (
                            "docker inspect "
                            "--format '{{.Name}} {{.State.Status}} "
                            "{{if .State.Health}}{{.State.Health.Status}}"
                            "{{else}}no-healthcheck{{end}}' "
                            f"{config.container_name}"
                        ),
                    )
                    for config in installable
                ],
            ],
        },
        {
            "name": "status-and-log-inspection",
            "kind": "remote",
            "commands": [
                _ssh(target, f"{compose} ps"),
                _ssh(target, f"{compose} logs --tail 100 --timestamps"),
            ],
        },
        {
            "name": "backup-restore-and-redeploy-reference",
            "kind": "operator-docs",
            "commands": [
                _ssh(
                    target,
                    f"find {target.runtime_root} -maxdepth 2 -type d -name backup-boundary",
                ),
                _ssh(target, f"cd {target.deploy_root} && {compose} restart"),
            ],
        },
    ]

    plan: dict[str, object] = {
        "ok": True,
        "mode": mode,
        "target": {
            "name": target.name,
            "host": target.host,
            "user": target.user,
            "port": target.port,
            "deploy_root": target.deploy_root,
            "runtime_root": target.runtime_root,
            "compose_project": target.compose_project,
        },
        "ssh": ssh_prefix,
        "profiles": profile_ids,
        "secret_bridges": [_secret_bridge_metadata(target, config) for config in installable],
        "steps": steps,
        "live_esxi_boundary": (
            "Live ESXi execution is Human Review/HITL through EMB-276 unless a later "
            "issue provisions remote access and required secrets."
        ),
    }
    if mode == "mock-check":
        plan["mock_health"] = load_mock_health(target.health_fixture)
    return plan


def load_mock_health(fixture_path: str) -> dict[str, object]:
    fixture = Path(fixture_path)
    with fixture.open("r", encoding="utf-8") as fixture_file:
        payload = json.load(fixture_file)
    problems = payload.get("problems")
    if not isinstance(problems, list):
        raise ValidationError("mock health fixture must contain a problems list")
    failures = [
        problem
        for problem in problems
        if isinstance(problem, dict) and problem.get("severity") in {"critical", "error"}
    ]
    return {
        "ok": not failures,
        "fixture": fixture_path,
        "problem_count": len(problems),
        "failures": failures,
        "status_commands_verified": ["health-checks", "status-and-log-inspection"],
    }


def _secret_bridge_metadata(target: DeployTarget, config: ProfileConfig) -> dict[str, object]:
    phase = config.data["phase"]  # type: ignore[index]
    telegram = config.data["telegram"]  # type: ignore[index]
    model = config.data["model"]  # type: ignore[index]
    return {
        "profile_id": config.profile_id,
        "phase": {
            "app": phase["app"],
            "environment": phase["environment"],
            "path": phase["path"],
        },
        "secret_names": [
            telegram["bot_token_secret"],
            telegram["owner_id_secret"],
            model["api_key_secret"],
        ],
        "token_file": str(telegram["token_path"]),
        "dotenv_bridge": (
            target.dotenv_bridge_dir.replace("${EXO_RUNTIME_ROOT}", target.runtime_root).replace(
                "{profile_id}",
                config.profile_id,
            )
            + "/provider.env"
        ),
        "dotenv_keys": [telegram["owner_id_secret"], model["api_key_secret"]],
        "git_policy": (
            "generated bridge artifacts are instance-local under runtime_root and ignored"
        ),
    }


def _secret_bridge_command(target: DeployTarget, config: ProfileConfig) -> str:
    bridge = _secret_bridge_metadata(target, config)
    phase = bridge["phase"]
    telegram = config.data["telegram"]  # type: ignore[index]
    model = config.data["model"]  # type: ignore[index]
    return _ssh(
        target,
        (
            f"cd {target.deploy_root} && "
            f"EXO_RUNTIME_ROOT={target.runtime_root} "
            f"install -d -m 0700 {target.runtime_root}/{config.profile_id}/secret-bridge && "
            f"EXO_RUNTIME_ROOT={target.runtime_root} "
            "phase run "
            f"--app {phase['app']} --env {phase['environment']} --path {phase['path']} "
            "-- ./deploy/remote/materialize-secret-bridge.sh "
            f"{config.profile_id} "
            f"{telegram['bot_token_secret']} "
            f"{telegram['owner_id_secret']} "
            f"{model['api_key_secret']}"
        ),
    )


def _compose_prefix(target: DeployTarget, compose_remote: str) -> str:
    return (
        f"EXO_RUNTIME_ROOT={target.runtime_root} "
        f"docker compose -p {target.compose_project} -f {compose_remote}"
    )


def _runtime_dirs(target: DeployTarget, config: ProfileConfig) -> list[str]:
    profile_root = f"{target.runtime_root}/{config.profile_id}"
    return [
        f"{profile_root}/hermes-home",
        f"{profile_root}/workspace",
        f"{profile_root}/secret-bridge",
        f"{profile_root}/vault",
        f"{profile_root}/personal-files",
        f"{profile_root}/skills",
        f"{profile_root}/config",
        f"{profile_root}/log-boundary",
        f"{profile_root}/backup-boundary",
        f"{profile_root}/placeholders/personal-documents",
    ]


def _ssh_prefix(target: DeployTarget) -> str:
    return (
        f"ssh -p {target.port} "
        f"-o ConnectTimeout={target.connect_timeout_seconds} "
        f"-o StrictHostKeyChecking={target.strict_host_key_checking} "
        f"{target.ssh_destination}"
    )


def _ssh(target: DeployTarget, command: str) -> str:
    return f"{_ssh_prefix(target)} -- sh -lc {shlex.quote(command)}"


def _rsync_ssh(target: DeployTarget) -> str:
    return (
        f"ssh -p {target.port} "
        f"-o ConnectTimeout={target.connect_timeout_seconds} "
        f"-o StrictHostKeyChecking={target.strict_host_key_checking}"
    )


def _rsync_exclude_args() -> str:
    return " ".join(
        f"--exclude {shlex.quote(pattern)}"
        for pattern in RUNTIME_RSYNC_EXCLUDES
    )


def _table(data: dict[str, object], key: str) -> dict[str, object]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValidationError(f"{key} must be a table")
    return value


def _require_exact_keys(data: dict[str, object], expected: tuple[str, ...], label: str) -> None:
    actual = set(data)
    expected_set = set(expected)
    missing = sorted(expected_set - actual)
    extra = sorted(actual - expected_set)
    if missing or extra:
        raise ValidationError(f"{label} keys mismatch; missing={missing}, extra={extra}")


def _require_non_empty_strings(
    data: dict[str, object],
    keys: tuple[str, ...],
    label: str,
) -> None:
    for key in keys:
        _non_empty_string(data.get(key), f"{label}.{key}")


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value


def _positive_int(value: object, field: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field} must be a positive integer")
    return value
