"""A passage of a plugin file that a package replaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from checkReport import CcheckReport

PREVIEW_LENGTH = 60


@dataclass(frozen=True)
class CtextReplacement:
    """Replaces one passage of a file of the plugin folder in a package.

    The passage must appear exactly once in the file. When the source text
    changes, the replacement stops matching and the build fails, so that the
    new text is reviewed for the package instead of being shipped unadapted.
    """

    path: str  # file inside the plugin folder, with '/' separators
    original: str
    replacement: str

    def preview(self) -> str:
        """The start of the passage, to name it in messages."""
        firstLine = self.original.strip().splitlines()[0]
        return firstLine if len(firstLine) <= PREVIEW_LENGTH else firstLine[:PREVIEW_LENGTH] + "..."

    def applyIn(self, packageDir: Path, where: str, report: CcheckReport) -> None:
        """Replaces the passage in the copy of the file inside packageDir.
        Line endings are read in any style and written as LF."""
        file = packageDir / PurePosixPath(self.path)
        fileWhere = f"{where}/{self.path}"
        if not file.is_file():
            report.error(fileWhere, "file not found in the package")
            return
        text = file.read_text(encoding="utf-8")
        count = text.count(self.original)
        if count != 1:
            report.error(fileWhere, f"the passage '{self.preview()}' appears {count} time(s) instead of once: update its replacement in scripts/packageVariants.py")
            return
        file.write_text(text.replace(self.original, self.replacement), encoding="utf-8", newline="\n")
