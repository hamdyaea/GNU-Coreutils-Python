#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  16-11-2024
Last update: 16-11-2024
Version: 1.0
Description: The csplit command from GNU coreutils in Python3  
Example of use: python3 csplit.py input.txt 10 20 30
'''

import os
import re
import sys
from pathlib import Path

def split_by_pattern(file_path, patterns, prefix="xx", suffix_format="%02d", digits=2, keep_files=False, suppress_matched=False, elide_empty_files=False, quiet=False):
    try:
        # Lire le contenu du fichier
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        output_files = []
        start_idx = 0

        for i, pattern in enumerate(patterns):
            if pattern.isdigit():  # Si le motif est un numéro de ligne
                end_idx = int(pattern) - 1
            else:  # Si le motif est une expression régulière
                regex = re.compile(pattern.strip("/"))
                end_idx = next((idx for idx, line in enumerate(lines[start_idx:], start=start_idx) if regex.search(line)), len(lines))

            if end_idx <= start_idx:
                if not elide_empty_files:
                    output_files.append(None)
                continue

            # Créer le fichier de sortie
            file_suffix = suffix_format % i
            output_file = f"{prefix}{file_suffix}"
            output_files.append(output_file)

            with open(output_file, "w", encoding="utf-8") as out:
                out.writelines(lines[start_idx:end_idx])

            if not quiet:
                print(f"{output_file}: {end_idx - start_idx} bytes")

            start_idx = end_idx
            if not suppress_matched and end_idx < len(lines):
                start_idx += 1  # Inclure la ligne correspondante dans la section suivante

        # Reste du fichier
        if start_idx < len(lines):
            file_suffix = suffix_format % len(output_files)
            output_file = f"{prefix}{file_suffix}"
            output_files.append(output_file)

            with open(output_file, "w", encoding="utf-8") as out:
                out.writelines(lines[start_idx:])

            if not quiet:
                print(f"{output_file}: {len(lines) - start_idx} bytes")

        if elide_empty_files:
            for file in output_files:
                if file and os.path.exists(file) and os.path.getsize(file) == 0:
                    os.remove(file)

    except Exception as e:
        if not keep_files:
            for file in output_files:
                if file and os.path.exists(file):
                    os.remove(file)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Split a file into sections determined by context lines.")
    parser.add_argument("file", help="Input file to split.")
    parser.add_argument("patterns", nargs="+", help="Patterns to split the file.")
    parser.add_argument("-b", "--suffix-format", default="%02d", help="Use sprintf FORMAT instead of %02d.")
    parser.add_argument("-f", "--prefix", default="xx", help="Use PREFIX instead of 'xx'.")
    parser.add_argument("-k", "--keep-files", action="store_true", help="Do not remove output files on errors.")
    parser.add_argument("-n", "--digits", type=int, default=2, help="Use specified number of digits instead of 2.")
    parser.add_argument("-s", "--quiet", action="store_true", help="Do not print counts of output file sizes.")
    parser.add_argument("-z", "--elide-empty-files", action="store_true", help="Suppress empty output files.")
    parser.add_argument("--suppress-matched", action="store_true", help="Suppress the lines matching PATTERN.")
    args = parser.parse_args()

    # Ajuster le suffix_format pour correspondre au nombre de chiffres
    suffix_format = f"%0{args.digits}d"

    split_by_pattern(
        args.file,
        args.patterns,
        prefix=args.prefix,
        suffix_format=suffix_format,
        digits=args.digits,
        keep_files=args.keep_files,
        suppress_matched=args.suppress_matched,
        elide_empty_files=args.elide_empty_files,
        quiet=args.quiet
    )

if __name__ == "__main__":
    main()

