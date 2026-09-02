#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills"
PLUGINS_DIR = REPO_ROOT / "plugins"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
LEGACY_BUNDLE = PLUGINS_DIR / "lingyzh-skills"

CATEGORY_OVERRIDES = {
    "grilling": "Productivity",
    "vue-best-practices": "Developer Tools",
}

DISPLAY_NAME_OVERRIDES = {
    "grilling": "Grilling",
    "vue-best-practices": "Vue Best Practices",
}

SHORT_DESCRIPTION_OVERRIDES = {
    "grilling": "Clarify material ambiguity before planning or execution",
    "vue-best-practices": "Personal Vue 3 and uni-app development conventions",
}

PLUGIN_DESCRIPTION_OVERRIDES = {
    "grilling": "Clarify material ambiguity, stress-test plans and requirements, and reduce avoidable rework.",
    "vue-best-practices": "Customized Vue 3 and uni-app development practices focused on maintainability and personal workflow conventions.",
}

LONG_DESCRIPTION_OVERRIDES = {
    "grilling": "Stress-test plans and requirements, resolve material ambiguity through Ask-tool-first interaction, and reduce avoidable rework before execution.",
    "vue-best-practices": "Customized Vue 3 and uni-app development guidance covering JS/JSDoc/TS tiers, four-space formatting, request layering, async UI locks, Pinia, Axios, and platform gates.",
}

DEFAULT_PROMPT_OVERRIDES = {
    "grilling": "Use the grilling skill when material ambiguity should be resolved before planning or execution.",
    "vue-best-practices": "Use vue-best-practices for Vue.js and uni-app Vue development tasks.",
}

KEYWORD_OVERRIDES = {
    "grilling": ["agent-skills", "grilling", "requirements"],
    "vue-best-practices": ["agent-skills", "vue", "uni-app"],
}


def parse_frontmatter(skill_dir: Path) -> dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter: {skill_dir / 'SKILL.md'}")

    frontmatter = text.split("---\n", 2)[1]

    def match(pattern: str, label: str) -> str:
        result = re.search(pattern, frontmatter, flags=re.MULTILINE)
        if not result:
            raise ValueError(f"Missing {label}: {skill_dir / 'SKILL.md'}")
        return result.group(1).strip().strip('"\'')

    return {
        "name": match(r"^name:\s*(.+)$", "name"),
        "description": match(r"^description:\s*(.+)$", "description"),
        "version": match(r"^\s+version:\s*(.+)$", "metadata.version"),
    }


def source_skills() -> list[tuple[Path, dict[str, str]]]:
    result: list[tuple[Path, dict[str, str]]] = []
    for skill_dir in sorted(path for path in SOURCE_DIR.iterdir() if path.is_dir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        metadata = parse_frontmatter(skill_dir)
        if metadata["name"] != skill_dir.name:
            raise ValueError(
                f"Skill directory/name mismatch: {skill_dir.name} != {metadata['name']}"
            )
        result.append((skill_dir, metadata))
    return result


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )


def codex_plugin_manifest(metadata: dict[str, str]) -> dict:
    name = metadata["name"]
    category = CATEGORY_OVERRIDES.get(name, "Productivity")
    keywords = KEYWORD_OVERRIDES.get(name, ["agent-skills", name])
    return {
        "name": name,
        "version": metadata["version"],
        "description": PLUGIN_DESCRIPTION_OVERRIDES.get(name, metadata["description"]),
        "author": {
            "name": "LingYzh",
            "url": "https://github.com/LingYzh",
        },
        "homepage": "https://github.com/LingYzh/my-skills-collections",
        "repository": "https://github.com/LingYzh/my-skills-collections",
        "license": "MIT",
        "keywords": [*keywords, "codex"],
        "skills": "./skills/",
        "interface": {
            "displayName": DISPLAY_NAME_OVERRIDES.get(name, name),
            "shortDescription": SHORT_DESCRIPTION_OVERRIDES.get(name, metadata["description"]),
            "longDescription": LONG_DESCRIPTION_OVERRIDES.get(name, metadata["description"]),
            "developerName": "LingYzh",
            "category": category,
            "websiteURL": "https://github.com/LingYzh/my-skills-collections",
            "defaultPrompt": [DEFAULT_PROMPT_OVERRIDES.get(name, f"Use the {name} skill when relevant.")],
        },
    }


def claude_plugin_manifest(metadata: dict[str, str]) -> dict:
    name = metadata["name"]
    keywords = KEYWORD_OVERRIDES.get(name, ["agent-skills", name])
    return {
        "name": name,
        "displayName": DISPLAY_NAME_OVERRIDES.get(name, name),
        "version": metadata["version"],
        "description": PLUGIN_DESCRIPTION_OVERRIDES.get(name, metadata["description"]),
        "author": {
            "name": "LingYzh",
            "url": "https://github.com/LingYzh",
        },
        "homepage": "https://github.com/LingYzh/my-skills-collections",
        "repository": "https://github.com/LingYzh/my-skills-collections",
        "license": "MIT",
        "keywords": [*keywords, "claude-code"],
        "skills": "./skills/",
    }


def codex_marketplace(skills: list[tuple[Path, dict[str, str]]]) -> dict:
    plugins = []
    for _, metadata in skills:
        name = metadata["name"]
        plugins.append(
            {
                "name": name,
                "source": {
                    "source": "local",
                    "path": f"./plugins/{name}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": CATEGORY_OVERRIDES.get(name, "Productivity"),
            }
        )
    return {
        "name": "lingyzh-skills",
        "interface": {"displayName": "LingYzh Skills"},
        "plugins": plugins,
    }


def claude_marketplace(skills: list[tuple[Path, dict[str, str]]]) -> dict:
    plugins = []
    for _, metadata in skills:
        name = metadata["name"]
        keywords = KEYWORD_OVERRIDES.get(name, ["agent-skills", name])
        plugins.append(
            {
                "name": name,
                "source": f"./plugins/{name}",
                "description": PLUGIN_DESCRIPTION_OVERRIDES.get(name, metadata["description"]),
                "version": metadata["version"],
                "author": {
                    "name": "LingYzh",
                    "url": "https://github.com/LingYzh",
                },
                "homepage": "https://github.com/LingYzh/my-skills-collections",
                "repository": "https://github.com/LingYzh/my-skills-collections",
                "license": "MIT",
                "keywords": [*keywords, "claude-code"],
                "category": CATEGORY_OVERRIDES.get(name, "Productivity"),
            }
        )
    return {
        "name": "lingyzh-skills",
        "owner": {
            "name": "LingYzh",
            "url": "https://github.com/LingYzh",
        },
        "description": "LingYzh's personal marketplace of customized Agent Skills.",
        "plugins": plugins,
    }


def generate(target_root: Path) -> None:
    skills = source_skills()
    target_plugins = target_root / "plugins"

    for source_dir, metadata in skills:
        name = metadata["name"]
        plugin_dir = target_plugins / name
        skill_target = plugin_dir / "skills" / name
        skill_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, skill_target)
        write_json(plugin_dir / ".codex-plugin" / "plugin.json", codex_plugin_manifest(metadata))
        write_json(plugin_dir / ".claude-plugin" / "plugin.json", claude_plugin_manifest(metadata))

    write_json(target_root / ".agents" / "plugins" / "marketplace.json", codex_marketplace(skills))
    write_json(target_root / ".claude-plugin" / "marketplace.json", claude_marketplace(skills))


def relative_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def compare_directories(expected: Path, actual: Path, label: str) -> list[str]:
    expected_files = relative_files(expected)
    actual_files = relative_files(actual)
    problems: list[str] = []

    for relative_path in sorted(expected_files - actual_files):
        problems.append(f"Missing from {label}: {relative_path.as_posix()}")
    for relative_path in sorted(actual_files - expected_files):
        problems.append(f"Extra in {label}: {relative_path.as_posix()}")
    for relative_path in sorted(expected_files & actual_files):
        if (expected / relative_path).read_bytes() != (actual / relative_path).read_bytes():
            problems.append(f"Content differs in {label}: {relative_path.as_posix()}")
    return problems


def build_expected() -> Path:
    temporary = Path(tempfile.mkdtemp(prefix="skills-plugin-sync-"))
    generate(temporary)
    return temporary


def sync() -> None:
    expected = build_expected()
    try:
        desired_names = {path.name for path in (expected / "plugins").iterdir() if path.is_dir()}

        if LEGACY_BUNDLE.exists():
            shutil.rmtree(LEGACY_BUNDLE)

        for name in desired_names:
            target = PLUGINS_DIR / name
            if target.exists():
                shutil.rmtree(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(expected / "plugins" / name, target)

        CODEX_MARKETPLACE.parent.mkdir(parents=True, exist_ok=True)
        CLAUDE_MARKETPLACE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(expected / ".agents" / "plugins" / "marketplace.json", CODEX_MARKETPLACE)
        shutil.copy2(expected / ".claude-plugin" / "marketplace.json", CLAUDE_MARKETPLACE)
    finally:
        shutil.rmtree(expected)


def check() -> int:
    expected = build_expected()
    problems: list[str] = []
    try:
        for plugin_dir in sorted((expected / "plugins").iterdir()):
            problems.extend(
                compare_directories(
                    plugin_dir,
                    PLUGINS_DIR / plugin_dir.name,
                    f"plugin {plugin_dir.name}",
                )
            )

        for expected_file, actual_file, label in [
            (
                expected / ".agents" / "plugins" / "marketplace.json",
                CODEX_MARKETPLACE,
                "Codex marketplace",
            ),
            (
                expected / ".claude-plugin" / "marketplace.json",
                CLAUDE_MARKETPLACE,
                "Claude marketplace",
            ),
        ]:
            if not actual_file.exists():
                problems.append(f"Missing {label}: {actual_file.relative_to(REPO_ROOT)}")
            elif expected_file.read_bytes() != actual_file.read_bytes():
                problems.append(f"Content differs: {label}")

        if LEGACY_BUNDLE.exists():
            problems.append("Legacy plugins/lingyzh-skills bundle still exists")
    finally:
        shutil.rmtree(expected)

    if not problems:
        print("Per-skill Codex/Claude plugin distribution is in sync.")
        return 0

    print("Plugin distribution is out of sync:")
    for problem in problems:
        print(f"- {problem}")
    print("Run: python scripts/sync-plugins.py")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate one Codex/Claude plugin per root Agent Skill."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated plugin directories and marketplace manifests without modifying them.",
    )
    args = parser.parse_args()

    if args.check:
        return check()

    sync()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
