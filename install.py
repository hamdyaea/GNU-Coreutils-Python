#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The install command from GNU coreutils in Python3.  
Example of use: python3 install.py source.txt /destination/
'''


import os
import sys
import stat
import shutil
import argparse
import grp
import pwd
from pathlib import Path
from datetime import datetime

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Copy files and set attributes',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'sources',
        nargs='+',
        help='Source file(s) to install'
    )
    
    parser.add_argument(
        'destination',
        help='Destination directory or file'
    )
    
    parser.add_argument(
        '-m', '--mode',
        type=lambda x: int(x, 8),
        default=0o755,
        help='Set permission bits (as in chmod), default is 755 in octal'
    )
    
    parser.add_argument(
        '-o', '--owner',
        help='Set ownership (super-user only)'
    )
    
    parser.add_argument(
        '-g', '--group',
        help='Set group ownership (super-user only)'
    )
    
    parser.add_argument(
        '-d', '--directory',
        action='store_true',
        help='Treat all arguments as directory names; create all components of specified directories'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print name of each file before copying'
    )
    
    parser.add_argument(
        '-b', '--backup',
        action='store_true',
        help='Make backup before removal'
    )
    
    parser.add_argument(
        '-S', '--suffix',
        default='~',
        help='Override the usual backup suffix'
    )
    
    parser.add_argument(
        '--preserve-timestamps',
        action='store_true',
        help='Preserve timestamps of source files'
    )
    
    parser.add_argument(
        '-s', '--strip',
        action='store_true',
        help='Strip symbol tables'
    )

    return parser.parse_args()

def get_uid_gid(owner, group):
    """Convert owner and group names to uid and gid."""
    uid = gid = -1
    
    if owner:
        try:
            uid = pwd.getpwnam(owner).pw_uid
        except KeyError:
            print(f"install: invalid user: '{owner}'", file=sys.stderr)
            sys.exit(1)
    
    if group:
        try:
            gid = grp.getgrnam(group).gr_gid
        except KeyError:
            print(f"install: invalid group: '{group}'", file=sys.stderr)
            sys.exit(1)
    
    return uid, gid

def create_backup(file_path, suffix):
    """Create a backup of the file if it exists."""
    if os.path.exists(file_path):
        backup_path = f"{file_path}{suffix}"
        shutil.copy2(file_path, backup_path)
        return backup_path
    return None

def install_file(source, destination, mode, uid, gid, verbose, backup, suffix, preserve_timestamps, strip):
    """Install a single file."""
    try:
        # Determine if destination is a directory
        dest_path = Path(destination)
        if dest_path.is_dir():
            dest_path = dest_path / os.path.basename(source)
        
        # Create backup if requested
        if backup and dest_path.exists():
            backup_path = create_backup(dest_path, suffix)
            if verbose and backup_path:
                print(f"made backup of '{dest_path}' as '{backup_path}'")
        
        # Copy the file
        if verbose:
            print(f"installing '{source}' to '{dest_path}'")
        
        shutil.copy2(source, dest_path)
        
        # Set permissions
        os.chmod(dest_path, mode)
        
        # Set ownership
        if uid != -1 or gid != -1:
            os.chown(dest_path, uid, gid)
        
        # Strip if requested (simplified implementation)
        if strip and (dest_path.suffix in ['.so', '.dll', '.exe'] or not dest_path.suffix):
            os.system(f"strip {dest_path}")
        
        # Handle timestamps
        if not preserve_timestamps:
            current_time = datetime.now().timestamp()
            os.utime(dest_path, (current_time, current_time))
        
        return True
        
    except (OSError, shutil.Error) as e:
        print(f"install: error installing '{source}': {str(e)}", file=sys.stderr)
        return False

def create_directories(paths, mode, uid, gid, verbose):
    """Create directories with specified attributes."""
    for path in paths:
        try:
            os.makedirs(path, mode=mode, exist_ok=True)
            if uid != -1 or gid != -1:
                os.chown(path, uid, gid)
            if verbose:
                print(f"created directory '{path}'")
        except OSError as e:
            print(f"install: error creating directory '{path}': {str(e)}", file=sys.stderr)
            return False
    return True

def main():
    """Main program entry point."""
    args = parse_args()
    
    # Get UID and GID
    uid, gid = get_uid_gid(args.owner, args.group)
    
    # Handle directory creation mode
    if args.directory:
        success = create_directories(
            args.sources + [args.destination],
            args.mode,
            uid,
            gid,
            args.verbose
        )
        sys.exit(0 if success else 1)
    
    # Handle file installation
    exit_code = 0
    for source in args.sources:
        if not install_file(
            source,
            args.destination,
            args.mode,
            uid,
            gid,
            args.verbose,
            args.backup,
            args.suffix,
            args.preserve_timestamps,
            args.strip
        ):
            exit_code = 1
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
