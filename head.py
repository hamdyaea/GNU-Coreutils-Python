#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  5-11-2024
Last update: 5-11-2024
Version: 1.0
Description: Head command from GNU coreutils en python3.  
Example of use: python3 heady.py -n 5 file.txt
'''
import argparse
import os
import sys

def print_head(file, num_lines, num_bytes, quiet, verbose):
    if verbose:
        print(f"==> {file} <==")
    
    if file == "-":
        input_stream = sys.stdin
    else:
        input_stream = open(file, 'r')

    try:
        if num_bytes is not None:
            content = input_stream.read(num_bytes)
            print(content, end='')
        elif num_lines is not None:
            for _ in range(num_lines):
                line = input_stream.readline()
                if not line:
                    break
                print(line, end='')
        else:
            for _ in range(10):  # Default to 10 lines
                line = input_stream.readline()
                if not line:
                    break
                print(line, end='')
    finally:
        if file != "-":
            input_stream.close()

def main():
    parser = argparse.ArgumentParser(description='Output the first part of files.')
    parser.add_argument('files', nargs='*', default=['-'], help='Files to read (default: - for stdin)')
    parser.add_argument('-n', '--lines', type=int, help='Print the first NUM lines')
    parser.add_argument('-c', '--bytes', type=int, help='Print the first NUM bytes')
    parser.add_argument('-q', '--quiet', action='store_true', help='Never print headers')
    parser.add_argument('-v', '--verbose', action='store_true', help='Always print headers')
    parser.add_argument('--version', action='version', version='head 1.0', help='Output version information and exit')

    args = parser.parse_args()

    for file in args.files:
        print_head(file, args.lines, args.bytes, args.quiet, args.verbose)

if __name__ == '__main__':
    main()

