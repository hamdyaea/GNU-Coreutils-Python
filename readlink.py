#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The readlink command from GNU coreutils in Python3.  
Example of use: python3 readlink.py /path/to/symlink
'''

import os
import sys

def readlink_command(paths, options):
    """
    Resolve symbolic links and print their target
    
    Options:
    -f, --canonicalize: Canonicalize by following every symlink
    -n, --no-newline: Do not print a newline
    -e, --exist: Exit with 0 if the link exists
    -m: Do not require link to exist
    """
    for path in paths:
        try:
            # Handle different options
            if '-f' in options or '--canonicalize' in options:
                # Fully resolve the path, following all symlinks
                resolved_path = os.path.realpath(path)
                print(resolved_path, end='' if '-n' in options else '\n')
            
            elif '-e' in options or '--exist' in options:
                # Check if link exists
                if os.path.exists(path) and os.path.islink(path):
                    print(os.readlink(path), end='' if '-n' in options else '\n')
                    sys.exit(0)
                sys.exit(1)
            
            elif '-m' in options:
                # Resolve link without checking existence
                resolved_path = os.readlink(path)
                print(resolved_path, end='' if '-n' in options else '\n')
            
            else:
                # Default behavior: read link target
                link_target = os.readlink(path)
                print(link_target, end='' if '-n' in options else '\n')
        
        except FileNotFoundError:
            print(f"readlink: {path}: No such file or directory", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"readlink: {path}: Permission denied", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"readlink: {path}: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    # Parse command-line arguments
    options = []
    paths = []
    
    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            options.append(arg)
        else:
            paths.append(arg)
    
    # Validate input
    if not paths:
        print("Usage: readlink [OPTIONS] FILE...", file=sys.stderr)
        sys.exit(1)
    
    readlink_command(paths, options)

if __name__ == "__main__":
    main()
