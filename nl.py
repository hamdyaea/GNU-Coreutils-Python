#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The nl command from gnu coreutils in Python3.  
Example of use:  echo -e "ligne1\nligne2\n\nligne4" | python3 nl.py
'''
#!/usr/bin/env python3

import argparse
import sys
import re

def number_lines(file, options):
    """Number the lines in the given file or stdin according to options."""
    line_number = options.starting_line_number
    section_line_count = 0
    reset_numbering = True if options.no_renumber else False
    
    def get_number_style(line_number):
        """Return the formatted line number according to the chosen format."""
        if options.number_format == 'rn':
            return f"{line_number: >{options.number_width}}"
        elif options.number_format == 'rz':
            return f"{line_number:0{options.number_width}d}"
        else:  # default 'ln'
            return str(line_number)

    def process_line(line, line_number):
        """Process and number the line based on the style and format."""
        if line.strip() or options.body_numbering == 'a':
            return f"{get_number_style(line_number)}{options.number_separator}{line}"
        return line

    with open(file, 'r') if file != '-' else sys.stdin as f:
        for line in f:
            # For every section, check if we need to renumber.
            if reset_numbering and re.match(options.section_delimiter, line):
                line_number = options.starting_line_number
                section_line_count = 0

            if section_line_count >= options.join_blank_lines:
                line_number += options.line_increment
                section_line_count = 0

            # Print the processed line
            print(process_line(line, line_number))
            line_number += options.line_increment
            section_line_count += 1

def main():
    parser = argparse.ArgumentParser(description="Write each FILE to standard output, with line numbers added.")
    
    # Define arguments
    parser.add_argument('files', nargs='*', default=['-'], help="Files to be processed. Defaults to stdin if none.")
    parser.add_argument('-b', '--body-numbering', choices=['a', 't', 'n'], default='t', help="use STYLE for numbering body lines")
    parser.add_argument('-d', '--section-delimiter', type=str, default=":", help="use CC for logical page delimiters")
    parser.add_argument('-f', '--footer-numbering', choices=['a', 't', 'n'], default='n', help="use STYLE for numbering footer lines")
    parser.add_argument('--header', '--header-numbering', choices=['a', 't', 'n'], default='a', help="use STYLE for numbering header lines")  # Renamed from -h to --header
    parser.add_argument('-i', '--line-increment', type=int, default=1, help="line number increment at each line")
    parser.add_argument('-l', '--join-blank-lines', type=int, default=1, help="group of NUMBER empty lines counted as one")
    parser.add_argument('-n', '--number-format', choices=['ln', 'rn', 'rz'], default='rn', help="insert line numbers according to FORMAT")
    parser.add_argument('-p', '--no-renumber', action='store_true', help="do not reset line numbers for each section")
    parser.add_argument('-s', '--number-separator', type=str, default='\t', help="add STRING after (possible) line number")
    parser.add_argument('-v', '--starting-line-number', type=int, default=1, help="first line number for each section")
    parser.add_argument('-w', '--number-width', type=int, default=6, help="use NUMBER columns for line numbers")
    
    # Version
    parser.add_argument('--version', action='version', version="nl.py 1.0", help="output version information and exit")

    # Parse arguments
    args = parser.parse_args()

    # Process each file
    for file in args.files:
        number_lines(file, args)

if __name__ == "__main__":
    main()

