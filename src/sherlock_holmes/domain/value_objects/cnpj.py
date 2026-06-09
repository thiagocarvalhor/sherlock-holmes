"""CNPJ normalization helpers."""

from __future__ import annotations


def compact_digits(value: str | None) -> str:
    """Return only digits from a string."""

    return "".join(char for char in str(value or "") if char.isdigit())


def normalize_cnpj(value: str | None) -> str:
    """Return a 14-digit CNPJ or raise ValueError."""

    digits = compact_digits(value)
    if len(digits) != 14:
        raise ValueError(f"Invalid CNPJ: {value!r} (expected 14 digits)")
    return digits


__all__ = ["compact_digits", "normalize_cnpj"]
