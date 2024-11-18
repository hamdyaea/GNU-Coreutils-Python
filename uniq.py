#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The uniq command from GNU coreutils in Python3.  
Example of use: python3 uniq.py -c input.txt
'''
import argparse
import sys


VERSION = "1.0"


def read_input(file, zero_terminated):
    """Read input lines, handling zero-terminated lines if required."""
    if file == "-":
        stream = sys.stdin
    else:
        stream = open(file, "r", encoding="utf-8")
    
    separator = "\0" if zero_terminated else "\n"
    try:
        for line in stream:
            yield line.rstrip(separator)
    finally:
        if file != "-":
            stream.close()


def write_output(lines, file, zero_terminated):
    """Write output lines, handling zero-terminated lines if required."""
    separator = "\0" if zero_terminated else "\n"
    if file == "-":
        for line in lines:
            sys.stdout.write(line + separator)
    else:
        with open(file, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + separator)


def process_lines(lines, args):
    """Process input lines according to the provided options."""
    previous_line = None
    count = 0
    results = []
    duplicates = []
    is_first_line = True

    def add_result(line, count):
        if args.count:
            results.append(f"{count:>7} {line}")
        elif args.repeated and count > 1:
            results.append(line)
        elif args.unique and count == 1:
            results.append(line)
        elif not args.repeated and not args.unique:
            results.append(line)

    for line in lines:
        if args.ignore_case:
            comparison_line = line.lower()
        else:
            comparison_line = line

        # Skip fields and/or characters
        if args.skip_fields > 0 or args.skip_chars > 0:
            fields = line.split()
            fields_to_skip = args.skip_fields
            if args.skip_fields > 0 and len(fields) > fields_to_skip:
                line = " ".join(fields[fields_to_skip:])
            if args.skip_chars > 0:
                line = line[args.skip_chars:]

            comparison_line = line.lower() if args.ignore_case else line

        if is_first_line:
            is_first_line = False
            previous_line = comparison_line
            count = 1
        elif comparison_line == previous_line:
            count += 1
        else:
            if args.all_repeated:
                if count > 1:
                    duplicates.extend([""] if args.all_repeated == "separate" else [])
                    duplicates.append(previous_line)
            add_result(previous_line, count)
            previous_line = comparison_line
            count = 1

    # Add the final line
    if previous_line is not None:
        if args.all_repeated:
            if count > 1:
                duplicates.extend([""] if args.all_repeated == "separate" else [])
                duplicates.append(previous_line)
        add_result(previous_line, count)

    if args.all_repeated:
        results = duplicates

    return results


def main():
    parser = argparse.ArgumentParser(description="Filter adjacent matching lines.")
    parser.add_argument(
        "input", nargs="?", default="-", help="Input file (default: standard input)."
    )
    parser.add_argument(
        "output", nargs="?", default="-", help="Output file (default: standard output)."
    )
    parser.add_argument(
        "-c", "--count", action="store_true", help="Prefix lines by the number of occurrences."
    )
    parser.add_argument(
        "-d", "--repeated", action="store_true", help="Only print duplicate lines."
    )
    parser.add_argument(
        "-D", "--all-repeated", nargs="?", const="none", choices=["none", "prepend", "separate"],
        help="Print all duplicate lines with optional delimiters."
    )
    parser.add_argument(
        "-f", "--skip-fields", type=int, default=0,
        help="Avoid comparing the first N fields."
    )
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="Ignore case when comparing."
    )
    parser.add_argument(
        "-s", "--skip-chars", type=int, default=0,
        help="Avoid comparing the first N characters."
    )
    parser.add_argument(
        "-u", "--unique", action="store_true", help="Only print unique lines."
    )
    parser.add_argument(
        "-z", "--zero-terminated", action="store_true",
        help="End lines with 0 byte, not newline."
    )
    parser.add_argument(
        "-w", "--check-chars", type=int, default=None,
        help="Compare no more than N characters in lines."
    )
    parser.add_argument(
        "--version", action="version", version=f"uniq.py {VERSION}",
        help="Output version information and exit."
    )
    args = parser.parse_args()

    lines = read_input(args.input, args.zero_terminated)
    results = process_lines(lines, args)
    write_output(results, args.output, args.zero_terminated)


if __name__ == "__main__":
    main()

