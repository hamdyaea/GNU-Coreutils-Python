#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The base64 command from GNU coreutils in Python3.  
Example of use: echo "Hello World" | python3 pybase64.py
'''


import sys
import base64
import argparse
from typing import BinaryIO, Optional

class Base64Tool:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.wrap_column = args.wrap if args.wrap != 0 else None
        self.buffer_size = 8192  # Read buffer size for efficient processing

    def process_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Process input stream and write to output stream."""
        try:
            if self.args.decode:
                self._decode_stream(input_stream, output_stream)
            else:
                self._encode_stream(input_stream, output_stream)
        except (base64.binascii.Error, UnicodeDecodeError) as e:
            print(f"base64: invalid input: {str(e)}", file=sys.stderr)
            sys.exit(1)

    def _encode_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Encode binary input stream to base64."""
        # Initialize variables for line wrapping
        current_line_length = 0
        
        while True:
            chunk = input_stream.read(self.buffer_size)
            if not chunk:
                break

            # Encode chunk
            encoded = base64.b64encode(chunk)
            
            # Handle line wrapping
            if self.wrap_column is not None:
                # Process the encoded data in parts to maintain line length
                encoded_str = encoded.decode('ascii')
                while encoded_str:
                    available_space = self.wrap_column - current_line_length
                    if available_space <= 0:
                        output_stream.write(b'\n')
                        current_line_length = 0
                        available_space = self.wrap_column
                    
                    # Write as much as fits on the current line
                    part = encoded_str[:available_space]
                    output_stream.write(part.encode('ascii'))
                    encoded_str = encoded_str[available_space:]
                    current_line_length += len(part)
            else:
                # Write without wrapping
                output_stream.write(encoded)
        
        # Add final newline if we were wrapping
        if self.wrap_column is not None and current_line_length > 0:
            output_stream.write(b'\n')

    def _decode_stream(self, input_stream: BinaryIO, output_stream: BinaryIO) -> None:
        """Decode base64 input stream to binary."""
        # For decoding, we need to accumulate the entire input to handle
        # potential line breaks and padding correctly
        encoded_data = b''
        
        for line in input_stream:
            # Skip empty lines
            if not line.strip():
                continue
            encoded_data += line.strip()
        
        # Handle padding if missing
        missing_padding = len(encoded_data) % 4
        if missing_padding:
            encoded_data += b'=' * (4 - missing_padding)
        
        # Decode and write
        decoded_data = base64.b64decode(encoded_data)
        output_stream.write(decoded_data)

    def process_files(self) -> None:
        """Process input and output files based on command line arguments."""
        try:
            # Handle input file
            if self.args.input_file and self.args.input_file != '-':
                with open(self.args.input_file, 'rb') as infile:
                    if self.args.output_file and self.args.output_file != '-':
                        with open(self.args.output_file, 'wb') as outfile:
                            self.process_stream(infile, outfile)
                    else:
                        self.process_stream(infile, sys.stdout.buffer)
            else:
                if self.args.output_file and self.args.output_file != '-':
                    with open(self.args.output_file, 'wb') as outfile:
                        self.process_stream(sys.stdin.buffer, outfile)
                else:
                    self.process_stream(sys.stdin.buffer, sys.stdout.buffer)
        
        except IOError as e:
            print(f"base64: {str(e)}", file=sys.stderr)
            sys.exit(1)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='base64 encode or decode FILE, or standard input, to standard output.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  base64.py file        Encode FILE to standard output
  base64.py -d file     Decode FILE to standard output
  base64.py -w 76 file  Encode FILE with line wrapping at column 76'''
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='input file (default: stdin)',
        default='-'
    )
    
    parser.add_argument(
        '-d', '--decode',
        action='store_true',
        help='decode data'
    )
    
    parser.add_argument(
        '-i', '--ignore-garbage',
        action='store_true',
        help='when decoding, ignore non-alphabet characters'
    )
    
    parser.add_argument(
        '-w', '--wrap',
        type=int,
        default=76,
        help='wrap encoded lines after COLS character (default 76, 0 to disable wrapping)'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='output file (default: stdout)',
        default='-'
    )

    return parser.parse_args()

def main() -> None:
    """Main program entry point."""
    args = parse_arguments()
    base64_tool = Base64Tool(args)
    base64_tool.process_files()

if __name__ == '__main__':
    main()
