#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of the baseman command from GNU coreutils in Python3  
Example of use: python3 basename.py /usr/bin/sort
'''
import os
import sys

VERSION = "basename (Python coreutils) 1.0"

def print_help():
    help_text = """
Usage: basename [OPTION]... NAME...
Print NAME with any leading directory components removed.
If specified, also remove a trailing SUFFIX.

  -a, --multiple          support multiple arguments and treat each as a NAME
  -s, --suffix=SUFFIX     remove a trailing SUFFIX; implies -a
  -z, --zero              end each output line with NUL, not newline
      --help              display this help and exit
      --version           output version information and exit
"""
    print(help_text.strip())

def basename(name, suffix=None):
    base = os.path.basename(name)
    if suffix and base.endswith(suffix):
        base = base[:-len(suffix)]
    return base

def main():
    args = sys.argv[1:]
    multiple = False
    suffix = None
    zero_terminated = False

    if "--help" in args:
        print_help()
        return
    if "--version" in args:
        print(VERSION)
        return

    names = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-a", "--multiple"):
            multiple = True
        elif arg.startswith("-s=") or arg.startswith("--suffix="):
            suffix = arg.split("=", 1)[1]
            multiple = True
        elif arg == "-s" or arg == "--suffix":
            i += 1
            suffix = args[i]
            multiple = True
        elif arg in ("-z", "--zero"):
            zero_terminated = True
        else:
            names.append(arg)
        i += 1

    if not names:
        print("basename: missing operand")
        sys.exit(1)

    if not multiple and len(names) > 1:
        print("basename: extra operand", names[1:])
        sys.exit(1)

    output_terminator = "\0" if zero_terminated else "\n"
    for name in names:
        print(basename(name, suffix=suffix), end=output_terminator)

if __name__ == "__main__":
    main()

