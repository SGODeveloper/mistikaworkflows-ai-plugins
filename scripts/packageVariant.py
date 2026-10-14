"""How the package of a plugin differs for one directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Tuple

from checkReport import CcheckReport
from forbiddenText import CforbiddenText
from textReplacement import CtextReplacement


@dataclass(frozen=True)
class CpackageVariant:
    """The package of one plugin for one directory (the target).

    The package is a copy of the plugin folder without excludedPaths, with
    every replacement applied and with none of forbiddenText left in its text
    files. checkPackage then validates it with the target's rules, and the
    version in its manifest names the file to upload.
    """

    target: str
    plugin: str
    manifest: str  # at the root of the package
    excludedPaths: Tuple[str, ...]  # inside the plugin folder, with '/' separators
    replacements: Tuple[CtextReplacement, ...]
    forbiddenText: CforbiddenText
    checkPackage: Callable[[Path, CcheckReport], None]

    def excludes(self, relativePath: PurePosixPath) -> bool:
        """Whether a path of the plugin folder stays out of the package."""
        for excludedPath in map(PurePosixPath, self.excludedPaths):
            if relativePath == excludedPath or excludedPath in relativePath.parents:
                return True
        return False

    def adapt(self, packageDir: Path, where: str, report: CcheckReport) -> None:
        """Applies the replacements to the copy in packageDir and checks that
        no forbidden text is left. where names packageDir in messages."""
        for replacement in self.replacements:
            replacement.applyIn(packageDir, where, report)
        self.forbiddenText.checkFolder(packageDir, where, report)
