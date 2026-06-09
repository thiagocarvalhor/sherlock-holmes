"""Port for storing operational review state."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ReviewStatusStore(Protocol):
    """Read and write review status and notes for UI or persistence adapters."""

    def get_status(self, key: str, *, default: str = "pendente") -> str:
        """Return the current review status for a key."""

    def set_status(self, key: str, status: str) -> None:
        """Persist the review status for a key."""

    def get_notes(self, key: str, *, default: str = "") -> str:
        """Return the current review notes for a key."""

    def set_notes(self, key: str, notes: str) -> None:
        """Persist review notes for a key."""
