#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The dir command from Coreutils in Python3   
Example of use: python3 dir.py -l -H
'''
import os
import argparse
from datetime import datetime

def human_readable_size(size):
    """Convert file size to human-readable format."""
    for unit in ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}Y"

def list_directory(path, long_format=False, human_readable=False):
    """List the contents of a directory."""
    try:
        entries = os.listdir(path)
    except PermissionError:
        print(f"dir: cannot open directory '{path}': Permission denied")
        return
    except FileNotFoundError:
        print(f"dir: cannot access '{path}': No such file or directory")
        return

    entries.sort()
    for entry in entries:
        full_path = os.path.join(path, entry)
        try:
            stats = os.stat(full_path)
        except FileNotFoundError:
            continue  # Skip files that no longer exist

        if long_format:
            size = stats.st_size
            if human_readable:
                size = human_readable_size(size)
            modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
            print(f"{stats.st_mode:10o} {stats.st_nlink:2} {stats.st_uid:5} {stats.st_gid:5} {size:8} {modified_time} {entry}")
        else:
            print(entry)

def main():
    parser = argparse.ArgumentParser(
        description="List directory contents.",
    )
    parser.add_argument("files", nargs="*", default=["."], help="Files or directories to list (default: current directory).")
    parser.add_argument("-l", "--long", action="store_true", help="Use a long listing format.")
    parser.add_argument("-H", "--human-readable", action="store_true", help="With -l, print sizes in human-readable format.")
    parser.add_argument("-a", "--all", action="store_true", help="Do not ignore entries starting with '.'.")

    args = parser.parse_args()

    for path in args.files:
        if os.path.isdir(path):
            if len(args.files) > 1:
                print(f"{path}:")
            list_directory(path, long_format=args.long, human_readable=args.human_readable)
        elif os.path.isfile(path):
            print(path)
        else:
            print(f"dir: cannot access '{path}': No such file or directory")

if __name__ == "__main__":
    main()

