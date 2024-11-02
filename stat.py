#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of stat from GNU Coreutils in Python3  
Example of use: python3 stat.py --format="%s %n" fichier.txt
'''

import os
import sys
import stat
import time

VERSION = "stat (Python coreutils) 1.0"

def print_help():
    help_text = """
Usage: stat [OPTION]... FILE...
Display file or file system status.

  -L, --dereference            follow links
  -Z, --context                print the SELinux security context
  -f, --file-system            display file system status instead of file status
  -c, --format=FORMAT          use the specified FORMAT instead of the default
      --printf=FORMAT          like --format, but interpret backslash escapes
  -t, --terse                  print the information in terse form
      --help                   display this help and exit
      --version                output version information and exit

Format sequences for files:
  %a    Access rights in octal
  %A    Access rights in human readable form
  %b    Number of blocks allocated
  %B    The size in bytes of each block
  %d    Device number in decimal
  %D    Device number in hex
  %f    Raw mode in hex
  %F    File type
  %g    Group ID of owner
  %G    Group name of owner
  %h    Number of hard links
  %i    Inode number
  %n    File name
  %N    Quoted file name with dereference if symbolic link
  %o    I/O block size
  %s    Total size, in bytes
  %t    Major device type in hex
  %T    Minor device type in hex
  %u    User ID of owner
  %U    User name of owner
  %x    Time of last access
  %X    Time of last access as seconds since Epoch
  %y    Time of last modification
  %Y    Time of last modification as seconds since Epoch
  %z    Time of last change
  %Z    Time of last change as seconds since Epoch
"""
    print(help_text.strip())

def parse_format(fmt, stats, follow_symlinks, selinux_context=None):
    """Interpret format sequences based on file stats."""
    replacements = {
        "%a": oct(stats.st_mode & 0o777)[2:],
        "%A": stat.filemode(stats.st_mode),
        "%b": stats.st_blocks,
        "%B": stats.st_blksize,
        "%d": stats.st_dev,
        "%D": hex(stats.st_dev),
        "%f": hex(stats.st_mode),
        "%F": "symbolic link" if stat.S_ISLNK(stats.st_mode) else "regular file",
        "%g": stats.st_gid,
        "%h": stats.st_nlink,
        "%i": stats.st_ino,
        "%n": os.path.basename(path),
        "%N": f'"{os.path.realpath(path) if follow_symlinks else path}"',
        "%o": stats.st_blksize,
        "%s": stats.st_size,
        "%t": hex(os.major(stats.st_dev)),
        "%T": hex(os.minor(stats.st_dev)),
        "%u": stats.st_uid,
        "%x": time.ctime(stats.st_atime),
        "%X": int(stats.st_atime),
        "%y": time.ctime(stats.st_mtime),
        "%Y": int(stats.st_mtime),
        "%z": time.ctime(stats.st_ctime),
        "%Z": int(stats.st_ctime),
        "%C": selinux_context if selinux_context else "N/A"
    }

    # Handle Unix-specific attributes if available
    if os.name != 'nt':
        import pwd
        import grp
        replacements["%G"] = grp.getgrgid(stats.st_gid).gr_name
        replacements["%U"] = pwd.getpwuid(stats.st_uid).pw_name
    else:
        replacements["%G"] = "N/A"
        replacements["%U"] = "N/A"

    for key, value in replacements.items():
        fmt = fmt.replace(key, str(value))
    return fmt

def main():
    args = sys.argv[1:]
    follow_symlinks = False
    file_system = False
    terse = False
    custom_format = None
    printf_format = None

    if "--help" in args:
        print_help()
        return
    if "--version" in args:
        print(VERSION)
        return

    paths = []
    for arg in args:
        if arg in ("-L", "--dereference"):
            follow_symlinks = True
        elif arg in ("-Z", "--context"):
            print("SELinux context support is not implemented in this example.")
        elif arg in ("-f", "--file-system"):
            file_system = True
        elif arg in ("-t", "--terse"):
            terse = True
        elif arg.startswith("--format="):
            custom_format = arg.split("=", 1)[1]
        elif arg.startswith("--printf="):
            printf_format = arg.split("=", 1)[1]
        else:
            paths.append(arg)

    for path in paths:
        try:
            stats = os.stat(path, follow_symlinks=follow_symlinks)
            if file_system:
                fs_stats = os.statvfs(path)
                print(f"File System for {path}:")
                print(f"Block size: {fs_stats.f_bsize}")
                print(f"Total blocks: {fs_stats.f_blocks}")
                print(f"Free blocks: {fs_stats.f_bfree}")
                continue

            if custom_format:
                output = parse_format(custom_format, stats, follow_symlinks)
            elif printf_format:
                output = parse_format(printf_format, stats, follow_symlinks).replace("\\n", "\n").replace("\\t", "\t")
            elif terse:
                output = f"{stats.st_mode} {stats.st_uid} {stats.st_gid} {stats.st_size} {stats.st_mtime} {path}"
            else:
                output = (
                    f"  File: {path}\n"
                    f"  Size: {stats.st_size}\tBlocks: {stats.st_blocks}\tIO Block: {stats.st_blksize}\n"
                    f"Device: {stats.st_dev}\tInode: {stats.st_ino}\tLinks: {stats.st_nlink}\n"
                    f"Access: ({oct(stats.st_mode)})\tUid: ({stats.st_uid})\tGid: ({stats.st_gid})\n"
                    f"Access: {time.ctime(stats.st_atime)}\n"
                    f"Modify: {time.ctime(stats.st_mtime)}\n"
                    f"Change: {time.ctime(stats.st_ctime)}"
                )

            print(output)

        except FileNotFoundError:
            print(f"stat: cannot stat '{path}': No such file or directory")

if __name__ == "__main__":
    main()

