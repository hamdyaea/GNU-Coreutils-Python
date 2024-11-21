#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  21-11-2024
Last update: 21-11-2024
Version: 1.0
Description: The b2sum command from GNU coreutils in Python3.  
Example of use: python b2sum.py file.txt
'''


import sys
import argparse
from hashlib import blake2b
from pathlib import Path

def calculate_b2sum(file_path, hash_length=None):
    """
    Calculate BLAKE2b hash sum of a file.
    
    Args:
        file_path (Path): Path to the file to hash
        hash_length (int, optional): Length of the hash digest in bytes (default: 64)
    
    Returns:
        tuple: (hash_hex_string, error_message)
    """
    try:
        # Create BLAKE2b hash object with specified digest size
        if hash_length:
            hasher = blake2b(digest_size=hash_length)
        else:
            hasher = blake2b()
        
        # Read and update hash in chunks for memory efficiency
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):  # 8KB chunks
                hasher.update(chunk)
                
        return hasher.hexdigest(), None
        
    except Exception as e:
        return None, f"Error processing {file_path}: {str(e)}"

def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description='Calculate BLAKE2b hash sums of files.'
    )
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Files to calculate hash sums for'
    )
    parser.add_argument(
        '-l', '--length',
        type=int,
        help='Length of hash in bytes (default: 64)',
        default=None
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Read checksums from files and check them'
    )

    args = parser.parse_args()

    # Check mode
    if args.check:
        check_files(args.files)
        return

    # Hash calculation mode
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: {file_path} does not exist", file=sys.stderr)
            continue

        hash_value, error = calculate_b2sum(file_path, args.length)
        
        if error:
            print(error, file=sys.stderr)
        else:
            print(f"{hash_value}  {file_path}")

def check_files(checksum_files):
    """
    Verify checksums stored in files.
    
    Args:
        checksum_files (list): List of files containing checksums to verify
    """
    for checksum_file in checksum_files:
        try:
            with open(checksum_file, 'r') as f:
                for line in f:
                    # Parse checksum file format: <hash>  <filename>
                    try:
                        stored_hash, filename = line.strip().split('  ', 1)
                        file_path = Path(filename)
                        
                        if not file_path.exists():
                            print(f"{filename}: FAILED (file not found)")
                            continue
                            
                        calculated_hash, error = calculate_b2sum(file_path)
                        
                        if error:
                            print(f"{filename}: FAILED ({error})")
                        elif calculated_hash == stored_hash:
                            print(f"{filename}: OK")
                        else:
                            print(f"{filename}: FAILED (hash mismatch)")
                            
                    except ValueError:
                        print(f"Invalid line format in {checksum_file}")
                        
        except Exception as e:
            print(f"Error reading {checksum_file}: {str(e)}", file=sys.stderr)

if __name__ == '__main__':
    main()
