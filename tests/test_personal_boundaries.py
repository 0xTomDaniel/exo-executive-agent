"""Accepted single-preferences-skill policy, exercised through distribution interfaces."""

import tempfile
import unittest
from pathlib import Path

from exo_distribution.skills import install_planned_skills, load_skills_manifest, plan_skill_install

ROOT = Path(__file__).resolve().parents[1]


class PersonalBoundaryTests(unittest.TestCase):
    def test_team_planning_is_a_module_of_the_only_tom_preferences_skill(self):
        manifest = load_skills_manifest(ROOT / "skills/sources.toml", ROOT)
        self.assertNotIn("ember-weekly-planning", {s.name for s in manifest.sources})
        with tempfile.TemporaryDirectory() as temp:
            plans = plan_skill_install(manifest, "tom-personal-agent", ROOT, Path(temp))
            install_planned_skills(plans, manifest)
            tom = next(
                p.actual_destination for p in plans if p.source.name == "tom-operating-style"
            )
            self.assertTrue((tom / "modules/ember-weekly-planning/guide.md").is_file())
            self.assertEqual(list(tom.rglob("SKILL.md")), [tom / "SKILL.md"])
            self.assertTrue(
                (tom / "modules/ember-weekly-planning/references/icp-qualification.md").is_file()
            )
            self.assertIn("modules/ember-weekly-planning/guide.md", (tom / "SKILL.md").read_text())
            for owner in ("sebastian-personal-agent", "noah-personal-agent"):
                self.assertNotIn(
                    "tom-operating-style",
                    {
                        p.source.name
                        for p in plan_skill_install(manifest, owner, ROOT, Path(temp) / owner)
                    },
                )

    def test_meow_missing_owner_context_never_attempts_credential_access(self):
        import os
        import subprocess
        import sys

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spy = root / "security"
            spy.write_text('#!/bin/sh\n: > "' + str(root / "accessed") + '"\nexit 1\n')
            spy.chmod(0o755)
            env = {
                **os.environ,
                "PATH": temp,
                "MEOW_EXO_EMAIL": "",
                "MEOW_EXO_KEYCHAIN_SERVICE": "",
            }
            for script, args in [
                ("safe_read.py", ["list-bank-accounts"]),
                ("authenticate_macos.py", []),
            ]:
                result = subprocess.run(
                    [sys.executable, str(ROOT / ".agents/skills/meow/scripts" / script), *args],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertIn("owner_context_required", result.stderr)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / "accessed").exists())

    def test_shared_guidance_has_no_known_owner_identity_leaks(self):
        import re

        paths = [ROOT / "AGENTS.md", ROOT / "SOUL.md"]
        paths += list((ROOT / "deploy/voice").rglob("*.md"))
        paths += list((ROOT / "skills").rglob("*.md"))
        paths += [
            p
            for p in (ROOT / ".agents/skills").rglob("*")
            if p.suffix in {".md", ".py", ".sh", ".cjs", ".json"}
            and "tom-operating-style" not in p.parts
        ]
        personal = re.compile(
            r"\b(?:Tom|Sebastian|Varela|Noah|Hamilton|AirCollar|Ember)\b|hamiltonspice|Projects/Arbitrum",
            re.I,
        )
        failures = []
        for path in paths:
            content = path.read_text()
            # Exact routing identifiers are permitted, not arbitrary lines.
            for identifier in ("tom-operating-style", "tom-personal-agent"):
                content = content.replace(identifier, "")
            if personal.search(content):
                failures.append(str(path.relative_to(ROOT)))
        self.assertEqual(failures, [], "Known personal identity in shared guidance")

    def test_old_standalone_team_skill_requires_preserving_migration(self):
        from exo_distribution.config import ValidationError

        manifest = load_skills_manifest(ROOT / "skills/sources.toml", ROOT)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "ember-weekly-planning"
            old.mkdir()
            note = old / "SKILL.md"
            note.write_text("Runtime customization to preserve.\n")
            with self.assertRaisesRegex(ValidationError, "retired standalone"):
                plan_skill_install(manifest, "tom-personal-agent", ROOT, root)
            self.assertEqual(note.read_text(), "Runtime customization to preserve.\n")
