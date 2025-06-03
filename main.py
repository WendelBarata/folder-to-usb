"""
main.py
-------
Script to copy files from a PC directory to the first detected USB drive
(Windows), skipping unnecessary files and folders (such as venv, node_modules,
etc).

Features:
- Automatically detects the connected USB drive (Windows).
- Allows ignoring specific directories, extensions, and files.
- Efficient copy: does not enter ignored folders.
- Supports dry-run mode (simulation without copying).
- Optional progress bar (tqdm).

Main functions:
- is_pendrive: checks if a drive letter is a USB drive.
- find_pendrive: returns the letter of the first detected USB drive.
- should_ignore: determines if a file or directory should be ignored.
- smart_copy_to_pendrive: performs the smart copy operation.

Requirements:
- Windows
- pywin32 (win32file)
- tqdm (optional, for progress bar)

Example usage:
    smart_copy_to_pendrive(
        r"C:/Users/USERNAME/your_project_folder",
        dry_run=True
    )
"""

import os
import shutil
import logging

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def is_pendrive(drive_letter):
    # Simple check for Windows removable drives
    import win32file
    drive_type = win32file.GetDriveType(f"{drive_letter}:\\")
    return drive_type == win32file.DRIVE_REMOVABLE


def find_pendrive():
    # Returns the first removable drive letter found
    from string import ascii_uppercase
    for letter in ascii_uppercase:
        if is_pendrive(letter):
            return f"{letter}:\\"
    raise RuntimeError("No pendrive detected.")


def should_ignore(path, ignore_dirs, ignore_exts, ignore_files):
    name = os.path.basename(path)
    if name in ignore_dirs or name in ignore_files:
        return True
    if any(name.endswith(ext) for ext in ignore_exts):
        return True
    return False


def smart_copy_to_pendrive(
    src_folder,
    ignore_dirs=None,
    ignore_exts=None,
    ignore_files=None,
    dry_run=False
):
    """
    Copies files from src_folder to the first detected pendrive,
    skipping unwanted files/folders.
    Args:
        src_folder (str): Source folder to copy from.
        ignore_dirs (set): Directory names to ignore.
        ignore_exts (set): File extensions to ignore.
        ignore_files (set): File names to ignore.
        dry_run (bool): If True, only print what would be copied.
    """
    if ignore_dirs is None:
        ignore_dirs = {
            'node_modules', 'venv', '.git', '__pycache__', '.mypy_cache',
            '.pytest_cache', '.idea', '.next', 'dist', 'build', 'out', '.cache'
        }
    if ignore_exts is None:
        ignore_exts = {
            '.exe', '.dll', '.pyc', '.pyo', '.log', '.tmp', '.cache'
        }
    if ignore_files is None:
        ignore_files = {
            'package-lock.json', 'yarn.lock', '.DS_Store', 'Thumbs.db'
        }

    logging.basicConfig(level=logging.INFO, format='%(message)s')
    pendrive_root = find_pendrive()
    dest_folder = os.path.join(pendrive_root, os.path.basename(src_folder))

    # Count total files for progress bar
    total_files = 0
    for root, dirs, files in os.walk(src_folder):
        dirs[:] = [d for d in dirs if not should_ignore(
            d, ignore_dirs, set(), set())]
        for file in files:
            if not should_ignore(file, set(), ignore_exts, ignore_files):
                total_files += 1

    iterator = os.walk(src_folder)
    if HAS_TQDM and not dry_run:
        pbar = tqdm(total=total_files, desc="Copying files", unit="file")
    else:
        pbar = None

    for root, dirs, files in iterator:
        dirs[:] = [d for d in dirs if not should_ignore(
            d, ignore_dirs, set(), set())]
        rel_path = os.path.relpath(root, src_folder)
        dest_path = os.path.join(dest_folder, rel_path)
        if not dry_run:
            os.makedirs(dest_path, exist_ok=True)
        for file in files:
            if should_ignore(file, set(), ignore_exts, ignore_files):
                continue
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            if dry_run:
                logging.info(f"Would copy: {src_file} -> {dest_file}")
            else:
                try:
                    shutil.copy2(src_file, dest_file)
                    logging.info(f"Copied: {src_file} -> {dest_file}")
                except Exception as e:
                    logging.error(
                        f"Failed to copy {src_file} to {dest_file}: {e}"
                    )
            if pbar:
                pbar.update(1)
    if pbar:
        pbar.close()

# Example usage:
# smart_copy_to_pendrive(
#     r"C:/Users/USERNAME/your_project_folder",
#     dry_run=True
# )  # Preview
# smart_copy_to_pendrive(
#     r"C:/Users/USERNAME/your_project_folder"
# )  # Actual copy
