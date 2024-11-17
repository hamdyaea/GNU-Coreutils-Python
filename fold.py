#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The fold command from GNU coreutils in Python3  
Example of use: echo "This is a long line that needs to be wrapped in a nice way" | python3 fold.py -w 20
'''

import sys
import argparse

def fold_text(text, width, by_bytes=False, break_at_space=False):
    """Fold text into lines of the specified width."""
    lines = []
    start = 0
    while start < len(text):
        # Determine the end of the line based on width or byte count
        if by_bytes:
            end = start + width
            lines.append(text[start:end])
        else:
            end = start + width
            if break_at_space:
                # Find the last space within the width
                if end < len(text):
                    while end > start and text[end-1] != ' ':
                        end -= 1
            lines.append(text[start:end])
        
        start = end

    return lines

def process_file(file, width, by_bytes, break_at_space):
    """Process a file, folding each line according to the specified options."""
    with open(file, 'r') if file != '-' else sys.stdin as f:
        for line in f:
            line = line.rstrip('\n')
            folded_lines = fold_text(line, width, by_bytes, break_at_space)
            for folded_line in folded_lines:
                print(folded_line)

def main():
    parser = argparse.ArgumentParser(
        description="Wrap input lines in each FILE, writing to standard output."
    )
    parser.add_argument(
        "-b", "--bytes", action="store_true", 
        help="Count bytes rather than columns."
    )
    parser.add_argument(
        "-s", "--spaces", action="store_true", 
        help="Break at spaces rather than columns."
    )
    parser.add_argument(
        "-w", "--width", type=int, default=80, 
        help="Use WIDTH columns instead of 80."
    )
    parser.add_argument(
        "--version", action="version", version="fold.py 1.0", 
        help="Show version and exit."
    )
    parser.add_argument(
        "files", nargs="*", default=["-"], 
        help="Files to process. If not specified, read from standard input."
    )
    
    args = parser.parse_args()
    
    # Process each file specified or stdin
    for file in args.files:
        process_file(file, args.width, args.bytes, args.spaces)

if __name__ == "__main__":
    main()

