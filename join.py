#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The join command from GNU coreutils in Python3.  
Example of use: python3 join.py file1.txt file2.txt
'''

import argparse
import sys

def join_files(file1, file2, join_field1, join_field2, delimiter, output_format, ignore_case, missing_value, header, check_order):
    """
    Function to join lines from two files based on a common field.
    """
    def read_file(file, delimiter):
        """
        Read a file into a list of lines, processing each line to split into fields.
        """
        lines = []
        with open(file, 'r') if file != '-' else sys.stdin as f:
            for line in f:
                if line.endswith('\n'):
                    line = line[:-1]
                fields = line.split(delimiter)
                lines.append(fields)
        return lines

    def join_lines(lines1, lines2):
        """
        Join lines based on the join field.
        """
        result = []
        i, j = 0, 0
        while i < len(lines1) and j < len(lines2):
            # Compare the join fields of both lines
            field1 = lines1[i][join_field1]
            field2 = lines2[j][join_field2]
            comparison = (field1.lower() if ignore_case else field1) == (field2.lower() if ignore_case else field2)

            if comparison:
                # Join the lines and append to result
                joined_line = []
                for format in output_format:
                    if format == '0':
                        joined_line.append(field1)
                    elif format == '1':
                        joined_line.extend(lines1[i])
                    elif format == '2':
                        joined_line.extend(lines2[j])
                result.append(delimiter.join(joined_line))
                i += 1
                j += 1
            elif field1 < field2:
                i += 1
            else:
                j += 1
        return result

    # Read both files
    lines1 = read_file(file1, delimiter)
    lines2 = read_file(file2, delimiter)

    # Check for ordering if necessary
    if check_order:
        if any(lines1[i][join_field1] > lines1[i + 1][join_field1] for i in range(len(lines1) - 1)):
            sys.stderr.write("Warning: File1 is not sorted on the join field.\n")
        if any(lines2[i][join_field2] > lines2[i + 1][join_field2] for i in range(len(lines2) - 1)):
            sys.stderr.write("Warning: File2 is not sorted on the join field.\n")

    # Join the lines
    result = join_lines(lines1, lines2)

    # Output the result
    for line in result:
        print(line)

def main():
    """
    Main entry point for the join command.
    """
    parser = argparse.ArgumentParser(description="Join lines of two files on a common field")
    parser.add_argument("file1", help="First input file")
    parser.add_argument("file2", help="Second input file")
    parser.add_argument("-1", "--field1", type=int, default=1, help="Join on this FIELD of file 1")
    parser.add_argument("-2", "--field2", type=int, default=1, help="Join on this FIELD of file 2")
    parser.add_argument("-t", "--delimiter", type=str, default=" ", help="Use CHAR as input and output field separator")
    parser.add_argument("-o", "--output", type=str, default="1,2", help="Output format: comma-separated FILENUM.FIELD specifications")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Ignore case when comparing fields")
    parser.add_argument("-e", "--missing", type=str, default="", help="Replace missing fields with STRING")
    parser.add_argument("-a", "--print-unpairable", type=int, choices=[1, 2], help="Print unpairable lines from file FILENUM (1 or 2)")
    parser.add_argument("--header", action="store_true", help="Treat first line as header")
    parser.add_argument("--check-order", action="store_true", help="Check that the input is sorted")
    parser.add_argument("--version", action="version", version="join.py 1.0", help="Output version information")

    args = parser.parse_args()

    # Parse output format
    output_format = args.output.split(',')

    # If header is set, treat the first lines as headers
    if args.header:
        sys.stderr.write("Warning: Treating first line as headers (no join attempt).\n")
        return

    # Join files
    join_files(
        args.file1, args.file2,
        join_field1=args.field1 - 1,  # Adjust for 0-indexed Python lists
        join_field2=args.field2 - 1,  # Adjust for 0-indexed Python lists
        delimiter=args.delimiter,
        output_format=output_format,
        ignore_case=args.ignore_case,
        missing_value=args.missing,
        header=args.header,
        check_order=args.check_order
    )

if __name__ == "__main__":
    main()

