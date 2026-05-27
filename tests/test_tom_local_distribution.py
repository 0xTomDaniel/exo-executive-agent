from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from exo_distribution.config import load_profile_config, schema_summary
from exo_distribution.render import render_hermes_config
from exo_distribution.smoke import run_fake_telegram_smoke


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "profiles/tom-local-dev/profile.toml"
SCHEMA = REPO_ROOT / "schemas/profile-config.schema.json"
TEMPLATE = REPO_ROOT / "profiles/tom-local-dev/hermes/config.yaml.template"
GENERATED = REPO_ROOT / "profiles/tom-local-dev/generated/config.yaml"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


class TomLocalDistributionTest(unittest.TestCase):
    def test_profile_validates_against_checked_in_contract(self) -> None:
        self.assertIn("Exo Hermes Profile Config", schema_summary(SCHEMA))
        config = load_profile_config(PROFILE)
        self.assertEqual(config.profile_id, "tom-local-dev")

    def test_rendered_hermes_config_matches_committed_example(self) -> None:
        config = load_profile_config(PROFILE)
        rendered = render_hermes_config(config, TEMPLATE)
        self.assertEqual(rendered, GENERATED.read_text(encoding="utf-8"))
        self.assertIn('token_env: "TELEGRAM_BOT_TOKEN"', rendered)
        self.assertNotIn("fake-token-not-live", rendered)

    def test_fake_telegram_smoke_replies_only_to_owner(self) -> None:
        config = load_profile_config(PROFILE)
        replies = run_fake_telegram_smoke(config, REPO_ROOT)
        self.assertEqual(
            replies,
            [
                {
                    "chat_id": "fake-tom-owner",
                    "text": "Tom local/dev Exo is loaded with fake Telegram and safe-core tools only.",
                }
            ],
        )

    def test_smoke_command_uses_no_live_credentials(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/smoke_tom_local.py"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('"profile": "tom-local-dev"', result.stdout)
        self.assertIn("fake Telegram", result.stdout)

    def test_env_example_is_secret_only_and_blank(self) -> None:
        content = ENV_EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("TELEGRAM_BOT_TOKEN=", content)
        self.assertIn("TELEGRAM_OWNER_ID=", content)
        self.assertIn("OPENAI_API_KEY=", content)
        for line in content.splitlines():
            self.assertFalse(line.startswith("VITE_"), line)
            if line.startswith(("TELEGRAM_BOT_TOKEN=", "TELEGRAM_OWNER_ID=", "OPENAI_API_KEY=")):
                self.assertTrue(line.endswith("="), line)


if __name__ == "__main__":
    unittest.main()
