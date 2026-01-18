from __future__ import annotations

import argparse
import logging
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def normalize_format(fmt: str) -> tuple[str, str]:
    normalized = fmt.strip().lower()
    if normalized == "png":
        return "PNG", ".png"
    if normalized in {"jpg", "jpeg"}:
        return "JPEG", ".jpg"
    if normalized == "webp":
        return "WEBP", ".webp"
    raise ValueError(f"Unsupported format: {fmt!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch convert images in a folder to a chosen output format.",
    )
    parser.add_argument(
        "input_folder",
        help="Folder containing source images",
    )
    parser.add_argument(
        "output_folder",
        help="Folder to write converted images into (created if missing)",
    )
    parser.add_argument(
        "--format",
        default="png",
        help="Output format: png, jpg/jpeg, webp (default: png)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process subfolders recursively (preserves relative paths)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite outputs if they already exist",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output (still prints final summary)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()


def iter_input_files(input_folder: Path, *, recursive: bool) -> list[Path]:
    iterator = input_folder.rglob("*") if recursive else input_folder.iterdir()
    return [p for p in iterator if p.is_file()]


def output_path_for_input(
    input_path: Path,
    *,
    input_root: Path,
    output_root: Path,
    output_ext: str,
    recursive: bool,
) -> Path:
    rel_path = input_path.relative_to(
        input_root) if recursive else Path(input_path.name)
    return (output_root / rel_path).with_suffix(output_ext)


def convert_folder(
    input_folder: Path,
    output_folder: Path,
    *,
    output_format: str,
    recursive: bool,
    overwrite: bool,
    quiet: bool,
    logger: logging.Logger | None = None,
) -> tuple[int, int, int]:
    if logger is None:
        logger = logging.getLogger("image_converter")

    pillow_format, output_ext = normalize_format(output_format)
    output_folder.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0
    failed = 0

    files = iter_input_files(input_folder, recursive=recursive)
    total = len(files)

    for idx, input_path in enumerate(files, start=1):
        output_path = output_path_for_input(
            input_path,
            input_root=input_folder,
            output_root=output_folder,
            output_ext=output_ext,
            recursive=recursive,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not overwrite:
            skipped += 1
            if not quiet:
                logger.info("[%d/%d] SKIP (exists): %s -> %s",
                            idx, total, input_path, output_path)
            continue

        try:
            with Image.open(input_path) as img:
                if pillow_format == "JPEG" and img.mode not in {"RGB", "L"}:
                    img = img.convert("RGB")
                img.save(output_path, pillow_format)
            converted += 1
            if not quiet:
                logger.info("[%d/%d] OK: %s -> %s", idx,
                            total, input_path, output_path)
        except (UnidentifiedImageError, OSError) as exc:
            failed += 1
            if not quiet:
                logger.warning("[%d/%d] FAIL: %s (%s)",
                               idx, total, input_path, exc)

    return converted, skipped, failed


def main() -> int:
    args = parse_args()

    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")
    logger = logging.getLogger("image_converter")

    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder)

    if not input_folder.exists() or not input_folder.is_dir():
        print(f"Error: input_folder is not a directory: {input_folder}")
        return 2

    try:
        pillow_format, output_ext = normalize_format(args.format)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    converted, skipped, failed = convert_folder(
        input_folder,
        output_folder,
        output_format=args.format,
        recursive=args.recursive,
        overwrite=args.overwrite,
        quiet=args.quiet,
        logger=logger,
    )

    mode = "recursive" if args.recursive else "non-recursive"
    destination = f"{output_folder} (*{output_ext})"
    print(
        "Done. "
        f"Mode: {mode}, Format: {pillow_format}, Output: {destination}. "
        f"Converted: {converted}, Skipped: {skipped}, Failed: {failed}"
    )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
