#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The printf command from GNU coreutils in Python3.  
Example of use: python3 printf.py "Hello %s" "World"
'''

import sys
import re

class Printf:
    def __init__(self):
        # Mapping of printf escape sequences
        self.escape_sequences = {
            '\\a': '\a',   # Alert (bell)
            '\\b': '\b',   # Backspace
            '\\e': '\033', # Escape character
            '\\f': '\f',   # Form feed
            '\\n': '\n',   # Newline
            '\\r': '\r',   # Carriage return
            '\\t': '\t',   # Horizontal tab
            '\\v': '\v',   # Vertical tab
            '\\\\': '\\',  # Backslash
            '\\"': '"',    # Double quote
        }

    def parse_format(self, format_string):
        """
        Parse format string with escape sequences
        """
        for escape, replacement in self.escape_sequences.items():
            format_string = format_string.replace(escape, replacement)
        return format_string

    def printf(self, format_string, args):
        """
        Implement printf-like formatting
        """
        # Replace format specifiers
        try:
            # Handle %s, %d, %f, %x, %o, %c etc.
            formatted = format_string % tuple(args)
            
            # Parse escape sequences
            formatted = self.parse_format(formatted)
            
            # Print without newline by default
            print(formatted, end='')
        
        except TypeError as e:
            print(f"printf: {e}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"printf: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    # No arguments
    if len(sys.argv) < 2:
        print("Usage: printf FORMAT [ARGUMENT...]", file=sys.stderr)
        sys.exit(1)

    # Separate format string and arguments
    format_string = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Create printf instance and run
    printf_cmd = Printf()
    printf_cmd.printf(format_string, args)

if __name__ == "__main__":
    main()
