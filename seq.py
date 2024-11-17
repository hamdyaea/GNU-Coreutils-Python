#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: the seq command from GNU coreutils in Python3.  
Example of use: python3 seq.py 1 10
'''

import argparse
import sys

def generate_sequence(first, increment, last, format_str, separator, equal_width):
    """Generate the sequence from FIRST to LAST with the given INCREMENT."""
    # Handle cases where FIRST, INCREMENT, or LAST are not provided
    if increment == 0:
        raise ValueError("INCREMENT must not be zero.")
    
    numbers = []
    current = first
    
    while (increment > 0 and current <= last) or (increment < 0 and current >= last):
        numbers.append(current)
        current += increment
    
    # Format the numbers if needed
    formatted_numbers = []
    for num in numbers:
        try:
            # If format is provided, use the format string
            formatted_numbers.append(f"{num:{format_str}}")
        except ValueError:
            # In case of an invalid format, fallback to a default
            formatted_numbers.append(str(num))
    
    # If equal-width is specified, equalize width by padding with leading zeros
    if equal_width:
        max_length = max(len(str(int(num))) for num in numbers)  # Get max length of integer part
        formatted_numbers = [f"{int(num):0{max_length}d}" for num in numbers]
    
    # Join the numbers with the specified separator and print the result
    print(separator.join(formatted_numbers))

def main():
    parser = argparse.ArgumentParser(description="Print a sequence of numbers from FIRST to LAST with an optional INCREMENT.")
    
    # Define arguments
    parser.add_argument('first', type=float, nargs='?', default=1, help="The starting value (default: 1).")
    parser.add_argument('last', type=float, help="The ending value.")
    parser.add_argument('increment', type=float, nargs='?', default=1, help="The increment (default: 1).")
    
    parser.add_argument('-f', '--format', default='%g', help="Format for floating-point numbers (default: %g).")
    parser.add_argument('-s', '--separator', default='\n', help="Use STRING to separate numbers (default: '\\n').")
    parser.add_argument('-w', '--equal-width', action='store_true', help="Equalize width by padding with leading zeros.")
    parser.add_argument('--version', action='version', version="seq.py 1.0", help="Output version information and exit.")
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        generate_sequence(args.first, args.increment, args.last, args.format, args.separator, args.equal_width)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

