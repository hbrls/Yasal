#!/usr/bin/env python3
"""
L0 Triage Split Tool

Usage:
    python3 l0_triage_split.py <plan_file>

Plan file format (one directive per line, # = comment):
    COPY <source_file> <start>-<end> TO <dest_file>

Example:
    COPY Kiro/Prompt.md 75-88    TO Kiro/Expert.md
    COPY Kiro/Prompt.md 143-170  TO Kiro/Expert.md
    COPY Kiro/Spec.md   77-88    TO Kiro/Expert.md
    COPY Lovable/Prompt.md 86-103 TO Lovable/Tools.md

Rules:
    - All paths are relative to the directory containing the plan file.
    - Dest files are created if they don't exist; content is appended if they do.
    - Source files: copied ranges are deleted bottom-up after all copies finish.
    - A "## 来源：<source_file>" header is inserted once per source-per-dest group.
"""

import sys
from collections import defaultdict, OrderedDict
from pathlib import Path


def parse_plan(plan_path: Path):
    ops = []  # list of (source_str, start, end, dest_str)
    with open(plan_path) as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) != 5 or parts[0] != 'COPY' or parts[3] != 'TO':
                print(f"[WARN] Line {lineno} skipped (bad format): {raw.rstrip()}")
                continue
            source, range_str, dest = parts[1], parts[2], parts[4]
            start, end = map(int, range_str.split('-'))
            ops.append((source, start, end, dest))
    return ops


def phase_copy(ops, base: Path):
    """
    Write line ranges to destination files.
    Groups output by: dest → source → sorted ranges
    Writes a '## 来源：<source>' header once per source-in-dest group.
    """
    plan: dict[str, OrderedDict] = defaultdict(OrderedDict)
    for source, start, end, dest in ops:
        plan[dest].setdefault(source, []).append((start, end))

    for dest, sources in plan.items():
        dest_path = base / dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'a', encoding='utf-8') as out:
            for source, ranges in sources.items():
                src_lines = (base / source).read_text(encoding='utf-8').splitlines(keepends=True)
                out.write(f'\n## 来源：{source}\n\n')
                for start, end in sorted(ranges):
                    out.writelines(src_lines[start - 1:end])
                    out.write('\n')
        print(f"  [COPY] → {dest}  ({sum(len(r) for r in sources.values())} range(s))")


def phase_delete(ops, base: Path):
    """
    Delete copied ranges from source files.
    Per source file: collect all ranges, sort descending, delete bottom-up.
    """
    by_source: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for source, start, end, _dest in ops:
        by_source[source].append((start, end))

    for source, ranges in by_source.items():
        src_path = base / source
        lines = src_path.read_text(encoding='utf-8').splitlines(keepends=True)
        deleted = 0
        for start, end in sorted(ranges, reverse=True):
            del lines[start - 1:end]
            deleted += (end - start + 1)
        src_path.write_text(''.join(lines), encoding='utf-8')
        print(f"  [DELETE] {source}  (-{deleted} lines, {len(ranges)} range(s))")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    plan_path = Path(sys.argv[1]).resolve()
    base = plan_path.parent
    ops = parse_plan(plan_path)
    print(f"Plan: {len(ops)} operation(s) from {plan_path.name}")

    print("Phase 1: Copy")
    phase_copy(ops, base)

    print("Phase 2: Delete")
    phase_delete(ops, base)

    plan_path.unlink()
    print(f"Cleaned up: {plan_path.name}")
    print("Done.")


if __name__ == '__main__':
    main()
