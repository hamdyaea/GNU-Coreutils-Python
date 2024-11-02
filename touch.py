#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of the touch command from GNU coreutils in Python3  
Example of use: python touch.py test.txt
'''

import os
import sys
import time
import datetime
from pathlib import Path

VERSION = "touch (Python coreutils) 1.0"

def print_help():
    help_text = """
Usage: touch [OPTION]... FILE...
Update the access and modification times of each FILE to the current time.

  -a                     change only the access time
  -c, --no-create        do not create any files
  -d, --date=STRING      parse STRING and use it instead of current time
  -f                     (ignored)
  -h, --no-dereference   affect each symbolic link instead of any referenced file
  -m                     change only the modification time
  -r, --reference=FILE   use this file's times instead of current time
  -t [[CC]YY]MMDDhhmm[.ss]  use specified time instead of current time
      --time=WORD        specify which time to change: access time (-a): 'access',
                         'atime', 'use'; modification time (-m): 'modify', 'mtime'
      --help             display this help and exit
      --version          output version information and exit

The --date=STRING is a mostly free format human readable date string, e.g., "Sun, 29 Feb 2004 16:21:42 -0800" or "2004-02-29 16:21:42" or "next Thursday".
"""
    print(help_text.strip())

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError:
        return time.time()

def parse_timestamp_arg(timestamp):
    try:
        if '.' in timestamp:
            time_struct = time.strptime(timestamp, "%Y%m%d%H%M.%S")
        else:
            time_struct = time.strptime(timestamp, "%Y%m%d%H%M")
        return time.mktime(time_struct)
    except ValueError:
        print("touch: invalid date format")
        sys.exit(1)

def set_times(path, atime, mtime, no_dereference=False):
    if no_dereference and os.path.islink(path):
        print("touch: symbolic link timestamps modification is unsupported in Python")
    else:
        os.utime(path, (atime, mtime))

def main():
    args = sys.argv[1:]
    no_create = False
    access_time_only = False
    modification_time_only = False
    date_str = None
    reference_file = None
    timestamp = None
    no_dereference = False

    if "--help" in args:
        print_help()
        return
    if "--version" in args:
        print(VERSION)
        return

    files = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-a",):
            access_time_only = True
        elif arg in ("-c", "--no-create"):
            no_create = True
        elif arg.startswith("-d=") or arg.startswith("--date="):
            date_str = arg.split("=", 1)[1]
        elif arg == "-d" or arg == "--date":
            i += 1
            date_str = args[i]
        elif arg == "-f":
            pass
        elif arg in ("-h", "--no-dereference"):
            no_dereference = True
        elif arg == "-m":
            modification_time_only = True
        elif arg.startswith("-r=") or arg.startswith("--reference="):
            reference_file = arg.split("=", 1)[1]
        elif arg == "-r" or arg == "--reference":
            i += 1
            reference_file = args[i]
        elif arg.startswith("-t"):
            timestamp = arg[2:] if len(arg) > 2 else args[i + 1]
            if len(arg) == 2:
                i += 1
        elif arg == "--time":
            i += 1
            word = args[i]
            if word in ("access", "atime", "use"):
                access_time_only = True
            elif word in ("modify", "mtime"):
                modification_time_only = True
        else:
            files.append(arg)
        i += 1

    if not files:
        print("touch: missing file operand")
        sys.exit(1)

    if date_str:
        mtime = atime = parse_date(date_str)
    elif timestamp:
        mtime = atime = parse_timestamp_arg(timestamp)
    elif reference_file:
        try:
            ref_stat = os.stat(reference_file)
            atime, mtime = ref_stat.st_atime, ref_stat.st_mtime
        except FileNotFoundError:
            print(f"touch: failed to access '{reference_file}': No such file or directory")
            sys.exit(1)
    else:
        mtime = atime = time.time()

    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            if no_create:
                continue
            path.touch()

        try:
            if access_time_only:
                set_times(path, atime, os.stat(path).st_mtime, no_dereference)
            elif modification_time_only:
                set_times(path, os.stat(path).st_atime, mtime, no_dereference)
            else:
                set_times(path, atime, mtime, no_dereference)
        except Exception as e:
            print(f"touch: cannot update '{file_path}': {e}")

if __name__ == "__main__":
    main()

