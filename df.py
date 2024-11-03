#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  3-11-2024
Last update:3-11-2024
Version: 1.0
Description: The df command from coreutils in Python3.  
Example of use: python3 df.py -h /
'''
import argparse
import os
import shutil
import sys

VERSION = "1.0.0"

def human_readable(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size}{unit}"
        size //= 1024
    return f"{size}P"

def get_disk_usage(path, args):
    """Return disk usage statistics about the given path."""
    usage = shutil.disk_usage(path)
    if args.inodes:
        # Placeholder values as inodes require system-specific calls
        inodes_total, inodes_used, inodes_free = 100000, 50000, 50000
        return inodes_total, inodes_used, inodes_free
    
    total = usage.total
    used = usage.used
    free = usage.free
    
    if args.human_readable:
        total_display = human_readable(total)
        used_display = human_readable(used)
        free_display = human_readable(free)
    else:
        total_display, used_display, free_display = total, used, free
    
    return total, used, free, total_display, used_display, free_display

def main():
    parser = argparse.ArgumentParser(description="Display disk space usage.", add_help=False)
    
    # Options pour simuler -h et --help
    parser.add_argument("--help", action="help", help="Display this help and exit")
    parser.add_argument("-h", "--human-readable", action="store_true", help="Print sizes in powers of 1024 (e.g., 1023M)")
    
    parser.add_argument("file", nargs="*", default=["/"], help="File or directory to check")
    parser.add_argument("-a", "--all", action="store_true", help="Include all file systems")
    parser.add_argument("-B", "--block-size", help="Scale sizes by SIZE before printing them")
    parser.add_argument("-i", "--inodes", action="store_true", help="List inode information instead of block usage")
    parser.add_argument("--total", action="store_true", help="Display a grand total")
    parser.add_argument("--version", action="version", version=f"df.py version {VERSION}", help="Output version information and exit")
    
    args = parser.parse_args()
    
    # Affichage de l'en-tête
    if args.inodes:
        print(f"{'Filesystem':<20} {'Inodes':<10} {'IUsed':<10} {'IFree':<10}")
    else:
        print(f"{'Filesystem':<20} {'Size':<10} {'Used':<10} {'Avail':<10} {'Use%':<5}")
    
    total_size, total_used, total_free = 0, 0, 0
    for path in args.file:
        try:
            if args.inodes:
                inodes_total, inodes_used, inodes_free = get_disk_usage(path, args)
                print(f"{path:<20} {inodes_total:<10} {inodes_used:<10} {inodes_free:<10}")
            else:
                total, used, free, total_display, used_display, free_display = get_disk_usage(path, args)
                use_percent = f"{int((used / total) * 100)}%"
                
                print(f"{path:<20} {total_display:<10} {used_display:<10} {free_display:<10} {use_percent:<5}")
                
                # Accumule les totaux si --total est spécifié
                if args.total:
                    total_size += total
                    total_used += used
                    total_free += free
        except FileNotFoundError:
            print(f"df.py: {path}: No such file or directory", file=sys.stderr)
    
    # Affiche le grand total si demandé
    if args.total and not args.inodes:
        total_percent = f"{int((total_used / total_size) * 100)}%"
        print(f"{'Total':<20} {human_readable(total_size):<10} {human_readable(total_used):<10} {human_readable(total_free):<10} {total_percent:<5}")

if __name__ == "__main__":
    main()

