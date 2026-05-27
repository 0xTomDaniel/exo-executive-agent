#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exo_distribution.config import load_profile_config, schema_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Exo Hermes profile TOML file.")
    parser.add_argument(
        "profile",
        nargs="?",
        default="profiles/tom-local-dev/profile.toml",
        help="Profile TOML path to validate.",
    )
    parser.add_argument(
        "--schema",
        default="schemas/profile-config.schema.json",
        help="Checked-in schema contract path.",
    )
    args = parser.parse_args()

    schema = schema_summary(Path(args.schema))
    config = load_profile_config(Path(args.profile))
    print(f"validated {config.profile_id} with {schema}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
