# PC to USB Backup

A simple and efficient Python tool to copy files from your PC to a USB drive, automatically skipping unnecessary files and folders (like `venv`, `node_modules`, build artifacts, and more). Includes a simulation mode to preview what will be copied and how much space will be used.

---

## Features

- **Automatic USB detection** (Windows only)
- **Smart ignore rules** for common development folders and files
- **Dry-run mode**: preview what will be copied without making changes
- **Progress bar** (optional, via `tqdm`)
- **Detailed simulation report**: see file counts, sizes, and ignored content by extension

## Requirements

- Python 3.x
- Windows OS
- [pywin32](https://pypi.org/project/pywin32/) (`win32file`)
- [tqdm](https://pypi.org/project/tqdm/) (optional, for progress bar)

Install dependencies:

```sh
pip install pywin32 tqdm
```

## Usage

### 1. Copy files to USB drive

```python
from main import smart_copy_to_pendrive

smart_copy_to_pendrive(
    r"C:/Users/USERNAME/your_project_folder",  # Source folder
    dry_run=False  # Set to True for simulation only
)
```

- The script will automatically detect the first connected USB drive and copy the folder to it, skipping ignored files/folders.

### 2. Simulate the copy (see what would be copied/ignored)

Run the simulation script to generate a detailed log:

```sh
python simulate_main.py
```

- Edit `simulate_main.py` to set your source folder (`test_folder`).
- The script will create `simulated_copy_log.txt` with a summary of what would be copied and ignored, including per-extension statistics.

## Ignore Rules

By default, the following are ignored:

- **Directories:** `venv`, `node_modules`, `.git`, `__pycache__`, `.mypy_cache`, `.pytest_cache`, `.idea`, `.next`, `dist`, `build`, `out`, `.cache`
- **Extensions:** `.exe`, `.dll`, `.pyc`, `.pyo`, `.log`, `.tmp`, `.cache`
- **Files:** `package-lock.json`, `yarn.lock`, `.DS_Store`, `Thumbs.db`

You can customize these lists by passing your own sets to `smart_copy_to_pendrive`.

## Example

```python
from main import smart_copy_to_pendrive

# Preview what would be copied
smart_copy_to_pendrive(
    r"C:/Users/USERNAME/your_project_folder",
    dry_run=True
)

# Actually copy to USB
smart_copy_to_pendrive(
    r"C:/Users/USERNAME/your_project_folder"
)
```

## License

MIT License

---

**Note:** This tool is designed for Windows and will not work on Linux or macOS without modification.
