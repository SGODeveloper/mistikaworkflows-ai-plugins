"""Text that the files of a listing must not contain."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from checkReport import CcheckReport

# Files whose text a directory shows or an app reads: manifests, skills, README.
TEXT_SUFFIXES = (".md", ".json")


@dataclass(frozen=True)
class CforbiddenText:
    """Regular expressions, matched ignoring case, that no line of the text
    files of a listing may match, such as the package for a directory whose
    guidelines do not allow some content.

    Every match is an error that names the listing (scope) and says how to
    fix it (fix).
    """

    patterns: Tuple[str, ...]
    scope: str  # the listing, for messages: "the openai package"
    fix: str  # what to do about a match, for messages

    def matcher(self) -> re.Pattern[str]:
        """One expression that matches any of the patterns."""
        return re.compile("|".join(f"(?:{pattern})" for pattern in self.patterns), re.IGNORECASE)

    def checkFile(self, path: Path, where: str, report: CcheckReport) -> None:
        """Reports every match in one file. where names the file in messages."""
        self.checkLines(path, where, self.matcher(), report)

    def checkFolder(self, folder: Path, where: str, report: CcheckReport) -> None:
        """Reports every match in the text files of a folder and its subfolders.
        where names the folder in messages."""
        matcher = self.matcher()
        for path in sorted(folder.rglob("*"), key=lambda item: item.as_posix()):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                self.checkLines(path, f"{where}/{path.relative_to(folder).as_posix()}", matcher, report)

    def checkLines(self, path: Path, where: str, matcher: re.Pattern[str], report: CcheckReport) -> None:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for match in matcher.finditer(line):
                report.error(f"{where}:{number}", f"'{match.group(0)}' is not allowed in {self.scope}: {self.fix}")
