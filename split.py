#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The split command from GNU coreutils in Python3.  
Example of use: python3 split.py largefilet.xt
'''

import sys
import os
import argparse

def split_file(input_file, output_prefix, lines_per_file=1000, bytes_per_file=None, numeric_suffix=False):
    """
    Split a file into multiple smaller files.
    
    Args:
    - input_file: Path to the input file
    - output_prefix: Prefix for output files
    - lines_per_file: Number of lines per output file
    - bytes_per_file: Number of bytes per output file
    - numeric_suffix: Use numeric suffix for output files
    """
    try:
        with open(input_file, 'rb') as f:
            file_number = 0
            
            while True:
                # Determine output filename
                if numeric_suffix:
                    output_filename = f"{output_prefix}{file_number:02d}"
                else:
                    output_filename = f"{output_prefix}{chr(97 + file_number)}"
                
                # Open output file
                with open(output_filename, 'wb') as out_f:
                    # Split by lines
                    if lines_per_file is not None:
                        lines_written = 0
                        while lines_written < lines_per_file:
                            line = f.readline()
                            if not line:
                                return
                            out_f.write(line)
                            lines_written += 1
                    
                    # Split by bytes
                    if bytes_per_file is not None:
                        bytes_written = 0
                        while bytes_written < bytes_per_file:
                            chunk = f.read(bytes_per_file - bytes_written)
                            if not chunk:
                                return
                            out_f.write(chunk)
                            bytes_written += len(chunk)
                
                file_number += 1
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Split a file into multiple smaller files')
    parser.add_argument('input_file', help='Input file to split')
    parser.add_argument('-l', '--lines', type=int, 
                        help='Number of lines per output file')
    parser.add_argument('-b', '--bytes', type=int, 
                        help='Number of bytes per output file')
    parser.add_argument('-a', '--suffix-length', type=int, default=2, 
                        help='Length of output file name suffix')
    parser.add_argument('-d', '--numeric-suffix', action='store_true', 
                        help='Use numeric suffixes starting at 0')
    parser.add_argument('prefix', nargs='?', default='x', 
                        help='Prefix for output files (default: x)')

    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)

    if args.lines is None and args.bytes is None:
        args.lines = 1000  # Default to 1000 lines if no option specified

    split_file(
        args.input_file, 
        args.prefix, 
        lines_per_file=args.lines, 
        bytes_per_file=args.bytes,
        numeric_suffix=args.numeric_suffix
    )

if __name__ == "__main__":
    main()
