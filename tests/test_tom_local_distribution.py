from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from exo_distribution.config import load_profile_config, schema_summary
from exo_distribution.render import render_hermes_config
from exo_distribution.skills import (
    install_planned_skills,
    load_skills_manifest,
    plan_skill_install,
)
from exo_distribution.smoke import run_fake_telegram_smoke


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE = REPO_ROOT / "profiles/tom-local-dev/profile.toml"
SCHEMA = REPO_ROOT / "schemas/profile-config.schema.json"
TEMPLATE = REPO_ROOT / "profiles/tom-local-dev/hermes/config.yaml.template"
GENERATED = REPO_ROOT / "profiles/tom-local-dev/generated/config.yaml"
ENV_EXAMPLE = REPO_ROOT / ".env.example"
SKILLS_MANIFEST = REPO_ROOT / "skills/sources.toml"


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
                    "text": (
                        "Tom local/dev Exo is loaded with fake Telegram "
                        "and safe-core tools only."
                    ),
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

    def test_skills_manifest_records_pinned_multi_repo_sources(self) -> None:
        manifest = load_skills_manifest(SKILLS_MANIFEST, REPO_ROOT)
        self.assertEqual(manifest.default_install_root, "/opt/data/skills")
        sources_by_id = {source.id: source for source in manifest.sources}
        self.assertEqual(
            sources_by_id["exo.daily_brief"].repo,
            "github.com/0xTomDaniel/exo-executive-agent",
        )
        self.assertEqual(
            sources_by_id["hermes.file_brief"].repo,
            "github.com/hermes-fixtures/core-skills",
        )
        self.assertFalse(sources_by_id["private.calendar_audit"].approved)
        for source in manifest.sources:
            self.assertNotIn(source.ref, {"HEAD", "main", "master", "latest"})
            self.assertTrue(source.install_destination.startswith("/opt/data/skills/"))

    def test_profile_specific_skill_plan_excludes_unapproved_private_source(self) -> None:
        manifest = load_skills_manifest(SKILLS_MANIFEST, REPO_ROOT)
        plans = plan_skill_install(
            manifest,
            "tom-local-dev",
            REPO_ROOT,
            install_root=Path("/tmp/exo-skills"),
        )
        self.assertEqual(
            [plan.source.id for plan in plans],
            ["exo.daily_brief", "hermes.file_brief"],
        )
        self.assertEqual(
            [str(plan.runtime_destination) for plan in plans],
            ["/opt/data/skills/exo-daily-brief", "/opt/data/skills/hermes-file-brief"],
        )
        self.assertEqual(plan_skill_install(manifest, "unknown-profile", REPO_ROOT), [])

    def test_skill_installer_installs_updates_and_refuses_unmanaged_collisions(self) -> None:
        manifest = load_skills_manifest(SKILLS_MANIFEST, REPO_ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            install_root = Path(tmp) / "skills"
            plans = plan_skill_install(
                manifest,
                "tom-local-dev",
                REPO_ROOT,
                install_root=install_root,
            )
            self.assertEqual([plan.action for plan in plans], ["install", "install"])
            install_planned_skills(plans, manifest)
            self.assertTrue((install_root / "exo-daily-brief/SKILL.md").is_file())
            metadata = install_root / "exo-daily-brief/.exo-skill-source.json"
            self.assertIn('"source_id": "exo.daily_brief"', metadata.read_text(encoding="utf-8"))

            up_to_date = plan_skill_install(
                manifest,
                "tom-local-dev",
                REPO_ROOT,
                install_root=install_root,
            )
            self.assertEqual([plan.action for plan in up_to_date], ["up-to-date", "up-to-date"])

            updated_manifest_path = Path(tmp) / "sources-updated.toml"
            updated_manifest_path.write_text(
                SKILLS_MANIFEST.read_text(encoding="utf-8").replace(
                    "fixture-2026-05-27-core-v1",
                    "fixture-2026-05-27-core-v2",
                    1,
                ),
                encoding="utf-8",
            )
            updated_manifest = load_skills_manifest(updated_manifest_path, REPO_ROOT)
            update_plan = plan_skill_install(
                updated_manifest,
                "tom-local-dev",
                REPO_ROOT,
                install_root=install_root,
            )
            self.assertEqual([plan.action for plan in update_plan], ["replace", "up-to-date"])

        with tempfile.TemporaryDirectory() as tmp:
            install_root = Path(tmp) / "skills"
            unmanaged = install_root / "exo-daily-brief"
            unmanaged.mkdir(parents=True)
            (unmanaged / "SKILL.md").write_text("# Runtime-created skill\n", encoding="utf-8")
            collision_plan = plan_skill_install(
                manifest,
                "tom-local-dev",
                REPO_ROOT,
                install_root=install_root,
            )
            self.assertEqual(collision_plan[0].action, "collision")
            with self.assertRaisesRegex(Exception, "existing skill has no Exo source metadata"):
                install_planned_skills(collision_plan, manifest)

    def test_skill_installer_refuses_repo_owned_install_roots(self) -> None:
        manifest = load_skills_manifest(SKILLS_MANIFEST, REPO_ROOT)
        with self.assertRaisesRegex(Exception, "refusing to install skills into repo-owned path"):
            plan_skill_install(
                manifest,
                "tom-local-dev",
                REPO_ROOT,
                install_root=REPO_ROOT / "skills",
            )

    def test_install_skills_command_can_apply_to_fixture_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/install_skills.py",
                    "--profile",
                    "tom-local-dev",
                    "--install-root",
                    str(Path(tmp) / "skills"),
                    "--apply",
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn('"mode": "apply"', result.stdout)
            self.assertIn(
                '"runtime_destination": "/opt/data/skills/exo-daily-brief"',
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
