#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The fmt command from GNU coreutils in Python3.  
Example of use: python3 fmt.py file1.txt
'''
import argparse
import textwrap
import sys

VERSION = "1.0"

def format_text(input_file, width, goal_width, prefix, crown_margin, split_only, tagged_paragraph, uniform_spacing):
    """
    Function to format the input text based on the options.
    """
    def reformat_paragraph(paragraph):
        # Apply uniform spacing (one space between words, two after sentences)
        if uniform_spacing:
            paragraph = ' '.join(paragraph.split())
            paragraph = paragraph.replace(". ", ".  ")  # Two spaces after sentences
        
        # Handle tagged paragraph indentation (first line different)
        if tagged_paragraph:
            wrapped = textwrap.fill(paragraph, width=width, initial_indent="  ", subsequent_indent="    ")
        else:
            wrapped = textwrap.fill(paragraph, width=width)
        
        return wrapped

    formatted_output = []
    
    # Read input (file or stdin)
    if input_file == '-':
        input_text = sys.stdin.read()
    else:
        with open(input_file, 'r') as file:
            input_text = file.read()

    paragraphs = input_text.split('\n\n')

    for paragraph in paragraphs:
        if prefix:
            # Reformat only lines starting with a certain prefix
            if paragraph.startswith(prefix):
                formatted_paragraph = reformat_paragraph(paragraph)
            else:
                formatted_paragraph = paragraph
        else:
            # Regular reformat
            formatted_paragraph = reformat_paragraph(paragraph)

        # Crown margin - preserve the first two lines' indentation
        if crown_margin:
            lines = formatted_paragraph.splitlines()
            if len(lines) > 2:
                # Preserve indentation for the first two lines
                lines[0] = '  ' + lines[0].lstrip()
                lines[1] = '  ' + lines[1].lstrip()
                formatted_paragraph = '\n'.join(lines)

        formatted_output.append(formatted_paragraph)

    return '\n\n'.join(formatted_output)


def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Reformat each paragraph in the file(s), writing to standard output."
    )
    parser.add_argument(
        "-w", "--width", type=int, default=75,
        help="Maximum line width (default: 75 columns)"
    )
    parser.add_argument(
        "-g", "--goal", type=int, default=93,
        help="Goal width (default: 93% of width)"
    )
    parser.add_argument(
        "-p", "--prefix", type=str,
        help="Reformat only lines beginning with STRING, reattaching the prefix to reformatted lines"
    )
    parser.add_argument(
        "-c", "--crown-margin", action="store_true",
        help="Preserve indentation of first two lines"
    )
    parser.add_argument(
        "-s", "--split-only", action="store_true",
        help="Split long lines, but do not refill"
    )
    parser.add_argument(
        "-t", "--tagged-paragraph", action="store_true",
        help="Indentation of first line different from second"
    )
    parser.add_argument(
        "-u", "--uniform-spacing", action="store_true",
        help="One space between words, two after sentences"
    )
    parser.add_argument(
        "--version", action="version", version=f"fmt.py {VERSION}",
        help="Output version information"
    )
    parser.add_argument(
        "files", nargs="*", default=["-"],
        help="Input files (or - for stdin)"
    )

    args = parser.parse_args()

    # Calculate the actual width if goal width is set
    width = args.width
    if args.goal:
        width = int(width * (args.goal / 100))

    for input_file in args.files:
        formatted_text = format_text(
            input_file,
            width=width,
            goal_width=args.goal,
            prefix=args.prefix,
            crown_margin=args.crown_margin,
            split_only=args.split_only,
            tagged_paragraph=args.tagged_paragraph,
            uniform_spacing=args.uniform_spacing
        )
        print(formatted_text)


if __name__ == "__main__":
    main()

