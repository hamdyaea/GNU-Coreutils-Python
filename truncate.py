#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The truncate command from GNU coreutils in Python3.  
Example of use:  python3 truncate.py -s 100 file.txt
'''

import os
import sys
import argparse

def parse_size(size_str):
    """
    Parse size string with optional suffix (K, M, G, T, P, E, Z, Y)
    Returns size in bytes
    """
    if not size_str:
        return 0
        
    suffixes = {
        'K': 1024,
        'M': 1024**2,
        'G': 1024**3,
        'T': 1024**4,
        'P': 1024**5,
        'E': 1024**6,
        'Z': 1024**7,
        'Y': 1024**8
    }
    
    size_str = size_str.upper()
    
    # Handle +/- prefix for relative sizes
    multiplier = 1
    if size_str[0] in '+-':
        if size_str[0] == '-':
            multiplier = -1
        size_str = size_str[1:]
    
    # Parse numeric part and suffix
    if size_str[-1] in suffixes:
        number = float(size_str[:-1])
        bytes_size = int(number * suffixes[size_str[-1]])
    else:
        bytes_size = int(size_str)
    
    return bytes_size * multiplier

def truncate_file(file_path, size, reference=None, size_is_relative=False, no_create=False, no_error=False):
    """
    Truncate or extend a file to a specified size
    """
    try:
        # If using reference file
        if reference:
            try:
                ref_size = os.path.getsize(reference)
                final_size = ref_size
            except OSError as e:
                if not no_error:
                    print(f"truncate: error reading reference file '{reference}': {str(e)}", 
                          file=sys.stderr)
                return False
        else:
            current_size = 0
            if os.path.exists(file_path):
                current_size = os.path.getsize(file_path)
            
            if size_is_relative:
                final_size = current_size + size
            else:
                final_size = size

        # Check if file exists
        if not os.path.exists(file_path):
            if no_create:
                if not no_error:
                    print(f"truncate: '{file_path}': No such file", file=sys.stderr)
                return False
            # Create new file if it doesn't exist
            with open(file_path, 'w') as f:
                pass

        # Truncate or extend the file
        with open(file_path, 'a+b') as f:
            if final_size < 0:
                final_size = 0
            os.truncate(file_path, final_size)
        
        return True

    except (IOError, OSError) as e:
        if not no_error:
            print(f"truncate: '{file_path}': {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Shrink or extend the size of each FILE to the specified size',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
SIZE may be (or may be an integer optionally followed by) one of following:
  K =             1024
  M = K *         1024
  G = M *         1024
  T = G *         1024
  P = T *         1024
  E = P *         1024
  Z = E *         1024
  Y = Z *         1024
SIZE may also be prefixed by '+' or '-' to make it relative to current size.
        ''')
    
    parser.add_argument('files', nargs='+', help='File(s) to modify')
    parser.add_argument('-c', '--no-create', action='store_true',
                        help='do not create any files')
    parser.add_argument('-o', '--io-blocks', action='store_true',
                        help='treat SIZE as number of IO blocks instead of bytes')
    parser.add_argument('-r', '--reference', metavar='RFILE',
                        help='base size on RFILE')
    parser.add_argument('-s', '--size', metavar='SIZE',
                        help='set or adjust the file size by SIZE bytes')
    parser.add_argument('--no-preserve-root', action='store_true',
                        help='do not treat "/" specially')
    parser.add_argument('-n', '--no-error', action='store_true',
                        help='suppress error messages')

    args = parser.parse_args()

    # Validate arguments
    if not args.size and not args.reference:
        print("truncate: you must specify either '--size' or '--reference'", 
              file=sys.stderr)
        sys.exit(1)

    # Parse size
    size = 0
    size_is_relative = False
    if args.size:
        try:
            size = parse_size(args.size)
            size_is_relative = args.size[0] in '+-'
        except ValueError:
            print(f"truncate: invalid size: '{args.size}'", file=sys.stderr)
            sys.exit(1)

    # Process each file
    success = True
    for file_path in args.files:
        # Protect root directory
        if file_path == '/' and not args.no_preserve_root:
            print("truncate: refusing to process '/' without --no-preserve-root", 
                  file=sys.stderr)
            success = False
            continue

        if not truncate_file(
            file_path, 
            size, 
            args.reference,
            size_is_relative,
            args.no_create,
            args.no_error
        ):
            success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

