#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of echo from GNU Coreutils in Python3  
Example of use: python3 echo.py -e "Hello\nWorld"
'''
import sys
import re

VERSION = "echo (Python coreutils) 1.0"

def print_help():
    help_text = """
Usage: echo [OPTION]... [STRING]...
Echo the STRING(s) to standard output.

  -n             do not output the trailing newline
  -e             enable interpretation of backslash escapes
  -E             disable interpretation of backslash escapes (default)
      --help     display this help and exit
      --version  output version information and exit

If -e is in effect, the following sequences are recognized:

  \\\\    backslash
  \\a     alert (BEL)
  \\b     backspace
  \\c     produce no further output
  \\e     escape
  \\f     form feed
  \\n     new line
  \\r     carriage return
  \\t     horizontal tab
  \\v     vertical tab
  \\0NNN  byte with octal value NNN (1 to 3 digits)
  \\xHH   byte with hexadecimal value HH (1 to 2 digits)
"""
    print(help_text.strip())

def parse_escape_sequences(text):
    """Interpret backslash escape sequences in a string."""
    text = text.replace(r"\\", "\\")    # backslash
    text = text.replace(r"\a", "\a")    # alert
    text = text.replace(r"\b", "\b")    # backspace
    text = text.replace(r"\e", "\x1b")  # escape
    text = text.replace(r"\f", "\f")    # form feed
    text = text.replace(r"\n", "\n")    # new line
    text = text.replace(r"\r", "\r")    # carriage return
    text = text.replace(r"\t", "\t")    # horizontal tab
    text = text.replace(r"\v", "\v")    # vertical tab

    # Handle \0NNN (octal)
    text = re.sub(r"\\0([0-7]{1,3})", lambda m: chr(int(m.group(1), 8)), text)
    
    # Handle \xHH (hexadecimal)
    text = re.sub(r"\\x([0-9A-Fa-f]{1,2})", lambda m: chr(int(m.group(1), 16)), text)

    # Stop output on \c
    if r"\c" in text:
        text = text.split(r"\c")[0]
    return text

def main():
    args = sys.argv[1:]
    enable_escape = False
    newline = True

    if "--help" in args:
        print_help()
        return
    if "--version" in args:
        print(VERSION)
        return

    output_args = []
    for arg in args:
        if arg == "-n":
            newline = False
        elif arg == "-e":
            enable_escape = True
        elif arg == "-E":
            enable_escape = False
        else:
            output_args.append(arg)
    
    output = " ".join(output_args)
    if enable_escape:
        output = parse_escape_sequences(output)
    
    print(output, end=("" if not newline else "\n"))

if __name__ == "__main__":
    main()

