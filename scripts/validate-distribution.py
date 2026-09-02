#!/usr/bin/env python3

from __future__ import annotations

import json
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
DIST_DIR = REPO_ROOT / "dist"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
HOST_METADATA_DIRS = {".codex-plugin", ".claude-plugin"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS_DIR.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def validate_marketplaces(skills: list[Path]) -> list[str]:
    problems: list[str] = []
    names = {path.name for path in skills}

    codex = read_json(CODEX_MARKETPLACE)
    codex_plugins = {item["name"]: item for item in codex.get("plugins", [])}
    claude = read_json(CLAUDE_MARKETPLACE)
    claude_plugins = {item["name"]: item for item in claude.get("plugins", [])}

    if set(codex_plugins) != names:
        problems.append("Codex marketplace plugin set does not match root skills")
    if set(claude_plugins) != names:
        problems.append("Claude marketplace plugin set does not match root skills")

    for skill in skills:
        name = skill.name
        expected_path = f"./skills/{name}"

        codex_item = codex_plugins.get(name)
        if codex_item and codex_item.get("source", {}).get("path") != expected_path:
            problems.append(f"Codex marketplace path is wrong for {name}")

        claude_item = claude_plugins.get(name)
        if claude_item and claude_item.get("source") != expected_path:
            problems.append(f"Claude marketplace path is wrong for {name}")

    return problems


def validate_skill_manifests(skills: list[Path]) -> list[str]:
    problems: list[str] = []

    for skill in skills:
        name = skill.name
        codex_path = skill / ".codex-plugin" / "plugin.json"
        claude_path = skill / ".claude-plugin" / "plugin.json"

        if not codex_path.is_file():
            problems.append(f"Missing Codex plugin manifest for {name}")
        else:
            codex = read_json(codex_path)
            if codex.get("name") != name:
                problems.append(f"Codex plugin name mismatch for {name}")
            if codex.get("skills") != "./":
                problems.append(f"Codex plugin must point skills to ./ for {name}")

        if not claude_path.is_file():
            problems.append(f"Missing Claude plugin manifest for {name}")
        else:
            claude = read_json(claude_path)
            if claude.get("name") != name:
                problems.append(f"Claude plugin name mismatch for {name}")
            claude_skills = claude.get("skills")
            if claude_skills not in ("./", ["./"]):
                problems.append(f"Claude plugin must point skills to ./ for {name}")

    return problems


def validate_archives(skills: list[Path]) -> list[str]:
    problems: list[str] = []

    for skill in skills:
        archives = list(DIST_DIR.glob(f"{skill.name}-*.zip"))
        if len(archives) != 1:
            problems.append(f"Expected one release ZIP for {skill.name}, found {len(archives)}")
            continue

        with zipfile.ZipFile(archives[0]) as archive:
            names = archive.namelist()
            if "SKILL.md" not in names:
                problems.append(f"Release ZIP root is missing SKILL.md for {skill.name}")
            for name in names:
                top_level = Path(name).parts[0] if Path(name).parts else ""
                if top_level in HOST_METADATA_DIRS:
                    problems.append(
                        f"Release ZIP contains host plugin metadata for {skill.name}: {name}"
                    )

    return problems


def main() -> int:
    skills = skill_dirs()
    problems = []
    problems.extend(validate_marketplaces(skills))
    problems.extend(validate_skill_manifests(skills))
    problems.extend(validate_archives(skills))

    if not problems:
        print("Distribution structure is valid.")
        return 0

    print("Distribution validation failed:")
    for problem in problems:
        print(f"- {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
