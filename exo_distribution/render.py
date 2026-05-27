from __future__ import annotations

from pathlib import Path

from exo_distribution.config import ProfileConfig


def render_hermes_config(config: ProfileConfig, template_path: Path) -> str:
    output = template_path.read_text(encoding="utf-8")
    replacements = _flatten(config.data)
    replacements["tools.safe_core_yaml"] = _safe_core_yaml(config)
    replacements["tools.external_actions.enabled"] = _yaml_bool(
        bool(config.data["tools"]["external_actions"]["enabled"])  # type: ignore[index]
    )
    for key, value in replacements.items():
        output = output.replace("{{ " + key + " }}", value)
    return output


def _flatten(data: object, prefix: str = "") -> dict[str, str]:
    values: dict[str, str] = {}
    if isinstance(data, dict):
        for key, value in data.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            values.update(_flatten(value, next_prefix))
    elif isinstance(data, bool):
        values[prefix] = _yaml_bool(data)
    elif isinstance(data, (str, int, float)):
        values[prefix] = str(data)
    return values


def _safe_core_yaml(config: ProfileConfig) -> str:
    tools = config.data["tools"]["safe_core"]  # type: ignore[index]
    return "\n".join(f'    - "{tool["name"]}"' for tool in tools)  # type: ignore[index]


def _yaml_bool(value: bool) -> str:
    return "true" if value else "false"
