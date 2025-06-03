"""
simulate_main.py
------------
Verification/simulation script for main.py.

Features:
- Simulates copying files from a folder, applying the same exclusion rules for
  directories, extensions, and files as the main script.
- Generates a detailed report (simulated_copy_log.txt) containing:
    - Lists of ignored directories, extensions, and files.
    - All files that would be copied.
    - Total size to be copied and ignored.
    - Per-extension statistics (count and size of copied/ignored files).
- Correctly sums the size of all files inside ignored directories (such as
  venv, node_modules, etc.), even without entering them for copying.

Usage:
- Run this script to generate a simulation report before performing the
  actual copy.
- Does not perform any real copy, only simulates and generates the log.

Requirements:
- Python 3.x
- main.py in the same directory
"""

import os
from main import should_ignore

if __name__ == "__main__":
    # Set your test folder here (example):
    test_folder = r"C:/Users/USERNAME/your_project_folder"
    output_path = "simulated_copy_log.txt"
    total_copy_size = 0
    total_ignored_size = 0
    from collections import defaultdict
    copied_ext_stats = defaultdict(lambda: {'count': 0, 'size': 0})
    ignored_ext_stats = defaultdict(lambda: {'count': 0, 'size': 0})
    default_dirs = {
        'node_modules', 'venv', '.git', '__pycache__', '.mypy_cache',
        '.pytest_cache', '.idea', '.next', 'dist', 'build', 'out', '.cache'
    }
    default_exts = {
        '.exe', '.dll', '.pyc', '.pyo', '.log', '.tmp', '.cache'
    }
    default_files = {
        'package-lock.json', 'yarn.lock', '.DS_Store', 'Thumbs.db'
    }

    def add_dir_ignored_stats(dir_path):
        for root, _, files in os.walk(dir_path):
            for file in files:
                src_file = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(src_file)
                except Exception:
                    continue
                ext = os.path.splitext(file)[1].lower()
                global total_ignored_size
                total_ignored_size += file_size
                ignored_ext_stats[ext]['count'] += 1
                ignored_ext_stats[ext]['size'] += file_size

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Simulated Copy Log\n\n")
        # Write the default ignore lists for documentation
        f.write("## Ignored Directories\n")
        for d in default_dirs:
            f.write(f"- {d}\n")
        f.write("\n## Ignored Extensions\n")
        for e in default_exts:
            f.write(f"- {e}\n")
        f.write("\n## Ignored Files\n")
        for n in default_files:
            f.write(f"- {n}\n")
        f.write("\n## Files That Would Be Copied\n\n")
        for root, dirs, files in os.walk(test_folder):
            # Handle ignored directories: remove from walk, but sum their stats
            ignored_dirs = [
                d for d in dirs if should_ignore(d, default_dirs, set(), set())
            ]
            for ignored in ignored_dirs:
                add_dir_ignored_stats(os.path.join(root, ignored))
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            rel_path = os.path.relpath(root, test_folder)
            for file in files:
                src_file = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(src_file)
                except Exception:
                    continue
                ext = os.path.splitext(file)[1].lower()
                if should_ignore(file, set(), default_exts, default_files):
                    total_ignored_size += file_size
                    ignored_ext_stats[ext]['count'] += 1
                    ignored_ext_stats[ext]['size'] += file_size
                    continue
                dest_file = os.path.join("SIMULATED_USB", rel_path, file)
                f.write(f"Would copy: {src_file} -> {dest_file}\n")
                total_copy_size += file_size
                copied_ext_stats[ext]['count'] += 1
                copied_ext_stats[ext]['size'] += file_size
        f.write("\n## Summary\n")
        f.write(
            f"Total size to copy: "
            f"{total_copy_size / (1024*1024):.2f} MB\n"
        )
        f.write(
            f"Total size ignored: "
            f"{total_ignored_size / (1024*1024):.2f} MB\n"
        )
        # New: Extension summary tables

        def write_ext_table(title, stats):
            f.write(f"\n### {title}\n")
            f.write(f"{'Extension':<12}{'Count':>10}{'Size (MB)':>15}\n")
            f.write(f"{'-'*37}\n")
            for ext, data in sorted(
                stats.items(), key=lambda x: (-x[1]['size'], x[0])
            ):
                f.write(
                    f"{ext or '[no ext]':<12}"
                    f"{data['count']:>10}"
                    f"{data['size']/(1024*1024):>15.2f}\n"
                )

        write_ext_table("Copied Extensions", copied_ext_stats)
        write_ext_table("Ignored Extensions", ignored_ext_stats)
