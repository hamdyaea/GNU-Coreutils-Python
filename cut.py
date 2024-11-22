#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description: The cut command from GNU coreutils in Python3.  
Example of use: python cut.py -c 1-3 file.txt
'''

import sys
import argparse

class CutCommand:
    def __init__(self, mode, fields, delimiter='\t', suppress_non_delimited=False):
        """
        Initialize Cut command with specified parameters.
        
        Args:
            mode (str): 'bytes', 'chars', or 'fields'
            fields (list): List of field/character ranges to extract
            delimiter (str): Field delimiter
            suppress_non_delimited (bool): Suppress lines without delimiter
        """
        self.mode = mode
        self.fields = self._parse_ranges(fields)
        self.delimiter = delimiter
        self.suppress_non_delimited = suppress_non_delimited

    def _parse_ranges(self, ranges):
        """
        Parse field/character ranges.
        
        Args:
            ranges (list): List of range strings
        
        Returns:
            list: Parsed and validated ranges
        """
        parsed_ranges = []
        for range_str in ranges:
            try:
                if '-' in range_str:
                    start, end = map(int, range_str.split('-'))
                    parsed_ranges.append((start, end))
                else:
                    parsed_ranges.append((int(range_str), int(range_str)))
            except ValueError:
                raise ValueError(f"Invalid range: {range_str}")
        return parsed_ranges

    def process_line(self, line):
        """
        Process a single line based on mode and ranges.
        
        Args:
            line (str): Input line to process
        
        Returns:
            str: Processed line or None
        """
        # Decode if bytes, strip newline
        if isinstance(line, bytes):
            line = line.decode('utf-8').rstrip('\n')

        if self.mode == 'fields':
            return self._process_fields(line)
        elif self.mode in ['bytes', 'chars']:
            return self._process_chars(line)
        
        return line

    def _process_fields(self, line):
        """
        Process line by extracting specified fields.
        
        Args:
            line (str): Input line
        
        Returns:
            str: Processed line or None
        """
        # Check delimiter
        parts = line.split(self.delimiter)
        
        # Suppress non-delimited lines if required
        if self.suppress_non_delimited and len(parts) < 2:
            return None

        # Extract fields
        selected_fields = []
        for start, end in self.fields:
            # Adjust for 0-based indexing
            start -= 1
            end = min(end, len(parts))
            
            selected_fields.extend(parts[start:end])

        return self.delimiter.join(selected_fields)

    def _process_chars(self, line):
        """
        Process line by extracting specified characters.
        
        Args:
            line (str): Input line
        
        Returns:
            str: Processed line
        """
        result = []
        for start, end in self.fields:
            # Adjust for 0-based indexing
            start -= 1
            # Extract characters
            result.append(line[start:end])
        
        return ''.join(result)

def main():
    """
    Main function to handle cut command functionality.
    """
    parser = argparse.ArgumentParser(description='Cut out selected portions of each line of files')
    
    # Mutually exclusive selection modes
    selection_group = parser.add_mutually_exclusive_group(required=True)
    selection_group.add_argument('-b', '--bytes', 
                                 help='Select only these bytes')
    selection_group.add_argument('-c', '--characters', 
                                 help='Select only these characters')
    selection_group.add_argument('-f', '--fields', 
                                 help='Select only these fields')
    
    # Additional options
    parser.add_argument('-d', '--delimiter', 
                        default='\t', 
                        help='Use DELIM instead of TAB for field delimiter')
    parser.add_argument('-s', '--only-delimited', 
                        action='store_true', 
                        help='Suppress lines with no delimiter')
    parser.add_argument('files', nargs='*', 
                        type=argparse.FileType('rb'), 
                        default=[sys.stdin.buffer], 
                        help='Input files (default: stdin)')
    
    args = parser.parse_args()
    
    # Determine mode and create CutCommand instance
    if args.bytes:
        cut_command = CutCommand('bytes', args.bytes.split(','))
    elif args.characters:
        cut_command = CutCommand('chars', args.characters.split(','))
    elif args.fields:
        cut_command = CutCommand('fields', 
                                 args.fields.split(','), 
                                 delimiter=args.delimiter, 
                                 suppress_non_delimited=args.only_delimited)
    
    # Process input files
    try:
        for file in args.files:
            for line in file:
                processed_line = cut_command.process_line(line)
                if processed_line is not None:
                    print(processed_line)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
