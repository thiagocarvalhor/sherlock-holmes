from __future__ import annotations

from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps


PRESETS = ("none", "basic", "binarized", "deskew_binarized")


def apply_preset(input_path: Path, preset: str, output_dir: Path) -> tuple[Path, dict[str, Any]]:
    if preset not in PRESETS:
        raise ValueError(f"Unknown preprocessing preset: {preset}")

    if preset == "none":
        return input_path, {"preset": preset, "output_created": False}

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{input_path.stem}__{preset}.png"

    if preset == "basic":
        image = Image.open(input_path)
        processed = _basic_image(image)
        processed.save(output_path)
        return output_path, {
            "preset": preset,
            "output_created": True,
            "operations": ["grayscale", "contrast_1.5"],
        }

    grayscale = _load_grayscale(input_path)

    if preset == "binarized":
        binarized = _otsu_threshold(grayscale)
        cv2.imwrite(str(output_path), binarized)
        return output_path, {
            "preset": preset,
            "output_created": True,
            "operations": ["grayscale", "otsu_threshold"],
        }

    angle = _estimate_skew_angle(grayscale)
    notes: dict[str, Any] = {
        "preset": preset,
        "output_created": True,
        "operations": ["grayscale", "deskew_if_safe", "otsu_threshold"],
        "estimated_angle": angle,
        "deskew_applied": False,
    }

    deskewed = grayscale
    if angle is not None and abs(angle) <= 15:
        deskewed = _rotate_bound(grayscale, angle)
        notes["deskew_applied"] = True

    binarized = _otsu_threshold(deskewed)
    cv2.imwrite(str(output_path), binarized)
    return output_path, notes


def _basic_image(image: Image.Image) -> Image.Image:
    grayscale = ImageOps.grayscale(image)
    return ImageEnhance.Contrast(grayscale).enhance(1.5)


def _load_grayscale(input_path: Path) -> np.ndarray:
    image = Image.open(input_path)
    return np.array(ImageOps.grayscale(image))


def _otsu_threshold(grayscale: np.ndarray) -> np.ndarray:
    _, thresholded = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    return thresholded


def _estimate_skew_angle(grayscale: np.ndarray) -> float | None:
    inverted = cv2.bitwise_not(_otsu_threshold(grayscale))
    coords = np.column_stack(np.where(inverted > 0))

    if len(coords) < 10:
        return None

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle

    # Negative angle rotates the image back toward horizontal text lines.
    return -float(angle)


def _rotate_bound(image: np.ndarray, angle: float) -> np.ndarray:
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )
