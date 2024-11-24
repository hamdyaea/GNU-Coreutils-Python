#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The vdir command from GNU coreutils in Python3.  
Example of use:  python3 vdir.py -a
'''


import os
import pwd
import grp
import stat
import time
import argparse
from datetime import datetime

def get_file_type(mode):
    """Return the file type character based on mode."""
    if stat.S_ISDIR(mode):
        return 'd'
    elif stat.S_ISLNK(mode):
        return 'l'
    elif stat.S_ISFIFO(mode):
        return 'p'
    elif stat.S_ISSOCK(mode):
        return 's'
    elif stat.S_ISBLK(mode):
        return 'b'
    elif stat.S_ISCHR(mode):
        return 'c'
    return '-'

def get_permissions(mode):
    """Convert file mode to string representation."""
    perms = ''
    for who in ('USR', 'GRP', 'OTH'):
        for what in ('R', 'W', 'X'):
            if mode & getattr(stat, f'S_I{what}{who}'):
                perms += what.lower()
            else:
                perms += '-'
    return perms

def format_size(size):
    """Format file size with proper alignment."""
    return f"{size:>8}"

def format_time(mtime):
    """Format modification time."""
    now = time.time()
    mtime_dt = datetime.fromtimestamp(mtime)
    
    if now - mtime < 15778800:  # 6 months in seconds
        return mtime_dt.strftime('%b %d %H:%M')
    else:
        return mtime_dt.strftime('%b %d  %Y')

def list_directory(directory='.', all_files=False, recursive=False):
    """List directory contents in vdir format."""
    try:
        entries = os.listdir(directory)
    except PermissionError:
        print(f"vdir: cannot open directory '{directory}': Permission denied")
        return
    except FileNotFoundError:
        print(f"vdir: cannot access '{directory}': No such file or directory")
        return

    if not all_files:
        entries = [e for e in entries if not e.startswith('.')]
    entries.sort()

    total_blocks = 0
    file_infos = []

    for entry in entries:
        path = os.path.join(directory, entry)
        try:
            stat_info = os.lstat(path)
            total_blocks += stat_info.st_blocks
            file_infos.append((entry, stat_info))
        except (FileNotFoundError, PermissionError):
            continue

    print(f"total {total_blocks // 2}")

    for entry, stat_info in file_infos:
        # Get file type and permissions
        mode = stat_info.st_mode
        perms = get_file_type(mode) + get_permissions(mode)
        
        # Get number of hard links
        nlink = stat_info.st_nlink
        
        # Get owner and group names
        try:
            owner = pwd.getpwuid(stat_info.st_uid).pw_name
        except KeyError:
            owner = str(stat_info.st_uid)
        try:
            group = grp.getgrgid(stat_info.st_gid).gr_name
        except KeyError:
            group = str(stat_info.st_gid)
        
        # Format size and time
        size = format_size(stat_info.st_size)
        mtime = format_time(stat_info.st_mtime)
        
        # Print the line
        print(f"{perms} {nlink:>3} {owner:<8} {group:<8} {size} {mtime} {entry}")

    if recursive:
        for entry in entries:
            path = os.path.join(directory, entry)
            if os.path.isdir(path) and not os.path.islink(path):
                print(f"\n{path}:")
                list_directory(path, all_files, recursive)

def main():
    parser = argparse.ArgumentParser(description='Python implementation of vdir command')
    parser.add_argument('directories', nargs='*', default=['.'], 
                        help='Directories to list')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Show hidden files')
    parser.add_argument('-R', '--recursive', action='store_true',
                        help='List subdirectories recursively')
    
    args = parser.parse_args()
    
    for directory in args.directories:
        if len(args.directories) > 1:
            print(f"{directory}:")
        list_directory(directory, args.all, args.recursive)
        if len(args.directories) > 1:
            print()

if __name__ == "__main__":
    main()
