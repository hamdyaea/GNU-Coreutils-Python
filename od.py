#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description:  The od command from GNU coreutils in Python3.
Example of use: python od.py file.txt
'''

import sys
import argparse
import binascii
import string

class OctalDumper:
    def __init__(self, options):
        """
        Initialize OctalDumper with specified options.
        
        Args:
            options (Namespace): Parsed command-line arguments
        """
        self.options = options
    
    def format_output(self, data):
        """
        Format input data based on specified output type.
        
        Args:
            data (bytes): Input data to dump
        
        Returns:
            list: Formatted output lines
        """
        if self.options.format == 'o':
            return self._format_octal(data)
        elif self.options.format == 'x':
            return self._format_hex(data)
        elif self.options.format == 'c':
            return self._format_char(data)
        elif self.options.format == 'd':
            return self._format_decimal(data)
        else:
            return self._format_octal(data)
    
    def _format_octal(self, data):
        """
        Format data in octal representation.
        
        Args:
            data (bytes): Input data
        
        Returns:
            list: Formatted octal output lines
        """
        output = []
        offset = 0
        
        while offset < len(data):
            # Get chunk of data
            chunk = data[offset:offset+self.options.width]
            
            # Format offset
            offset_str = f"{offset:07o}"
            
            # Format bytes
            byte_str = ' '.join(f"{b:03o}" for b in chunk)
            
            # Pad byte string if needed
            byte_str = byte_str.ljust(3 * self.options.width)
            
            output.append(f"{offset_str} {byte_str}")
            offset += self.options.width
        
        return output
    
    def _format_hex(self, data):
        """
        Format data in hexadecimal representation.
        
        Args:
            data (bytes): Input data
        
        Returns:
            list: Formatted hex output lines
        """
        output = []
        offset = 0
        
        while offset < len(data):
            # Get chunk of data
            chunk = data[offset:offset+self.options.width]
            
            # Format offset
            offset_str = f"{offset:07o}"
            
            # Format bytes
            byte_str = ' '.join(f"{b:02x}" for b in chunk)
            
            # Pad byte string if needed
            byte_str = byte_str.ljust(3 * self.options.width)
            
            output.append(f"{offset_str} {byte_str}")
            offset += self.options.width
        
        return output
    
    def _format_char(self, data):
        """
        Format data in character representation.
        
        Args:
            data (bytes): Input data
        
        Returns:
            list: Formatted character output lines
        """
        output = []
        offset = 0
        
        while offset < len(data):
            # Get chunk of data
            chunk = data[offset:offset+self.options.width]
            
            # Format offset
            offset_str = f"{offset:07o}"
            
            # Format characters
            char_str = []
            for b in chunk:
                if b in range(32, 127):
                    char_str.append(chr(b))
                else:
                    char_str.append('.')
            
            char_output = ''.join(char_str)
            output.append(f"{offset_str} {char_output}")
            offset += self.options.width
        
        return output
    
    def _format_decimal(self, data):
        """
        Format data in decimal representation.
        
        Args:
            data (bytes): Input data
        
        Returns:
            list: Formatted decimal output lines
        """
        output = []
        offset = 0
        
        while offset < len(data):
            # Get chunk of data
            chunk = data[offset:offset+self.options.width]
            
            # Format offset
            offset_str = f"{offset:07o}"
            
            # Format bytes
            byte_str = ' '.join(f"{b}" for b in chunk)
            
            # Pad byte string if needed
            byte_str = byte_str.ljust(3 * self.options.width)
            
            output.append(f"{offset_str} {byte_str}")
            offset += self.options.width
        
        return output

def main():
    """
    Main function to handle octal dump functionality.
    """
    parser = argparse.ArgumentParser(description='Dump files in octal and other formats')
    
    # Format options
    parser.add_argument('-t', dest='format', 
                        choices=['o', 'x', 'c', 'd'], 
                        default='o', 
                        help='Output format: o (octal), x (hex), c (char), d (decimal)')
    
    # Width options
    parser.add_argument('-w', '--width', type=int, 
                        default=16, 
                        help='Bytes per output line')
    
    # Input source
    parser.add_argument('files', nargs='*', 
                        type=argparse.FileType('rb'), 
                        default=[sys.stdin.buffer], 
                        help='Files to dump (default: stdin)')
    
    args = parser.parse_args()
    
    # Create dumper
    dumper = OctalDumper(args)
    
    # Process input files
    try:
        for file in args.files:
            # Read entire file
            data = file.read()
            
            # Format and print output
            output_lines = dumper.format_output(data)
            for line in output_lines:
                print(line)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
