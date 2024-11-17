#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The tr command from GNU coreutils in Python3.  
Example of use: echo "hello world" | python3 tr.py 'a-z' 'A-Z'
'''
import sys
import re
from typing import Optional


def expand_ranges(range_str: str) -> str:
    """
    Expands character ranges like 'a-z' into the full range 'abcdefghijklmnopqrstuvwxyz'.

    Args:
        range_str (str): Input string with potential ranges.

    Returns:
        str: Expanded string with ranges replaced by their full character sequences.
    """
    def expand(match):
        start, end = match.group(1), match.group(2)
        return ''.join(chr(i) for i in range(ord(start), ord(end) + 1))

    # Match ranges like a-z or A-Z
    return re.sub(r'([a-zA-Z0-9])-([a-zA-Z0-9])', expand, range_str)


def tr(input_text: str, string1: str, string2: Optional[str] = None, delete=False, squeeze=False, complement=False):
    """
    Implements a simplified version of the `tr` command in Python.

    Args:
        input_text (str): The input text to process.
        string1 (str): The first string (characters to translate/delete).
        string2 (str, optional): The second string (characters to translate to). Required if not deleting.
        delete (bool): If True, deletes characters from string1.
        squeeze (bool): If True, reduces repeated characters in string1 to a single instance.
        complement (bool): If True, uses the complement of string1 for operations.

    Returns:
        str: The processed text.
    """
    # Expand ranges in string1 and string2
    string1 = expand_ranges(string1)
    if string2:
        string2 = expand_ranges(string2)

    # Handle complement option
    if complement:
        all_chars = ''.join(chr(i) for i in range(256))
        string1 = ''.join(set(all_chars) - set(string1))

    if delete:
        # Delete characters in string1
        translation_table = str.maketrans('', '', string1)
        result = input_text.translate(translation_table)
    elif string2:
        # Ensure string2 matches the length of string1
        if len(string2) < len(string1):
            string2 = string2.ljust(len(string1), string2[-1])
        elif len(string2) > len(string1):
            string2 = string2[:len(string1)]
        translation_table = str.maketrans(string1, string2)
        result = input_text.translate(translation_table)
    else:
        raise ValueError("STRING2 must be provided unless `delete` is set.")

    # Apply squeeze if enabled
    if squeeze:
        squeeze_regex = f"[{re.escape(string1)}]+"
        result = re.sub(squeeze_regex, lambda m: m.group(0)[0], result)

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Python implementation of the `tr` command.")
    parser.add_argument("string1", help="First string (characters to translate/delete)")
    parser.add_argument("string2", nargs="?", help="Second string (characters to translate to)")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete characters in string1")
    parser.add_argument("-s", "--squeeze", action="store_true", help="Squeeze repeated characters")
    parser.add_argument("-c", "--complement", action="store_true", help="Use the complement of string1")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    try:
        output_text = tr(
            input_text=input_text,
            string1=args.string1,
            string2=args.string2,
            delete=args.delete,
            squeeze=args.squeeze,
            complement=args.complement
        )
        sys.stdout.write(output_text)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

