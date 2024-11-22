#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description:  The numfmt command from GNU coreutils in Python3.
Example of use: python numfmt.py --to-suffix 1048576
'''

import sys
import argparse
import re

class NumberFormatter:
    def __init__(self, options):
        """
        Initialize NumberFormatter with specified options.
        
        Args:
            options (Namespace): Parsed command-line arguments
        """
        self.options = options

    def format_number(self, number):
        """
        Format number based on specified options.
        
        Args:
            number (str or float): Number to format
        
        Returns:
            str: Formatted number
        """
        try:
            # Convert to float if possible
            num = float(number)
        except ValueError:
            return number  # Return original if not a valid number
        
        # Apply to/from options
        if self.options.to_unit:
            num = self._convert_to_unit(num)
        
        if self.options.from_unit:
            num = self._convert_from_unit(num)
        
        # Apply formatting options
        if self.options.to_suffix:
            return self._apply_suffix_format(num)
        
        if self.options.format:
            return self._apply_custom_format(num)
        
        # Default formatting
        return self._default_format(num)

    def _convert_to_unit(self, num):
        """
        Convert number to specified unit.
        
        Args:
            num (float): Input number
        
        Returns:
            float: Converted number
        """
        units = {
            'K': 1024, 'M': 1024**2, 'G': 1024**3, 
            'T': 1024**4, 'P': 1024**5
        }
        return num / units.get(self.options.to_unit.upper(), 1)

    def _convert_from_unit(self, num):
        """
        Convert number from specified unit.
        
        Args:
            num (float): Input number
        
        Returns:
            float: Converted number
        """
        units = {
            'K': 1024, 'M': 1024**2, 'G': 1024**3, 
            'T': 1024**4, 'P': 1024**5
        }
        return num * units.get(self.options.from_unit.upper(), 1)

    def _apply_suffix_format(self, num):
        """
        Format number with SI/IEC suffixes.
        
        Args:
            num (float): Input number
        
        Returns:
            str: Formatted number with suffix
        """
        units = [
            (1024**5, 'P'), (1024**4, 'T'), 
            (1024**3, 'G'), (1024**2, 'M'), 
            (1024, 'K')
        ]
        
        for divisor, suffix in units:
            if abs(num) >= divisor:
                value = num / divisor
                return f"{value:.1f}{suffix}"
        
        return f"{num:.1f}"

    def _apply_custom_format(self, num):
        """
        Apply custom formatting based on format specifier.
        
        Args:
            num (float): Input number
        
        Returns:
            str: Formatted number
        """
        return self.options.format.format(num)

    def _default_format(self, num):
        """
        Apply default number formatting.
        
        Args:
            num (float): Input number
        
        Returns:
            str: Formatted number
        """
        return f"{num}"

def main():
    """
    Main function to handle number formatting.
    """
    parser = argparse.ArgumentParser(description='Number formatting utility')
    
    # Conversion options
    parser.add_argument('--to', dest='to_unit', 
                        choices=['K', 'M', 'G', 'T', 'P'], 
                        help='Convert to specified unit')
    parser.add_argument('--from', dest='from_unit', 
                        choices=['K', 'M', 'G', 'T', 'P'], 
                        help='Convert from specified unit')
    
    # Formatting options
    parser.add_argument('--to-suffix', action='store_true', 
                        help='Convert to human-readable suffix')
    parser.add_argument('--format', 
                        help='Custom formatting (e.g., "{:.2f}")')
    
    # Input source
    parser.add_argument('numbers', nargs='*', 
                        help='Numbers to format')
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), 
                        help='Input file with numbers')
    
    args = parser.parse_args()
    
    # Determine input source
    if args.file:
        numbers = args.file.read().split()
    elif args.numbers:
        numbers = args.numbers
    else:
        numbers = sys.stdin.read().split()
    
    # Create formatter
    formatter = NumberFormatter(args)
    
    # Process and output numbers
    try:
        for number in numbers:
            print(formatter.format_number(number))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
