#!/usr/bin/env python3

# Developers : Mehdi Marhol / Hamdy Abou El Anein
# kbmehdi69@gmail.com / hamdy.aea@protonmail.com

# This software is a basic copy of the famous ls command in Linux coreutils.

import os
import sys
from stat import S_ISDIR, S_ISLNK
import pwd
import grp
import time

def format_permissions(mode):
    permissions = [
        "d" if S_ISDIR(mode) else ("l" if S_ISLNK(mode) else "-"),
        "r" if mode & 0o400 else "-",
        "w" if mode & 0o200 else "-",
        "x" if mode & 0o100 else "-",
        "r" if mode & 0o040 else "-",
        "w" if mode & 0o020 else "-",
        "x" if mode & 0o010 else "-",
        "r" if mode & 0o004 else "-",
        "w" if mode & 0o002 else "-",
        "x" if mode & 0o001 else "-",
    ]
    return "".join(permissions)

def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return f"{size:.1f}{unit}"
        size /= 1024.0

def list_directory(path=".", show_all=False, almost_all=False, long_format=False):
    try:
        entries = os.listdir(path)

        if not show_all:
            entries = [entry for entry in entries if not entry.startswith(".")]
        elif almost_all:
            entries = [entry for entry in entries if entry not in [".", ".."]]

        if long_format:
            for entry in sorted(entries):
                full_path = os.path.join(path, entry)
                stat_info = os.lstat(full_path)

                permissions = format_permissions(stat_info.st_mode)
                n_links = stat_info.st_nlink
                owner = pwd.getpwuid(stat_info.st_uid).pw_name
                group = grp.getgrgid(stat_info.st_gid).gr_name
                size = human_readable_size(stat_info.st_size)
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(stat_info.st_mtime))

                print(f"{permissions} {n_links:>2} {owner:<8} {group:<8} {size:>8} {mtime} {entry}")
        else:
            print("  ".join(sorted(entries)))

    except FileNotFoundError:
        print(f"Error: Directory '{path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for directory '{path}'.")

def print_help():
    print("NAME\n    ls - list directory contents\n")
    print("SYNOPSIS\n    ls [OPTION]... [FILE]...\n")
    print("DESCRIPTION\n    List information about the FILEs (the current directory by default).\n")
    print("OPTIONS")
    print("  -a, --all            Do not ignore entries starting with .")
    print("  -A, --almost-all     Do not list implied . and ..")
    print("  -l                   Use a long listing format")
    print("  -h, --help           Display this help and exit")

def main():
    show_all = False
    almost_all = False
    long_format = False

    # Parse arguments
    args = sys.argv[1:]
    path = "."

    for arg in args:
        if arg in ("-a", "--all"):
            show_all = True
        elif arg in ("-A", "--almost-all"):
            almost_all = True
        elif arg == "-l":
            long_format = True
        elif arg in ("-h", "--help"):
            print_help()
            return
        elif os.path.isdir(arg):
            path = arg
        else:
            print(f"Error: Unknown option or invalid path '{arg}'")
            return

    list_directory(path, show_all, almost_all, long_format)

if __name__ == "__main__":
    main()
