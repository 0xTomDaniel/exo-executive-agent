# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""Read-only pre/post-write metadata check. Exit 1 for invalid or unreadable notes."""

import argparse
import json
from pathlib import Path

from note_metadata import MetadataError, parse_frontmatter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    checked, invalid = 0, []
    for source in args.paths:
        paths = (
            sorted(
                p
                for p in source.rglob("*.md")
                if not any(part.startswith(".") for part in p.relative_to(source).parts)
            )
            if source.is_dir()
            else [source]
        )
        for path in paths:
            checked += 1
            try:
                parse_frontmatter(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, MetadataError) as exc:
                invalid.append({"path": str(path), "error": str(exc)})
    print(json.dumps({"checked": checked, "invalid": invalid}, indent=2))
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
