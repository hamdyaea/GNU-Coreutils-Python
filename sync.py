#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The sync command from GNU coreutils in Python3.  
Example of use: python3 sync.py 
'''


import os
import argparse
import sys

def sync_files(files=None, data_only=False, file_system=False):
    """
    Synchronize cached writes to persistent storage.
    
    Args:
        files (list, optional): List of specific files to sync
        data_only (bool, optional): Sync only file data
        file_system (bool, optional): Sync entire file systems
    """
    try:
        if files:
            # Validate file existence
            for file in files:
                if not os.path.exists(file):
                    print(f"Error: File {file} does not exist", file=sys.stderr)
                    return False
            
            if file_system:
                # Sync file systems containing specified files
                file_systems = set(os.path.realpath(os.path.dirname(f)) for f in files)
                for fs in file_systems:
                    os.sync()
            else:
                # Sync specific files
                for file in files:
                    fd = os.open(file, os.O_RDWR)
                    if data_only:
                        os.fsync(fd)
                    else:
                        os.sync()
                    os.close(fd)
        else:
            # Sync entire system if no files specified
            os.sync()
        
        return True
    
    except PermissionError:
        print("Error: Insufficient permissions to sync", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Sync error: {e}", file=sys.stderr)
        return False

def main():
    """
    Main function to parse arguments and call sync functionality
    """
    parser = argparse.ArgumentParser(description='Synchronize cached writes to persistent storage')
    parser.add_argument('files', nargs='*', help='Files to synchronize')
    parser.add_argument('-d', '--data', action='store_true', 
                        help='Sync only file data, no unneeded metadata')
    parser.add_argument('-f', '--file-system', action='store_true', 
                        help='Sync the file systems that contain the files')
    parser.add_argument('--version', action='version', 
                        version='sync utility 1.0')
    
    args = parser.parse_args()
    
    result = sync_files(
        files=args.files, 
        data_only=args.data, 
        file_system=args.file_system
    )
    
    sys.exit(0 if result else 1)

if __name__ == '__main__':
    main()
