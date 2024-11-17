#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The paste command from GNU coreutils in Python3.
Example of use: echo -e "line1\nline2\n" | python3 paste.py
'''


import argparse
import sys

def paste_files(files, delimiters, serial, zero_terminated):
    """Merge lines of files, separated by the specified delimiters."""
    # If delimiters are provided, use them, otherwise default to TABs
    if delimiters:
        delimiters = delimiters.split(',')
    else:
        delimiters = ['\t']

    # Initialize a list to hold lines from each file
    lines = [file.readlines() for file in files]

    # Process lines
    max_lines = max(len(line) for line in lines)  # Find the maximum number of lines
    for i in range(max_lines):
        merged_line = []
        for j in range(len(lines)):
            try:
                line = lines[j][i].strip()
            except IndexError:
                line = ''  # If a file has fewer lines, use empty string
            # Add the line with the delimiter
            if j < len(delimiters):
                merged_line.append(line + delimiters[j])
            else:
                merged_line.append(line + delimiters[-1])

        # Join all parts together
        merged_line_str = ''.join(merged_line).rstrip(delimiters[-1])  # Remove trailing delimiter
        if zero_terminated:
            print(merged_line_str + '\0', end='')  # Print with NUL termination
        else:
            print(merged_line_str)  # Normal newline-terminated output

def main():
    parser = argparse.ArgumentParser(description="Merge lines of files, separated by TABs or other delimiters.")
    
    # Define arguments
    parser.add_argument('files', nargs='*', default=[sys.stdin], type=argparse.FileType('r'), help="Files to process, or use standard input if none specified.")
    
    parser.add_argument('-d', '--delimiters', default='\t', help="Use characters from LIST as delimiters instead of TABs (default: '\\t').")
    parser.add_argument('-s', '--serial', action='store_true', help="Paste one file at a time instead of in parallel.")
    parser.add_argument('-z', '--zero-terminated', action='store_true', help="Use NUL as line delimiter instead of newline.")
    parser.add_argument('--version', action='version', version="paste.py 1.0", help="Output version information and exit.")
    
    # Parse arguments
    args = parser.parse_args()

    # Check if we need to merge files serially or in parallel
    if args.serial:
        for file in args.files:
            paste_files([file], args.delimiters, serial=True, zero_terminated=args.zero_terminated)
    else:
        paste_files(args.files, args.delimiters, serial=False, zero_terminated=args.zero_terminated)

if __name__ == "__main__":
    main()

