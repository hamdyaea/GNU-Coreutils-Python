#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
"""Educational rm subset with explicit recursion and symlink-safe traversal."""
import argparse
import os
from pathlib import Path
import sys


def confirm(path):
    return input(f"rm: remove '{path}'? [y/N] ").strip().lower() == "y"


def remove(path, *, recursive=False, directory=False, force=False, interactive=False, verbose=False):
    path = Path(path)
    if path.name in (".", "..") or str(path) == ".":
        raise OSError("refusing to remove '.' or '..'")
    if not path.is_symlink() and path.resolve() == Path("/"):
        raise OSError("refusing to remove the filesystem root")
    if not os.path.lexists(path):
        if force:
            return
        raise FileNotFoundError(f"{path}: no such file or directory")
    if path.is_symlink() or not path.is_dir():
        if interactive and not confirm(path):
            return
        path.unlink()
    elif recursive:
        if interactive and not confirm(path):
            return
        for child in path.iterdir():
            remove(child, recursive=True, directory=directory, force=force,
                   interactive=interactive, verbose=verbose)
        path.rmdir()
    elif directory:
        if interactive and not confirm(path):
            return
        path.rmdir()
    else:
        raise IsADirectoryError(f"{path}: is a directory (use -r or -d)")
    if verbose:
        print(f"removed '{path}'")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-i", action="store_true", help="ask before each removal")
    parser.add_argument("-I", action="store_true", help="ask once for recursive or large operations")
    parser.add_argument("-r", "-R", "--recursive", action="store_true")
    parser.add_argument("-d", "--dir", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    if not args.files and not args.force:
        parser.error("missing operand")
    if args.I and not args.force and (args.recursive or len(args.files) > 3):
        if input("rm: proceed with requested removals? [y/N] ").strip().lower() != "y":
            return 0
    result = 0
    for name in args.files:
        try:
            remove(name, recursive=args.recursive, directory=args.dir, force=args.force,
                   interactive=args.i and not args.force, verbose=args.verbose)
        except OSError as exc:
            print(f"rm: {exc}", file=sys.stderr)
            result = 1
    return result


if __name__ == "__main__":
    raise SystemExit(main())
