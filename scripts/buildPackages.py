#!/usr/bin/env python3
"""Builds the packages of the plugins for a directory with its own rules.

For every plugin with a variant for the target (scripts/packageVariants.py),
it checks the repository as scripts/checkManifests.py does, copies the plugin
folder to dist/<target>/<plugin>/ without the excluded paths and the
operating system and editor files, adapts its text, checks the result with
the target's rules and writes dist/<target>/<plugin>-<version>.zip, the file
to upload, with the package files at its root. The plugin folder itself is
never changed. Entries are sorted and dated 1980-01-01, so building unchanged
sources again gives the same file.

Usage: python3 scripts/buildPackages.py openai   (from anywhere; exit code 1 on errors)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import List

from checkManifests import REPO_ROOT, checkRepository, displayPath
from checkReport import CcheckReport
from packageVariant import CpackageVariant
from packageVariants import VARIANTS

DIST_DIR = REPO_ROOT / "dist"

# Operating system and editor files, never packaged (see .gitignore).
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX", "__pycache__"}
JUNK_SUFFIXES = ("~", ".bak", ".swp")

ZIP_DATE = (1980, 1, 1, 0, 0, 0)
ZIP_UNIX_SYSTEM = 3
ZIP_FILE_MODE = 0o100644 << 16
ZIP_DIRECTORY_MODE = (0o040755 << 16) | 0x10  # 0x10: MS-DOS directory flag


def isJunk(name: str) -> bool:
    return name in JUNK_NAMES or name.endswith(JUNK_SUFFIXES)


def stagePackage(pluginDir: Path, variant: CpackageVariant, packageDir: Path) -> None:
    """Copies the plugin folder to packageDir, without what the package leaves out."""

    def ignored(directory: str, names: List[str]) -> List[str]:
        base = PurePosixPath(Path(directory).relative_to(pluginDir).as_posix())
        return [name for name in names if isJunk(name) or variant.excludes(base / name)]

    shutil.copytree(pluginDir, packageDir, ignore=ignored)


def writeZip(packageDir: Path, zipPath: Path) -> None:
    """Writes the package folder as a ZIP with its contents at the root."""
    entries = sorted(packageDir.rglob("*"), key=lambda path: path.relative_to(packageDir).as_posix())
    with zipfile.ZipFile(zipPath, "w") as archive:
        for path in entries:
            name = path.relative_to(packageDir).as_posix()
            if path.is_dir():
                info = zipfile.ZipInfo(name + "/", ZIP_DATE)
                info.external_attr = ZIP_DIRECTORY_MODE
                data = b""
            else:
                info = zipfile.ZipInfo(name, ZIP_DATE)
                info.external_attr = ZIP_FILE_MODE
                info.compress_type = zipfile.ZIP_DEFLATED
                data = path.read_bytes()
            info.create_system = ZIP_UNIX_SYSTEM
            archive.writestr(info, data)


def buildPackage(variant: CpackageVariant, pluginDir: Path, targetDir: Path, report: CcheckReport) -> Path | None:
    """Builds the package of one plugin. Returns its ZIP, None on errors."""
    packageDir = targetDir / variant.plugin
    stagePackage(pluginDir, variant, packageDir)
    variant.adapt(packageDir, displayPath(packageDir), report)
    variant.checkPackage(packageDir, report)
    if report.hasErrors():
        return None
    version = json.loads((packageDir / variant.manifest).read_text(encoding="utf-8"))["version"]
    zipPath = targetDir / f"{variant.plugin}-{version}.zip"
    writeZip(packageDir, zipPath)
    return zipPath


def main() -> int:
    targets = sorted({variant.target for variant in VARIANTS})
    parser = argparse.ArgumentParser(description="Builds the plugin packages for a directory with its own rules.")
    parser.add_argument("target", choices=targets, help="the directory to build the packages for")
    target = parser.parse_args().target

    report = CcheckReport()
    entries = checkRepository(report)
    if report.hasErrors():
        report.printProblems()
        print("The repository has errors: fix them before building packages.")
        return 1

    # A clean folder, so that no package of an earlier build is left to upload.
    targetDir = DIST_DIR / target
    if targetDir.exists():
        shutil.rmtree(targetDir)
    targetDir.mkdir(parents=True)

    pluginDirs = {entry.get("name"): REPO_ROOT / entry.get("source", "") for entry in entries}
    built: List[Path] = []
    for variant in (variant for variant in VARIANTS if variant.target == target):
        pluginDir = pluginDirs.get(variant.plugin)
        if pluginDir is None:
            report.error(variant.plugin, "no plugin with this name in the marketplace")
            continue
        packageReport = CcheckReport()
        zipPath = buildPackage(variant, pluginDir, targetDir, packageReport)
        report.include(packageReport)
        if zipPath is not None:
            built.append(zipPath)

    report.printProblems()
    for zipPath in built:
        print(f"built {displayPath(zipPath)}")
    print(f"{len(built)} package(s) built for {target}: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.hasErrors() else 0


if __name__ == "__main__":
    sys.exit(main())
