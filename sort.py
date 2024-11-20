#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The sort command from GNU coreutils in Python3.  
Example of use: python3 sort.py file.txt
'''

import sys
import argparse

def gnu_sort(files=None, numeric_sort=False, reverse=False, unique=False):
    """
    Replica of GNU sort command functionality.
    
    Args:
        files (list): List of input files to sort
        numeric_sort (bool): Sort numerically instead of lexicographically
        reverse (bool): Reverse the sorting order
        unique (bool): Remove duplicate lines
    """
    # Collect all lines from files or stdin
    lines = []
    if files:
        for file in files:
            with open(file, 'r') as f:
                lines.extend(f.readlines())
    else:
        lines = sys.stdin.readlines()

    # Remove newline characters
    lines = [line.strip() for line in lines]
    
    # Handle unique flag
    if unique:
        lines = list(dict.fromkeys(lines))
    
    # Sort based on numeric or lexicographic comparison
    if numeric_sort:
        lines.sort(key=lambda x: float(x) if x.replace('.','',1).isdigit() else float('inf'), reverse=reverse)
    else:
        lines.sort(reverse=reverse)
    
    # Print sorted lines
    for line in lines:
        print(line)

def main():
    parser = argparse.ArgumentParser(description='GNU Sort Command Replica')
    parser.add_argument('files', nargs='*', help='Input files to sort')
    parser.add_argument('-n', '--numeric-sort', action='store_true', help='Sort numerically')
    parser.add_argument('-r', '--reverse', action='store_true', help='Reverse sort order')
    parser.add_argument('-u', '--unique', action='store_true', help='Remove duplicate lines')
    
    args = parser.parse_args()
    
    gnu_sort(
        files=args.files, 
        numeric_sort=args.numeric_sort, 
        reverse=args.reverse, 
        unique=args.unique
    )

if __name__ == '__main__':
    main()
