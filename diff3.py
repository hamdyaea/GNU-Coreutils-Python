#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version:  1.0
Description:  The diff3 command from GNU coreutils in Python3. 
Example of use: diff3.py myfile oldfile yourfile
'''

import argparse
import difflib
import sys
from typing import List, Optional, TextIO

class Diff3Tool:
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
            return []

    def compare_files(self, myfile: str, oldfile: str, yourfile: str):
        """Compare three files and output differences."""
        try:
            # Read files
            my_lines = self.preprocess_lines(self.read_file(myfile))
            old_lines = self.preprocess_lines(self.read_file(oldfile))
            your_lines = self.preprocess_lines(self.read_file(yourfile))

            # Determine merge strategy
            if self.args.merge:
                return self.merge_files(my_lines, old_lines, your_lines, myfile, oldfile, yourfile)
            elif self.args.ed_script:
                return self.generate_ed_script(my_lines, old_lines, your_lines, myfile, oldfile, yourfile)
            else:
                return self.display_differences(my_lines, old_lines, your_lines, myfile, oldfile, yourfile)

        except Exception as e:
            print(f"Error processing files: {e}", file=sys.stderr)
            return 2

    def preprocess_lines(self, lines: List[str]) -> List[str]:
        """Preprocess lines based on diff3 arguments."""
        if self.args.text:
            lines = [line.rstrip('\r\n') for line in lines]
        return lines

    def display_differences(self, my_lines: List[str], old_lines: List[str], your_lines: List[str], 
                            myfile: str, oldfile: str, yourfile: str) -> int:
        """Display differences between three files."""
        sm = difflib.SequenceMatcher(None, old_lines, my_lines)
        conflicts_found = False

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'replace':
                conflicts_found = True
                if self.args.show_all or self.args.show_overlap:
                    print(f"<<<<<<< {myfile}")
                    print(''.join(my_lines[i1:i2]), end='')
                    print("=======")
                    print(''.join(your_lines[j1:j2]), end='')
                    print(f">>>>>>> {yourfile}")

        return 1 if conflicts_found else 0

    def merge_files(self, my_lines: List[str], old_lines: List[str], your_lines: List[str], 
                    myfile: str, oldfile: str, yourfile: str) -> int:
        """Merge files with different strategies."""
        merged_lines = []
        sm = difflib.SequenceMatcher(None, old_lines, my_lines)
        conflicts_found = False

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                merged_lines.extend(my_lines[i1:i2])
            elif tag == 'replace':
                conflicts_found = True
                if self.args.easy_only:
                    merged_lines.extend(my_lines[i1:i2])
                elif self.args.overlap_only:
                    merged_lines.extend(your_lines[j1:j2])
                else:
                    # Default merge with conflict markers
                    merged_lines.extend([
                        f"<<<<<<< {myfile}\n",
                        *my_lines[i1:i2],
                        "=======\n",
                        *your_lines[j1:j2],
                        f">>>>>>> {yourfile}\n"
                    ])

        # Output merged content
        print(''.join(merged_lines), end='')
        return 1 if conflicts_found else 0

    def generate_ed_script(self, my_lines: List[str], old_lines: List[str], your_lines: List[str], 
                            myfile: str, oldfile: str, yourfile: str) -> int:
        """Generate ed script for merging files."""
        script_lines = []
        sm = difflib.SequenceMatcher(None, old_lines, my_lines)
        conflicts_found = False

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'replace':
                conflicts_found = True
                script_lines.append(f"{i1 + 1}c\n")
                script_lines.extend(your_lines[j1:j2])
                script_lines.append('.\n')

        if self.args.append_wq:
            script_lines.append('w\nq\n')

        print(''.join(script_lines), end='')
        return 1 if conflicts_found else 0

def main():
    parser = argparse.ArgumentParser(description='Compare three files line by line.')
    
    # Merge and diff options
    parser.add_argument('files', nargs=3, help='Three files to compare (MYFILE OLDFILE YOURFILE)')
    parser.add_argument('-A', '--show-all', action='store_true', help='Output all changes, bracketing conflicts')
    parser.add_argument('-m', '--merge', action='store_true', help='Output merged file')
    parser.add_argument('-e', '--ed-script', action='store_true', help='Output ed script')
    
    # Conflict handling
    parser.add_argument('-E', '--show-overlap', action='store_true', help='Like -e, but bracket conflicts')
    parser.add_argument('-3', '--easy-only', action='store_true', help='Incorporate only nonoverlapping changes')
    parser.add_argument('-x', '--overlap-only', action='store_true', help='Incorporate only overlapping changes')
    
    # Additional options
    parser.add_argument('-a', '--text', action='store_true', help='Treat all files as text')
    parser.add_argument('-i', action='store_true', help='Append w and q commands to ed script')
    parser.add_argument('-T', '--initial-tab', action='store_true', help='Make tabs line up')

    args = parser.parse_args()

    diff3_tool = Diff3Tool(args)
    result = diff3_tool.compare_files(args.files[0], args.files[1], args.files[2])
    sys.exit(result)

if __name__ == "__main__":
    main()
