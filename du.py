#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of the du command from coreutils in Python3  
Example of use: python3 du.py -a -H -d 1
'''
import argparse
import os
import sys

def format_size(size, human_readable):
    """Format size into human-readable format if needed."""
    if human_readable:
        for unit in ['B', 'K', 'M', 'G', 'T', 'P']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
    return str(size)

def du(path, all_files=False, human_readable=False, max_depth=None):
    """Recursively calculate disk usage for the specified path."""
    total_size = 0
    for root, dirs, files in os.walk(path):
        # Calculate total size of the current directory
        dir_size = 0
        for name in files:
            try:
                filepath = os.path.join(root, name)
                size = os.path.getsize(filepath)
                dir_size += size
                if all_files:
                    print(f"{format_size(size, human_readable)}\t{filepath}")
            except FileNotFoundError:
                continue

        total_size += dir_size

        # Print directory size if within depth limit
        if max_depth is None or root.count(os.sep) - path.count(os.sep) < max_depth:
            print(f"{format_size(dir_size, human_readable)}\t{root}")
        
        # Stop further recursion if max depth is reached
        if max_depth is not None and root.count(os.sep) - path.count(os.sep) >= max_depth:
            del dirs[:]

    return total_size

def main():
    parser = argparse.ArgumentParser(description="Python implementation of du command.")
    parser.add_argument("path", nargs="?", default=".", help="Path to calculate disk usage for")
    parser.add_argument("-a", "--all", action="store_true", help="Write counts for all files, not just directories")
    parser.add_argument("-H", "--human-readable", action="store_true", help="Print sizes in human readable format (e.g., 1K 234M 2G)")
    parser.add_argument("-d", "--max-depth", type=int, help="Print the total for a directory only if it is N or fewer levels below the command line argument")

    args = parser.parse_args()

    # Execute disk usage calculation
    total_size = du(args.path, all_files=args.all, human_readable=args.human_readable, max_depth=args.max_depth)
    print(f"Total: {format_size(total_size, args.human_readable)}\t{args.path}")

if __name__ == "__main__":
    main()

