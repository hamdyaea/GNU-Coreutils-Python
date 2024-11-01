#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email:  hamdy.aea@protonmail.com
Date of creation:  1-11-2024
Last update: 1-11-2024
Version: 1.0
Description: copy of cp from GNU linux coreutils in python.  
Example of use: python3 cp.py file1.txt file2.txt
'''

import os
import sys
import shutil
import stat

def copy_file(src, dst, follow_symlinks=True, preserve_attrs=False):
    """Copy a single file, optionally preserving attributes."""
    if preserve_attrs:
        shutil.copy2(src, dst)  # Copy file with metadata
    else:
        shutil.copy(src, dst)  # Copy file without metadata

def copy_directory(src, dst, follow_symlinks=True, preserve_attrs=False):
    """Recursively copy a directory."""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_directory(s, d, follow_symlinks, preserve_attrs)
        else:
            copy_file(s, d, follow_symlinks, preserve_attrs)

def cp(src, dst, options):
    """Main copy function."""
    if not os.path.exists(src):
        print(f"Source {src} does not exist.")
        return

    if os.path.isdir(src):
        if options.get('recursive'):
            copy_directory(src, dst, follow_symlinks=not options.get('no_dereference'), preserve_attrs=options.get('preserve'))
        else:
            print(f"{src} is a directory; use -R to copy it recursively.")
    else:
        # If src is a file
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))  # Target directory
        copy_file(src, dst, follow_symlinks=not options.get('no_dereference'), preserve_attrs=options.get('preserve'))

def main():
    # Default options
    options = {
        'recursive': False,
        'preserve': False,
        'force': False,
        'interactive': False,
        'no_dereference': False,
        'verbose': False,
    }

    # Parse arguments
    args = sys.argv[1:]
    src = []
    dst = None

    for arg in args:
        if arg.startswith('-'):
            if arg in ('-R', '-r', '--recursive'):
                options['recursive'] = True
            elif arg in ('-p', '--preserve'):
                options['preserve'] = True
            elif arg in ('-f', '--force'):
                options['force'] = True
            elif arg in ('-i', '--interactive'):
                options['interactive'] = True
            elif arg in ('-P', '--no-dereference'):
                options['no_dereference'] = True
            elif arg in ('-v', '--verbose'):
                options['verbose'] = True
            elif arg in ('--help'):
                print("Usage: python3 cp.py [OPTION]... SOURCE [SOURCE...] DEST")
                print("Options:")
                print("  -R, -r, --recursive    copy directories recursively")
                print("  -p, --preserve         preserve mode, ownership and timestamps")
                print("  -f, --force            if an existing destination file cannot be opened, remove it and try again")
                print("  -i, --interactive       prompt before overwrite")
                print("  -P, --no-dereference   never follow symbolic links in SOURCE")
                print("  -v, --verbose          explain what is being done")
                print("  --help                 display this help and exit")
                print("  --version              output version information and exit")
                return
            elif arg in ('--version'):
                print("cp.py version 1.0")
                return
        else:
            src.append(arg)

    if len(src) < 1:
        print("No source files specified.")
        return
    if len(src) > 1:
        dst = src[-1]  # Last argument is the destination
        src = src[:-1]  # All but the last are sources
    else:
        print("Destination not specified.")
        return

    for source in src:
        if options['verbose']:
            print(f"Copying {source} to {dst}")
        cp(source, dst, options)

if __name__ == "__main__":
    main()

