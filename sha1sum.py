#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  22-11-2024
Last update: 22-11-2024
Version: 1.0
Description: The sha1sum command from GNU coreutils in Python3.  
Example of use:  python sha1sum.py file1.txt
'''


import sys
import argparse
import hashlib
from pathlib import Path

def calculate_sha1(file_path, binary_output=False):
    """
    Calculate SHA1 hash for a given file.
    
    Args:
        file_path (Path): Path to the file
        binary_output (bool): Whether to output binary hash
    
    Returns:
        tuple: (hash_value, error_message)
    """
    try:
        sha1_hash = hashlib.sha1()
        
        with open(file_path, 'rb') as file:
            # Read in chunks for memory efficiency
            for chunk in iter(lambda: file.read(4096), b''):
                sha1_hash.update(chunk)
        
        # Return hash in requested format
        return (sha1_hash.digest() if binary_output 
                else sha1_hash.hexdigest()), None
    
    except Exception as e:
        return None, str(e)

def main():
    """
    Main function to handle SHA1 hash calculation.
    """
    parser = argparse.ArgumentParser(description='Calculate SHA1 hash sums')
    
    # Input files and modes
    parser.add_argument('files', nargs='+', type=Path, 
                        help='Files to calculate hash sums')
    parser.add_argument('-b', '--binary', 
                        action='store_true', 
                        help='Print binary digest')
    parser.add_argument('--check', 
                        action='store_true', 
                        help='Read checksums and verify')
    parser.add_argument('-q', '--quiet', 
                        action='store_true', 
                        help='Suppress OK/FAILED output')
    
    args = parser.parse_args()
    
    # Verify mode
    if args.check:
        check_files(args.files, args.quiet)
        return
    
    # Hash calculation mode
    for file_path in args.files:
        if not file_path.exists():
            print(f"{file_path}: No such file", file=sys.stderr)
            continue
        
        hash_value, error = calculate_sha1(file_path, args.binary)
        
        if error:
            print(f"Error processing {file_path}: {error}", file=sys.stderr)
        elif args.binary:
            sys.stdout.buffer.write(hash_value)
        else:
            print(f"{hash_value}  {file_path}")

def check_files(checksum_files, quiet=False):
    """
    Verify checksums from files.
    
    Args:
        checksum_files (list): List of files containing checksums
        quiet (bool): Suppress detailed output
    """
    for checksum_file in checksum_files:
        try:
            with open(checksum_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    try:
                        # Parse standard checksum file format
                        stored_hash, filename = line.split('  ', 1)
                        file_path = Path(filename)
                        
                        # Skip non-existent files
                        if not file_path.exists():
                            if not quiet:
                                print(f"{filename}: FAILED open")
                            continue
                        
                        # Calculate current hash
                        current_hash, error = calculate_sha1(file_path)
                        
                        # Compare hashes
                        if error:
                            if not quiet:
                                print(f"{filename}: FAILED (error: {error})")
                        elif current_hash == stored_hash:
                            if not quiet:
                                print(f"{filename}: OK")
                        else:
                            if not quiet:
                                print(f"{filename}: FAILED")
                    
                    except ValueError:
                        print(f"Invalid line format in {checksum_file}")
        
        except Exception as e:
            print(f"Error reading {checksum_file}: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
