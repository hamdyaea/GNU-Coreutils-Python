#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description:  The sha224sum command from GNU coreutils in Python3.
Example of use: python3 sha224sum.py file.txt
'''

import sys
import hashlib

def compute_sha224sum(filename):
    """
    Compute SHA-224 hash of a file, identical to sha224sum command.
    
    Args:
        filename (str): Path to the file to hash
    
    Returns:
        str: SHA-224 hash in hexadecimal format
    """
    sha224_hash = hashlib.sha224()
    
    try:
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha224_hash.update(chunk)
        
        return f"{sha224_hash.hexdigest()}  {filename}"
    
    except FileNotFoundError:
        print(f"sha224sum: {filename}: No such file or directory", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"sha224sum: {filename}: Permission denied", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./sha224sum.py <file1> [file2 ...]", file=sys.stderr)
        sys.exit(1)
    
    for filename in sys.argv[1:]:
        print(compute_sha224sum(filename))

if __name__ == "__main__":
    main()
