#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills"
TARGET_DIR = REPO_ROOT / "plugins" / "lingyzh-skills" / "skills"


def relative_files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
    }


def compare_directories(source: Path, target: Path) -> list[str]:
    if not target.exists():
        return [f"Missing generated directory: {target.relative_to(REPO_ROOT)}"]

    source_files = relative_files(source)
    target_files = relative_files(target)
    problems: list[str] = []

    for relative_path in sorted(source_files - target_files):
        problems.append(f"Missing from Codex bundle: {relative_path.as_posix()}")

    for relative_path in sorted(target_files - source_files):
        problems.append(f"Extra in Codex bundle: {relative_path.as_posix()}")

    for relative_path in sorted(source_files & target_files):
        if (source / relative_path).read_bytes() != (target / relative_path).read_bytes():
            problems.append(f"Content differs: {relative_path.as_posix()}")

    return problems


def sync() -> None:
    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)

    TARGET_DIR.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE_DIR, TARGET_DIR)
    print(f"Synced {SOURCE_DIR.relative_to(REPO_ROOT)} -> {TARGET_DIR.relative_to(REPO_ROOT)}")


def check() -> int:
    problems = compare_directories(SOURCE_DIR, TARGET_DIR)

    if not problems:
        print("Codex plugin skill bundle is in sync.")
        return 0

    print("Codex plugin skill bundle is out of sync:")
    for problem in problems:
        print(f"- {problem}")

    print("Run: python scripts/sync-codex-plugin.py")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync root Agent Skills into the generated Codex plugin bundle."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the generated Codex bundle without changing files.",
    )
    args = parser.parse_args()

    if args.check:
        return check()

    sync()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
