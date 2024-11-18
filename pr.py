#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The pr command from GNU coreutils in Python3.  
Example of use: python3 pr.py -n -d file.txt 
'''
import sys
import os
import argparse
from datetime import datetime

class PRCommand:
    def __init__(self, args):
        self.opts = self.parse_arguments(args)

    def parse_arguments(self, args):
        """Parse command-line arguments similar to GNU pr."""
        parser = argparse.ArgumentParser(description='Paginate or columnate files for printing.')
        
        # Page range selection
        parser.add_argument('+PAGE_RANGE', nargs='?', help='First[:last] page to print')
        
        # Columns
        parser.add_argument('-c', '--columns', type=int, default=1, 
                            help='Number of columns to print')
        parser.add_argument('-a', '--across', action='store_true', 
                            help='Print columns across rather than down')
        
        # Spacing and formatting
        parser.add_argument('-d', '--double-space', action='store_true', 
                            help='Double space the output')
        parser.add_argument('--header', default=None, 
                            help='Header to use instead of filename')
        parser.add_argument('-l', '--length', type=int, default=66, 
                            help='Page length in lines')
        parser.add_argument('-w', '--width', type=int, default=72, 
                            help='Page width in characters')
        
        # Line numbering
        parser.add_argument('-n', '--number-lines', action='store_true', 
                            help='Number lines')
        parser.add_argument('--number-format', default='%5d', 
                            help='Format for line numbers (default: 5 digits)')
        
        # Other options
        parser.add_argument('-t', '--omit-header', action='store_true', 
                            help='Omit page headers and trailers')
        parser.add_argument('files', nargs='*', type=str, default=['-'], 
                            help='Files to process (- for stdin)')
        
        return parser.parse_args(args)

    def read_input(self, file_path):
        """Read input from file or stdin."""
        try:
            if file_path == '-':
                # Check if stdin is not a tty (i.e., has piped input)
                if not sys.stdin.isatty():
                    return sys.stdin.readlines()
                return []
            
            with open(file_path, 'r') as f:
                return f.readlines()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return []

    def format_header(self, filename, page_num):
        """Create page header."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        header = self.opts.header or filename
        return f"{header}\t{date}\tPage {page_num}\n"

    def paginate(self):
        """Main pagination logic."""
        for filename in self.opts.files:
            # Read lines from file
            lines = self.read_input(filename)
            
            # Skip if no lines
            if not lines:
                continue
            
            # Apply line numbering if requested
            if self.opts.number_lines:
                lines = [f"{self.opts.number_format % (i+1)}\t{line}" 
                         for i, line in enumerate(lines)]
            
            # Double spacing
            if self.opts.double_space:
                lines = [line.rstrip() + '\n\n' for line in lines]
            
            # Pagination
            page_num = 1
            total_lines = len(lines)
            line_index = 0
            
            while line_index < total_lines:
                # Print header if not omitted
                if not self.opts.omit_header:
                    print(self.format_header(filename or 'stdin', page_num), end='')
                
                # Print page content
                page_lines = lines[line_index:line_index+self.opts.length]
                print(''.join(page_lines), end='')
                
                # Prepare for next page
                line_index += self.opts.length
                page_num += 1
                
                # Add form feed between pages
                if line_index < total_lines:
                    print('\f', end='')
            
            # Ensure a final newline after processing each file
            print()

def main():
    pr = PRCommand(sys.argv[1:])
    pr.paginate()

if __name__ == '__main__':
    main()
