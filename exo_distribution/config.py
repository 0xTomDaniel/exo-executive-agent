from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict


class ValidationError(ValueError):
    """Raised when a profile TOML file violates the Exo distribution contract."""


class ToolEntry(TypedDict):
    name: str
    reason: str


class ExternalActions(TypedDict):
    enabled: bool
    allow: list[str]
    policy: str


@dataclass(frozen=True)
class ProfileConfig:
    path: Path
    data: dict[str, object]

    @property
    def profile_id(self) -> str:
        return _table(self.data, "profile")["id"]

    @property
    def expected_reply(self) -> str:
        return _table(self.data, "smoke")["expected_reply"]


REQUIRED_TOP_LEVEL = (
    "profile",
    "hermes",
    "telegram",
    "model",
    "phase",
    "storage",
    "tools",
    "smoke",
)
SECRET_NAME = re.compile(r"^[A-Z][A-Z0-9_]*$")
FORBIDDEN_RUNTIME_FRAGMENTS = (
    "/Users/",
    "/home/",
    "/Volumes/",
    "/mnt/",
    "secrets",
    "credentials",
    "sessions",
    "logs",
    "backups",
)
SAFE_TOOL_PREFIXES = ("memory.", "files.", "telegram.reply_text")


def load_profile_config(path: Path) -> ProfileConfig:
    with path.open("rb") as config_file:
        data = tomllib.load(config_file)
    config = ProfileConfig(path=path, data=data)
    validate_profile_config(config)
    return config


def validate_profile_config(config: ProfileConfig) -> None:
    data = config.data
    _require_exact_keys(data, REQUIRED_TOP_LEVEL, "root")

    profile = _table(data, "profile")
    _require_exact_keys(profile, ("id", "owner_name", "mode", "timezone"), "profile")
    _require_non_empty_strings(profile, ("id", "owner_name", "mode", "timezone"), "profile")

    hermes = _table(data, "hermes")
    _require_exact_keys(hermes, ("runtime", "home", "workspace", "skills_dir"), "hermes")
    _require_non_empty_strings(hermes, ("runtime", "home", "workspace", "skills_dir"), "hermes")
    if hermes["skills_dir"] != "/opt/data/skills":
        raise ValidationError("hermes.skills_dir must install production skills into /opt/data/skills")

    telegram = _table(data, "telegram")
    _require_exact_keys(
        telegram,
        ("mode", "owner_id_secret", "bot_token_secret", "owner_only", "text_only"),
        "telegram",
    )
    if telegram["mode"] != "fake":
        raise ValidationError("tom local/dev profile must use fake Telegram mode")
    if telegram["owner_only"] is not True or telegram["text_only"] is not True:
        raise ValidationError("telegram must be owner-only and text-only for v1 local smoke")
    _validate_secret_name(telegram["owner_id_secret"], "telegram.owner_id_secret")
    _validate_secret_name(telegram["bot_token_secret"], "telegram.bot_token_secret")

    model = _table(data, "model")
    _require_exact_keys(model, ("mode", "provider", "api_key_secret"), "model")
    if model["mode"] != "fake":
        raise ValidationError("tom local/dev profile must use fake model mode")
    _validate_secret_name(model["api_key_secret"], "model.api_key_secret")

    phase = _table(data, "phase")
    _require_exact_keys(phase, ("app", "environment", "path"), "phase")
    _require_non_empty_strings(phase, ("app", "environment", "path"), "phase")
    if not str(phase["path"]).startswith("/"):
        raise ValidationError("phase.path must be an absolute Phase path")

    storage = _table(data, "storage")
    _require_exact_keys(storage, ("runtime", "vault", "personal_files"), "storage")
    _validate_storage_table(_table(storage, "runtime"), "runtime", required_access=None)
    _validate_storage_table(_table(storage, "vault"), "vault", required_access="read-write")
    _validate_storage_table(
        _table(storage, "personal_files"),
        "personal_files",
        required_access="read-only",
    )

    tools = _table(data, "tools")
    _require_exact_keys(tools, ("safe_core", "external_actions"), "tools")
    _validate_safe_core_tools(tools["safe_core"])
    external_actions = _table(tools, "external_actions")
    _require_exact_keys(external_actions, ("enabled", "allow", "policy"), "tools.external_actions")
    if external_actions["enabled"] is not False or external_actions["allow"] != []:
        raise ValidationError("external-action tools must be disabled by default")

    smoke = _table(data, "smoke")
    _require_exact_keys(
        smoke,
        ("telegram_fixture", "phase_fixture", "storage_fixture_root", "expected_reply"),
        "smoke",
    )
    _require_non_empty_strings(
        smoke,
        ("telegram_fixture", "phase_fixture", "storage_fixture_root", "expected_reply"),
        "smoke",
    )


def schema_summary(schema_path: Path) -> str:
    with schema_path.open("r", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)
    required = schema.get("required", [])
    if not isinstance(required, list) or sorted(required) != sorted(REQUIRED_TOP_LEVEL):
        raise ValidationError("schema required keys do not match validator top-level contract")
    return f"{schema.get('title', 'profile config')} ({schema.get('$schema', 'unknown schema')})"


def _validate_storage_table(
    table: dict[str, object],
    name: Literal["runtime", "vault", "personal_files"],
    required_access: str | None,
) -> None:
    required = ("kind", "path", "git_owned") if required_access is None else (
        "kind",
        "path",
        "access",
        "git_owned",
    )
    _require_exact_keys(table, required, f"storage.{name}")
    _require_non_empty_strings(table, ("kind", "path"), f"storage.{name}")
    if table["git_owned"] is not False:
        raise ValidationError(f"storage.{name}.git_owned must be false")
    path = str(table["path"])
    if "${EXO_RUNTIME_ROOT}" not in path:
        raise ValidationError(f"storage.{name}.path must be rooted under EXO_RUNTIME_ROOT")
    for fragment in FORBIDDEN_RUNTIME_FRAGMENTS:
        if fragment in path:
            raise ValidationError(f"storage.{name}.path contains private/runtime fragment {fragment}")
    if required_access is not None and table["access"] != required_access:
        raise ValidationError(f"storage.{name}.access must be {required_access}")


def _validate_safe_core_tools(value: object) -> None:
    if not isinstance(value, list) or not value:
        raise ValidationError("tools.safe_core must be a non-empty list")
    names: set[str] = set()
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise ValidationError(f"tools.safe_core[{index}] must be a table")
        _require_exact_keys(entry, ("name", "reason"), f"tools.safe_core[{index}]")
        _require_non_empty_strings(entry, ("name", "reason"), f"tools.safe_core[{index}]")
        name = str(entry["name"])
        if name in names:
            raise ValidationError(f"duplicate safe tool {name}")
        names.add(name)
        if not name.startswith(SAFE_TOOL_PREFIXES):
            raise ValidationError(f"safe/core tool {name} is not in the approved default set")


def _validate_secret_name(value: object, field: str) -> None:
    if not isinstance(value, str) or SECRET_NAME.fullmatch(value) is None:
        raise ValidationError(f"{field} must name an uppercase secret env bridge variable")
    if value.startswith("VITE_"):
        raise ValidationError(f"{field} must not use the client-exposed VITE_ prefix")


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
        if not isinstance(data.get(key), str) or not str(data[key]).strip():
            raise ValidationError(f"{label}.{key} must be a non-empty string")
