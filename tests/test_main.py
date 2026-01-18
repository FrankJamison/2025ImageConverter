from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

import main


def _write_image(path: Path, *, fmt: str = "JPEG") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (8, 8), color=(255, 0, 0))
    img.save(path, fmt)


def test_normalize_format() -> None:
    assert main.normalize_format("png") == ("PNG", ".png")
    assert main.normalize_format("JPG") == ("JPEG", ".jpg")
    assert main.normalize_format("jpeg") == ("JPEG", ".jpg")
    assert main.normalize_format("webp") == ("WEBP", ".webp")

    with pytest.raises(ValueError):
        main.normalize_format("tiff")


def test_output_path_non_recursive_uses_basename(tmp_path: Path) -> None:
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"
    input_path = input_root / "nested" / "photo.jpg"

    output_path = main.output_path_for_input(
        input_path,
        input_root=input_root,
        output_root=output_root,
        output_ext=".png",
        recursive=False,
    )

    assert output_path == output_root / "photo.png"


def test_output_path_recursive_preserves_relpath(tmp_path: Path) -> None:
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"
    input_path = input_root / "nested" / "photo.jpg"

    output_path = main.output_path_for_input(
        input_path,
        input_root=input_root,
        output_root=output_root,
        output_ext=".png",
        recursive=True,
    )

    assert output_path == output_root / "nested" / "photo.png"


def test_convert_folder_skips_existing_when_not_overwriting(tmp_path: Path) -> None:
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"

    _write_image(input_root / "a.jpg")
    (output_root).mkdir(parents=True, exist_ok=True)
    (output_root / "a.png").write_bytes(b"already")

    converted, skipped, failed = main.convert_folder(
        input_root,
        output_root,
        output_format="png",
        recursive=False,
        overwrite=False,
        quiet=True,
    )

    assert converted == 0
    assert skipped == 1
    assert failed == 0


def test_convert_folder_overwrites_when_requested(tmp_path: Path) -> None:
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"

    _write_image(input_root / "a.jpg")
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "a.png").write_bytes(b"old")

    converted, skipped, failed = main.convert_folder(
        input_root,
        output_root,
        output_format="png",
        recursive=False,
        overwrite=True,
        quiet=True,
    )

    assert converted == 1
    assert skipped == 0
    assert failed == 0
    assert (output_root / "a.png").stat().st_size != 3


def test_convert_folder_recursive_writes_nested_output(tmp_path: Path) -> None:
    input_root = tmp_path / "in"
    output_root = tmp_path / "out"

    _write_image(input_root / "nested" / "a.jpg")

    converted, skipped, failed = main.convert_folder(
        input_root,
        output_root,
        output_format="png",
        recursive=True,
        overwrite=False,
        quiet=True,
    )

    assert converted == 1
    assert skipped == 0
    assert failed == 0
    assert (output_root / "nested" / "a.png").exists()
