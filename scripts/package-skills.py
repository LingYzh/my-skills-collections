#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import re
import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills"
DIST_DIR = REPO_ROOT / "dist"
EXCLUDED_TOP_LEVEL = {".codex-plugin", ".claude-plugin"}


def skill_version(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^\s+version:\s*[\"']?([^\"'\n]+)", text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing metadata.version in {skill_dir / 'SKILL.md'}")
    return match.group(1).strip()


def package_skill(skill_dir: Path) -> Path:
    name = skill_dir.name
    version = skill_version(skill_dir)
    archive = DIST_DIR / f"{name}-{version}.zip"

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as output:
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(skill_dir)
            if relative.parts and relative.parts[0] in EXCLUDED_TOP_LEVEL:
                continue
            output.write(path, relative.as_posix())

    return archive


def main() -> int:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    archives: list[Path] = []
    for skill_dir in sorted(path for path in SOURCE_DIR.iterdir() if path.is_dir()):
        if (skill_dir / "SKILL.md").is_file():
            archives.append(package_skill(skill_dir))

    checksum_lines = []
    for archive in archives:
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        checksum_lines.append(f"{digest}  {archive.name}")
        print(f"Created {archive.relative_to(REPO_ROOT)}")

    (DIST_DIR / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
