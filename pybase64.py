#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The base64 GNU coreutils command in Python3.  
Example of use: python3 base64 input.txt
'''
import argparse
import base64
import sys

VERSION = "1.0"

def encode_file(file, wrap_length=76):
    """
    Encode the contents of the file in base64 and print to standard output.
    """
    with open(file, "rb") as f:
        data = f.read()
        # Correct use of base64 encoding
        encoded_data = base64.b64encode(data).decode("utf-8")

        # Wrap encoded data to the specified wrap length
        if wrap_length > 0:
            wrapped_data = "\n".join([encoded_data[i:i + wrap_length] for i in range(0, len(encoded_data), wrap_length)])
            print(wrapped_data)
        else:
            print(encoded_data)

def decode_file(file, ignore_garbage=False):
    """
    Decode the base64 encoded file and print to standard output.
    """
    with open(file, "r") as f:
        data = f.read()

        # Decode data, ignoring non-alphabet characters if --ignore-garbage is set
        if ignore_garbage:
            data = "".join([c for c in data if c.isalnum() or c in '+/='])
        
        decoded_data = base64.b64decode(data)

        # Print decoded data as text
        sys.stdout.buffer.write(decoded_data)

def process_input_data(is_decode, ignore_garbage, wrap_length, file):
    """
    Process data depending on whether encoding or decoding is requested.
    """
    if is_decode:
        decode_file(file, ignore_garbage)
    else:
        encode_file(file, wrap_length)

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Base64 encode or decode data and print to standard output."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="-",
        help="File to encode or decode (default is standard input).",
    )
    parser.add_argument(
        "-d", "--decode", action="store_true", help="Decode data."
    )
    parser.add_argument(
        "-i", "--ignore-garbage", action="store_true", help="Ignore non-alphabet characters when decoding."
    )
    parser.add_argument(
        "-w", "--wrap", type=int, default=76, help="Wrap encoded lines after COLS characters (default 76). Use 0 to disable line wrapping."
    )
    parser.add_argument(
        "--version", action="version", version=f"base64.py {VERSION}", help="Output version information and exit."
    )

    args = parser.parse_args()

    if args.file == "-":
        # Reading from standard input if no file is specified
        if args.decode:
            data = sys.stdin.read()
            # Decode from input
            decoded_data = base64.b64decode(data)
            sys.stdout.buffer.write(decoded_data)
        else:
            data = sys.stdin.read()
            # Encode input data
            encoded_data = base64.b64encode(data.encode()).decode("utf-8")
            sys.stdout.write(encoded_data)
    else:
        # Use specified file
        process_input_data(args.decode, args.ignore_garbage, args.wrap, args.file)


if __name__ == "__main__":
    main()

