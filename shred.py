#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The shred command from GNU coreutils in Python3  
Example of use: python3 shred.py file.txt  
'''

import os
import sys
import random
import argparse
import stat
from pathlib import Path

class FileShredder:
    def __init__(self, passes=3, zeros=True, remove=True, force=False, 
                 exact=False, verbose=False, size=None):
        self.passes = passes
        self.zeros = zeros
        self.remove = remove
        self.force = force
        self.exact = exact
        self.verbose = verbose
        self.size = size
        self.random = random.SystemRandom()  # Cryptographically secure RNG
        
    def _get_random_bytes(self, size):
        """Generate cryptographically secure random bytes."""
        return bytes(self.random.randint(0, 255) for _ in range(size))
        
    def _make_file_writable(self, path):
        """Make file writable if necessary."""
        try:
            mode = os.stat(path).st_mode
            if not mode & stat.S_IWUSR:
                os.chmod(path, mode | stat.S_IWUSR)
            return True
        except OSError:
            return False
            
    def _get_file_size(self, path):
        """Get file size, handling special files."""
        try:
            if self.size is not None:
                return self.size
            
            if self.exact:
                # Use actual file size for exact mode
                return os.path.getsize(path)
            else:
                # Round up to nearest block size
                size = os.path.getsize(path)
                block_size = 512  # Standard block size
                return ((size + block_size - 1) // block_size) * block_size
        except OSError:
            return 0
            
    def _secure_remove(self, path):
        """Securely remove the file using various techniques."""
        try:
            # First try to overwrite the filename
            dir_path = os.path.dirname(path)
            if not dir_path:
                dir_path = '.'
            
            # Generate random name with same length
            original_name = os.path.basename(path)
            random_name = ''.join(chr(self.random.randint(ord('A'), ord('Z'))) 
                                for _ in range(len(original_name)))
            random_path = os.path.join(dir_path, random_name)
            
            # Rename file
            try:
                os.rename(path, random_path)
                path = random_path
            except OSError:
                if self.verbose:
                    print(f"shred: warning: could not rename '{path}'", 
                          file=sys.stderr)
            
            # Remove the file
            os.unlink(path)
            return True
            
        except OSError as e:
            if self.verbose:
                print(f"shred: error removing '{path}': {str(e)}", 
                      file=sys.stderr)
            return False
            
    def shred_file(self, path):
        """Shred a single file."""
        if not self.force and not os.path.exists(path):
            print(f"shred: '{path}': No such file or directory", 
                  file=sys.stderr)
            return False
            
        # Check if file is writable or make it writable
        if not os.access(path, os.W_OK):
            if not self.force or not self._make_file_writable(path):
                print(f"shred: '{path}': Permission denied", file=sys.stderr)
                return False
                
        size = self._get_file_size(path)
        if size == 0:
            if self.verbose:
                print(f"shred: '{path}': file empty or error reading", 
                      file=sys.stderr)
            return False
            
        try:
            # Perform overwrite passes
            for pass_num in range(self.passes):
                if self.verbose:
                    print(f"shred: '{path}': pass {pass_num+1}/{self.passes}", 
                          file=sys.stderr)
                    
                with open(path, 'wb') as f:
                    # Write in chunks to handle large files
                    chunk_size = min(size, 1024 * 1024)  # 1MB chunks
                    remaining = size
                    
                    while remaining > 0:
                        write_size = min(remaining, chunk_size)
                        f.write(self._get_random_bytes(write_size))
                        remaining -= write_size
                        
                    # Ensure data is written to disk
                    f.flush()
                    os.fsync(f.fileno())
                    
            # Final pass with zeros if requested
            if self.zeros:
                if self.verbose:
                    print(f"shred: '{path}': final zero pass", file=sys.stderr)
                    
                with open(path, 'wb') as f:
                    remaining = size
                    while remaining > 0:
                        write_size = min(remaining, chunk_size)
                        f.write(b'\0' * write_size)
                        remaining -= write_size
                    f.flush()
                    os.fsync(f.fileno())
                    
            # Remove file if requested
            if self.remove:
                if self.verbose:
                    print(f"shred: '{path}': removing", file=sys.stderr)
                self._secure_remove(path)
                
            return True
            
        except OSError as e:
            print(f"shred: error writing '{path}': {str(e)}", file=sys.stderr)
            return False

def parse_size(size_str):
    """Parse size string with optional suffix (K, M, G)."""
    suffixes = {
        'K': 1024,
        'M': 1024**2,
        'G': 1024**3
    }
    
    size_str = size_str.upper()
    if size_str[-1] in suffixes:
        try:
            number = float(size_str[:-1])
            return int(number * suffixes[size_str[-1]])
        except ValueError:
            return None
    try:
        return int(size_str)
    except ValueError:
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Overwrite files to hide their contents and optionally delete them',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
SIZE may be (or may be an integer optionally followed by) one of following:
  K =             1024 (KiB)
  M = K *         1024 (MiB)
  G = M *         1024 (GiB)
        ''')
    
    parser.add_argument('files', nargs='+', help='File(s) to shred')
    parser.add_argument('-f', '--force', action='store_true',
                        help='change permissions to allow writing if necessary')
    parser.add_argument('-n', '--iterations', type=int, default=3,
                        help='overwrite N times instead of the default (3)')
    parser.add_argument('-s', '--size', metavar='SIZE',
                        help='shred this many bytes (suffixes K, M, G accepted)')
    parser.add_argument('-u', '--remove', action='store_true',
                        help='truncate and remove file after overwriting')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show progress')
    parser.add_argument('-x', '--exact', action='store_true',
                        help='do not round file sizes up to full blocks')
    parser.add_argument('-z', '--zero', action='store_true',
                        help='add a final overwrite with zeros to hide shredding')
    
    args = parser.parse_args()
    
    # Validate iterations
    if args.iterations < 1:
        print("shred: invalid number of passes", file=sys.stderr)
        sys.exit(1)
        
    # Parse size if provided
    size = None
    if args.size:
        size = parse_size(args.size)
        if size is None:
            print(f"shred: invalid size: '{args.size}'", file=sys.stderr)
            sys.exit(1)
    
    # Create shredder instance
    shredder = FileShredder(
        passes=args.iterations,
        zeros=args.zero,
        remove=args.remove,
        force=args.force,
        exact=args.exact,
        verbose=args.verbose,
        size=size
    )
    
    # Process all files
    success = True
    for file_path in args.files:
        if not shredder.shred_file(file_path):
            success = False
            
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
