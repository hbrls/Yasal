#!/usr/bin/env python3
import argparse
import re
import shutil
from pathlib import Path


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def destination_name(source: Path, source_root: Path) -> str:
    relative_parent = source.parent.relative_to(source_root)
    slug_source = str(relative_parent) if str(relative_parent) != "." else source.stem
    slug = slugify(slug_source)
    if not slug:
        slug = slugify(source.stem)
    return f"{source.stem}-{slug}{''.join(source.suffixes)}"


def collect_moves(source_root: Path, lessons_dir: Path, target_name: str) -> list[tuple[Path, Path]]:
    if not source_root.is_dir():
        raise FileNotFoundError(f"source root does not exist: {source_root}")

    moves = []
    destinations = set()

    for source in sorted(source_root.rglob(target_name)):
        destination = lessons_dir / destination_name(source, source_root)
        if destination.exists():
            raise FileExistsError(f"destination already exists: {destination}")
        if destination in destinations:
            raise FileExistsError(f"multiple sources map to the same destination: {destination}")
        destinations.add(destination)
        moves.append((source, destination))

    return moves


def move_files(source_root: Path, lessons_dir: Path, target_name: str, dry_run: bool) -> int:
    moves = collect_moves(source_root, lessons_dir, target_name)
    lessons_dir.mkdir(parents=True, exist_ok=True)

    for source, destination in moves:
        print(f"{source} -> {destination}")
        if not dry_run:
            shutil.move(str(source), str(destination))

    return len(moves)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", default="raw0/system-prompts")
    parser.add_argument("--lessons-dir", default="lessons")
    parser.add_argument("--target-name", default="Intent.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    source_root = (project_root / args.source_root).resolve()
    lessons_dir = (project_root / args.lessons_dir).resolve()

    count = move_files(source_root, lessons_dir, args.target_name, args.dry_run)
    action = "Would move" if args.dry_run else "Moved"
    print(f"{action} {count} file(s).")


if __name__ == "__main__":
    main()
