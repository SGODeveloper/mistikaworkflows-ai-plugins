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
