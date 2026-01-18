# 2025 Python Image Converter (Batch → PNG/JPG/WebP)

A small, focused **command-line image conversion utility** written in Python. It takes an input folder, converts each image it finds, and writes outputs in a chosen format (PNG/JPG/WebP) into a destination folder.

This repo is intentionally lightweight, built to demonstrate practical fundamentals that recruiters and developers care about: CLI design, filesystem automation, working with third‑party libraries, and producing a clean, usable deliverable.

---

## Quick Pitch (for Recruiters)

**What it does:** batch converts images from one folder into a chosen output format (`.png`, `.jpg`, `.webp`) in another folder.

**What it demonstrates:**

- Building a small CLI tool (argument-driven workflow)
- Filesystem operations (directory creation, listing, safe naming)
- Using a production-grade imaging library ([Pillow](https://python-pillow.org/))
- Delivering documentation and a repeatable setup (`requirements.txt`)

**Why it matters:** many real-world tasks are “small automation” problems. This project is an example of shipping a tidy tool that solves a real pain point quickly.

---

## Features

- Batch converts every file in an input folder into a chosen output format (`.png`, `.jpg`, `.webp`)
- Auto-creates the output folder if it doesn’t exist
- Preserves the original base filename (only changes the extension)
- Skips existing outputs by default (use `--overwrite` to replace)
- Handles non-image files gracefully (counts failures instead of crashing)
- Optional recursive mode to process subfolders (`--recursive`)

---

## Tech Stack

- **Python 3.x**
- **Pillow 12.x** for image decoding/encoding

Dependency is pinned in `requirements.txt` for reproducibility.

---

## Repository Layout

```text
.
├─ main.py            # CLI entry point (batch conversion)
├─ requirements.txt   # Runtime dependency pins
├─ README.md          # Project documentation
├─ pokedex/           # Sample input images (.jpg)
└─ new/               # Sample output images (generated)
```

---

## How It Works (Design + Implementation)

At a high level, the program follows a simple pipeline:

1. Read CLI arguments: `input_folder` and `output_folder`
2. Ensure the output folder exists (create it if missing)
3. Iterate over filenames in the input folder
4. For each file:
	- Open it via Pillow (`Image.open`)
	- Strip the original extension to get a base name
	- Save to the output folder in the chosen output format

### Key Design Decisions

- **Folder-to-folder workflow:** favors batch automation over single-file operation.
- **Keep names stable:** output naming uses the original base filename, so conversions are easy to track and diff.
- **Minimal dependencies:** Pillow is the only external library.

### Current Behavior (Important for Developers)

- The script iterates over files in the input folder (non-recursive by default).
- With `--recursive`, subfolders are processed and output subfolders are created to match.
- Files that cannot be decoded as images are counted as failures and skipped.
- If two different inputs share the same base name (e.g., `a.jpg` and `a.webp`), outputs will collide because both map to the same output name.
- Existing outputs are skipped unless `--overwrite` is provided.

---

## Getting Started

### Prerequisites

- Python 3.x installed

### Install

Recommended (virtual environment):

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Quick run (system Python):

```powershell
py -m pip install Pillow
```

If `py` isn’t available, replace it with `python`.

---

## Usage

Run from the project root:

```powershell
python main.py <input_folder> <output_folder>
```

Optional flags:

```text
--format      Output format: png, jpg/jpeg, webp (default: png)
--recursive   Process subfolders recursively (preserves relative paths)
--overwrite   Overwrite outputs if they already exist
--quiet       Suppress per-file output (still prints final summary)
--verbose     Enable debug logging
```

### More Examples

Convert to WebP (overwrite existing outputs):

```powershell
python main.py pokedex new --format webp --overwrite
```

Convert recursively while preserving subfolder structure:

```powershell
python main.py <input_folder> <output_folder> --recursive
```

### Example (using included sample folders)

```powershell
python main.py pokedex new
```

After running, converted files will be written into the `new/` folder.

---

## Developer Notes

### CLI Contract

The program exposes a small argparse-driven CLI:

- `input_folder` — directory containing source images
- `output_folder` — directory where converted files will be written

It also supports:

- `--format`
- `--recursive`
- `--overwrite`
- `--quiet`
- `--verbose`

If `input_folder` is missing or invalid, the program exits with a non-zero status and prints an error.

### Exit Codes

- `0` — completed with no conversion failures
- `1` — completed but one or more files failed to convert
- `2` — invalid input (e.g., input folder does not exist)

---

## Testing

Install dev dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Run tests:

```powershell
pytest
```

### Complexity

- Runtime is approximately $O(n)$ over files in the folder (each file is decoded and re-encoded once).
- Memory usage depends on image dimensions because each image is loaded into memory during conversion.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'PIL'`

Install Pillow:

```powershell
python -m pip install -r requirements.txt
```

### Permission error while installing packages

Try installing for your user:

```powershell
python -m pip install --user -r requirements.txt
```

### `Error: Unsupported format: '...'`

Use one of the supported output formats:

```text
png, jpg/jpeg, webp
```

---

## Roadmap / Improvements

If you want to evolve this into a more production-ready utility, good next steps are:

- Add `--dry-run` to preview planned outputs without writing files
- Add collision handling options (e.g., auto-rename, keep existing, fail fast)
- Add `--include/--exclude` patterns (process only certain extensions)
- Add `--workers` for parallel conversion (CPU-bound tradeoffs)
- Add richer reporting (write a JSON/CSV summary of results)

---

## License

No license file is included in this repository currently. If you plan to share or reuse this project publicly, consider adding a license (e.g., MIT) to make permissions explicit.