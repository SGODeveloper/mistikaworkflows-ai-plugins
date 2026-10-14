"""Problems found by the release checks of this repository."""

from __future__ import annotations

from typing import List


class CcheckReport:
    """Collects errors (block the release) and warnings (worth a look)."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warning(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")

    def hasErrors(self) -> bool:
        return bool(self.errors)

    def include(self, other: CcheckReport) -> None:
        """Adds the problems of another report, such as the one of a package."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    def printProblems(self) -> None:
        """Prints the warnings, then the errors, one per line."""
        for warning in self.warnings:
            print(f"warning: {warning}")
        for error in self.errors:
            print(f"error: {error}")
