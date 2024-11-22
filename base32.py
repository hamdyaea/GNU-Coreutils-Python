#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description: The base32 command from GNU coreutils in Python3.  
Example of use: python base32.py -e "Hello, World!"
'''
#!/usr/bin/env python3

import sys
import argparse
import base64

def base32_encode(input_data):
    """
    Encode input data to Base32.
    
    Args:
        input_data (bytes or str): Data to encode
    
    Returns:
        str: Base32 encoded string
    """
    if isinstance(input_data, str):
        input_data = input_data.encode('utf-8')
    
    return base64.b32encode(input_data).decode('utf-8')

def base32_decode(input_data):
    """
    Decode Base32 encoded data.
    
    Args:
        input_data (str): Base32 encoded string
    
    Returns:
        bytes: Decoded data
    """
    # Pad input if necessary
    input_data = input_data.upper()
    padding_needed = (8 - len(input_data) % 8) % 8
    input_data += '=' * padding_needed
    
    return base64.b32decode(input_data)

def main():
    """
    Command-line interface for Base32 encoding/decoding.
    """
    parser = argparse.ArgumentParser(description='Base32 encoding and decoding utility')
    
    # Mutually exclusive encoding/decoding group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encode', action='store_true', 
                       help='Encode input to Base32')
    group.add_argument('-d', '--decode', action='store_true', 
                       help='Decode Base32 input')
    
    # Input source options
    parser.add_argument('input', nargs='?', type=str, 
                        default=None, help='Input string or file')
    parser.add_argument('-f', '--file', action='store_true', 
                        help='Treat input as file path')
    
    # Output options
    parser.add_argument('-o', '--output', type=str, 
                        help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Determine input source
    if args.file and args.input:
        try:
            with open(args.input, 'rb') as f:
                input_data = f.read()
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.input:
        input_data = args.input
    else:
        # Read from stdin if no input provided
        input_data = sys.stdin.read().strip()
    
    # Perform encoding or decoding
    try:
        if args.encode:
            result = base32_encode(input_data)
        else:
            result = base32_decode(input_data).decode('utf-8')
        
        # Output handling
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
        else:
            print(result)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
