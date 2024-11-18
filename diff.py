#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The diff command from GNU coreutils  
Example of use: python3 diff.py file1.txt file2.txt
'''

import argparse
import difflib
import os
import re
import sys
from typing import List, Optional, TextIO

class DiffTool:
    def __init__(self, args):
        self.args = args

    def read_file(self, filename: str) -> List[str]:
        """Read file content, handling stdin and different input methods."""
        if filename == '-':
            return sys.stdin.readlines()
        try:
            with open(filename, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            if self.args.new_file:
                return []
            raise

    def compare_files(self, file1: str, file2: str):
        """Compare two files using various diff strategies."""
        try:
            # Preprocess files based on arguments
            lines1 = self.preprocess_lines(self.read_file(file1))
            lines2 = self.preprocess_lines(self.read_file(file2))

            if self.args.brief:
                return self.brief_comparison(lines1, lines2, file1, file2)

            if self.args.report_identical_files and lines1 == lines2:
                print(f"{file1} and {file2} are identical")
                return 0

            # Choose diff format
            if self.args.side_by_side:
                return self.side_by_side_diff(lines1, lines2, file1, file2)
            elif self.args.context:
                return self.context_diff(lines1, lines2, file1, file2)
            elif self.args.unified:
                return self.unified_diff(lines1, lines2, file1, file2)
            else:
                return self.normal_diff(lines1, lines2, file1, file2)

        except Exception as e:
            print(f"Error comparing files: {e}", file=sys.stderr)
            return 2

    def preprocess_lines(self, lines: List[str]) -> List[str]:
        """Preprocess lines based on diff arguments."""
        if self.args.ignore_case:
            lines = [line.lower() for line in lines]
        
        if self.args.ignore_all_space or self.args.ignore_space_change:
            lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines]
        
        if self.args.ignore_blank_lines:
            lines = [line for line in lines if line.strip()]
        
        return lines

    def normal_diff(self, lines1: List[str], lines2: List[str], file1: str, file2: str):
        """Standard diff output."""
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))
        print(f"Differences between {file1} and {file2}:")
        for line in diff:
            if line.startswith('- ') or line.startswith('+ ') or line.startswith('? '):
                print(line)
        return 1 if diff else 0

    def context_diff(self, lines1: List[str], lines2: List[str], file1: str, file2: str):
        """Context diff output."""
        context_lines = self.args.context or 3
        diff = list(difflib.context_diff(lines1, lines2, fromfile=file1, tofile=file2, n=context_lines))
        print(''.join(diff))
        return 1 if diff else 0

    def unified_diff(self, lines1: List[str], lines2: List[str], file1: str, file2: str):
        """Unified diff output."""
        unified_lines = self.args.unified or 3
        diff = list(difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2, n=unified_lines))
        print(''.join(diff))
        return 1 if diff else 0

    def side_by_side_diff(self, lines1: List[str], lines2: List[str], file1: str, file2: str):
        """Side-by-side diff output."""
        width = self.args.width or 130
        differ = difflib.Differ()
        diffs = list(differ.compare(lines1, lines2))
        
        for line in diffs:
            if line.startswith('- '):
                print(line[2:].ljust(width//2) + " | ", end='')
            elif line.startswith('+ '):
                print(" " * (width//2) + "| " + line[2:])
            elif line.startswith('? '):
                continue
        
        return 1 if any(line.startswith(('- ', '+ ')) for line in diffs) else 0

    def brief_comparison(self, lines1: List[str], lines2: List[str], file1: str, file2: str):
        """Brief difference reporting."""
        if lines1 != lines2:
            print(f"Files {file1} and {file2} differ")
            return 1
        return 0

def main():
    parser = argparse.ArgumentParser(description='Compare files line by line.')
    
    # Comparison modes
    parser.add_argument('files', nargs='+', help='Files to compare')
    parser.add_argument('-q', '--brief', action='store_true', help='Report only when files differ')
    parser.add_argument('-s', '--report-identical-files', action='store_true', help='Report when two files are the same')
    
    # Context and format options
    parser.add_argument('-c', '--context', type=int, nargs='?', const=3, help='Output context lines')
    parser.add_argument('-u', '--unified', type=int, nargs='?', const=3, help='Unified diff format')
    parser.add_argument('-y', '--side-by-side', action='store_true', help='Side-by-side output')
    parser.add_argument('-W', '--width', type=int, help='Maximum output width')
    
    # Whitespace and case handling
    parser.add_argument('-i', '--ignore-case', action='store_true', help='Ignore case differences')
    parser.add_argument('-w', '--ignore-all-space', action='store_true', help='Ignore all whitespace')
    parser.add_argument('-b', '--ignore-space-change', action='store_true', help='Ignore whitespace changes')
    parser.add_argument('-B', '--ignore-blank-lines', action='store_true', help='Ignore blank lines')
    
    # File handling
    parser.add_argument('-N', '--new-file', action='store_true', help='Treat absent files as empty')
    
    args = parser.parse_args()

    # Validate file inputs
    if len(args.files) != 2:
        print("Error: Exactly two files must be specified.", file=sys.stderr)
        sys.exit(2)

    diff_tool = DiffTool(args)
    result = diff_tool.compare_files(args.files[0], args.files[1])
    sys.exit(result)

if __name__ == "__main__":
    main()
