## 2025 Python Image Converter (Batch → PNG)

A small command-line Python utility that batch-converts all images in a folder into **PNG** files.

This project was built as a hands-on exercise to practice:
- Writing a simple CLI script that accepts arguments
- Working with the filesystem (listing files, creating folders)
- Using a third-party imaging library (Pillow)

---

## Features

- Converts every file in an input folder to `.png`
- Creates the output folder automatically if it doesn’t exist
- Keeps the original filename (only changes the extension)

---

## Tech Stack

- Python
- [Pillow](https://python-pillow.org/) (PIL) for image loading and saving

---

## How It Works

`main.py`:
1. Reads two command-line arguments: an `input_folder` and an `output_folder`
2. Ensures the output folder exists
3. Loops through every filename in the input folder
4. Opens each file with Pillow and saves it as PNG in the output folder

---

## Getting Started

### Prerequisites

- Python installed (3.x)

### Install Dependency (Pillow)

You can run this either in a virtual environment (recommended) or directly from your global Python install.

#### Option A — Virtual Environment (recommended)

PowerShell:

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### Option B — System Python (quick run)

```powershell
py -m pip install Pillow
```

If `py` isn’t available on your system, replace `py` with `python`.

---

## Usage

From the project root, run:

```powershell
python main.py <input_folder> <output_folder>
```

### Example (using the included sample folders)

```powershell
python main.py pokedex new
```

After running, converted PNGs will be written into the `new/` folder.

---

## Project Structure

```text
.
├─ main.py        # CLI entry point
├─ README.md      # Documentation
├─ requirements.txt
├─ pokedex/       # Example input images
└─ new/           # Example output folder (created if missing)
```

---

## Notes / Limitations

- The script currently attempts to open every file in the input folder; if the folder contains non-image files, Pillow may raise an error.
- Output filenames are based on the input filename (without extension). If two files share the same base name, later conversions will overwrite earlier ones.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'PIL'`

Install Pillow:

```powershell
python -m pip install Pillow
```

### Permission error while installing packages

Try installing for your user:

```powershell
python -m pip install --user Pillow
```

---

## What I’d Improve Next

- Skip non-image files gracefully (try/except around `Image.open`)
- Add basic logging / progress output
- Add unit tests for path handling and filename normalization