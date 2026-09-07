# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""Audit/repair standalone status comparisons in saved Base filters.

Requires explicit --attention to remove legacy Reviewed exclusions. Does not
change dates, membership or the meaning of the generic Base evaluator.
"""
import argparse
import json
from pathlib import Path
import re

import yaml

from note_metadata import MetadataError, UniqueLoader
from status_policy import ALIASES, label, normalize_status
from validate_notes import save_repair


def rewrite(text: str, attention: bool = False) -> str:
    base = yaml.load(text, Loader=UniqueLoader)
    if not isinstance(base, dict):
        raise MetadataError('Base must be a mapping')
    changed = False

    def filters(value):
        nonlocal changed
        if isinstance(value, dict):
            return {key: filters(child) for key, child in value.items()}
        if isinstance(value, list):
            return [filters(child) for child in value]
        if not isinstance(value, str):
            return value
        match = re.fullmatch(r'status\s*(==|!=)\s*("[^"\n]*"|\'[^\'\n]*\')', value)
        if not match:
            return value
        operator, raw = match.groups()
        old = raw[1:-1]
        if attention and operator == '!=' and label(old) == 'Reviewed':
            changed = True
            return 'true'
        name = normalize_status(old)
        if name is None:
            return value
        names = [name] + [alias for alias, target in ALIASES.items() if target == name]
        variants = [variant for n in names for variant in (f'[[{n}]]', n)]
        joiner = ' && ' if operator == '!=' else ' || '
        result = '(' + joiner.join(f'status {operator} {json.dumps(v)}' for v in variants) + ')'
        changed = changed or result != value
        return result

    if 'filters' in base:
        base['filters'] = filters(base['filters'])
    for view in base.get('views', []):
        if 'filters' in view:
            view['filters'] = filters(view['filters'])
    return yaml.safe_dump(base, sort_keys=False, allow_unicode=True) if changed else text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', type=Path)
    parser.add_argument('--attention', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    if args.apply and not args.backup_dir:
        parser.error('--apply requires --backup-dir outside the vault')
    reports, errors = [], []
    for path in args.paths:
        try:
            original = path.read_bytes()
            candidate = rewrite(original.decode('utf-8'), args.attention).encode('utf-8')
            if args.apply and candidate != original:
                save_repair(path, original, candidate, args.backup_dir)
            reports.append({'path': str(path), 'changed': candidate != original, 'applied': args.apply})
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            errors.append({'path': str(path), 'error': str(exc)})
    print(json.dumps({'bases': reports, 'errors': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
