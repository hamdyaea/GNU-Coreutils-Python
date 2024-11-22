#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description: The sha256sum command from GNU coreutils in Python3.  
Example of use: python3 sha256sum.py file.txt
'''

import sys
import hashlib

def compute_sha256sum(filename):
    """
    Compute SHA-256 hash of a file, identical to sha256sum command.
    
    Args:
        filename (str): Path to the file to hash
    
    Returns:
        str: SHA-256 hash in hexadecimal format
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256_hash.update(chunk)
        
        return f"{sha256_hash.hexdigest()}  {filename}"
    
    except FileNotFoundError:
        print(f"sha256sum: {filename}: No such file or directory", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"sha256sum: {filename}: Permission denied", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: ./sha256sum.py <file1> [file2 ...]", file=sys.stderr)
        sys.exit(1)
    
    for filename in sys.argv[1:]:
        print(compute_sha256sum(filename))

if __name__ == "__main__":
    main()
