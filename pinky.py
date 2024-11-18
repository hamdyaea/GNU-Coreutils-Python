#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version:  1.0
Description:  The pinky command from GNU coreutils in Python3. 
Example of use: python3 pinky.py
'''
#!/usr/bin/env python3

import os
import pwd
import spwd
import argparse
import sys
import socket
import datetime
from pathlib import Path

def get_user_info(username):
    """
    Retrieve detailed information about a user.
    
    Args:
        username (str): Username to retrieve information for
    
    Returns:
        dict: User information dictionary
    """
    try:
        # Get password database entry
        pw_entry = pwd.getpwnam(username)
        
        # Try to get shadow password entry for additional info
        try:
            sp_entry = spwd.getspnam(username)
            last_change = sp_entry.sp_lstchg
        except (PermissionError, KeyError):
            last_change = None
        
        # Construct user information dictionary
        user_info = {
            'username': pw_entry.pw_name,
            'uid': pw_entry.pw_uid,
            'gid': pw_entry.pw_gid,
            'gecos': pw_entry.pw_gecos.split(',')[0],  # Full name
            'home': pw_entry.pw_dir,
            'shell': pw_entry.pw_shell,
            'last_password_change': last_change
        }
        
        return user_info
    except KeyError:
        print(f"pinky: {username}: no such user", file=sys.stderr)
        return None

def print_short_format(users, options):
    """
    Print user information in short format.
    
    Args:
        users (list): List of user information dictionaries
        options (argparse.Namespace): Parsed command-line options
    """
    if not options.no_heading:
        # Print column headers
        headers = []
        if not options.no_full_name:
            headers.append("Name")
        headers.extend(["Login", "TTY", "Idle", "When", "Where"])
        print("\t".join(headers))
    
    for user_info in users:
        # Construct output line
        line_parts = []
        
        if not options.no_full_name:
            line_parts.append(user_info.get('gecos', user_info['username']))
        
        line_parts.append(user_info['username'])
        line_parts.extend(["?", "?", "?", "?"])  # Placeholder values
        
        print("\t".join(line_parts))

def print_long_format(users, options):
    """
    Print user information in long format.
    
    Args:
        users (list): List of user information dictionaries
        options (argparse.Namespace): Parsed command-line options
    """
    for user_info in users:
        print(f"Login: {user_info['username']}")
        
        if not options.no_full_name:
            print(f"Name: {user_info.get('gecos', user_info['username'])}")
        
        if not options.no_home_shell:
            print(f"Directory: {user_info['home']}")
            print(f"Shell: {user_info['shell']}")
        
        # Optional information (if available and not suppressed)
        if user_info['last_password_change']:
            print(f"Last password change: {user_info['last_password_change']}")

def main():
    """
    Main function to parse arguments and display user information
    """
    parser = argparse.ArgumentParser(description='Lightweight finger - print user information')
    
    # Format options
    parser.add_argument('-l', '--long', action='store_true', 
                        help='Produce long format output')
    parser.add_argument('-s', '--short', action='store_true', 
                        default=True, help='Produce short format output (default)')
    
    # Long format specific options
    parser.add_argument('-b', '--no-home-shell', action='store_true', 
                        help='Omit home directory and shell in long format')
    parser.add_argument('--no-project', action='store_true', 
                        help='Omit user\'s project file in long format')
    parser.add_argument('--no-plan', action='store_true', 
                        help='Omit user\'s plan file in long format')
    
    # Short format specific options
    parser.add_argument('-f', '--no-heading', action='store_true', 
                        help='Omit column headings in short format')
    parser.add_argument('-w', '--no-full-name', action='store_true', 
                        help='Omit user\'s full name in short format')
    parser.add_argument('-i', '--no-host', action='store_true', 
                        help='Omit full name and remote host in short format')
    parser.add_argument('-q', '--minimal', action='store_true', 
                        help='Omit full name, remote host, and idle time')
    
    # Additional options
    parser.add_argument('--lookup', action='store_true', 
                        help='Attempt to canonicalize hostnames via DNS')
    parser.add_argument('--version', action='version', 
                        version='pinky utility 1.0')
    
    # Users to query
    parser.add_argument('users', nargs='*', default=[os.getlogin()], 
                        help='Users to query (defaults to current user)')
    
    args = parser.parse_args()
    
    # Collect user information
    user_details = []
    for username in args.users:
        user_info = get_user_info(username)
        if user_info:
            user_details.append(user_info)
    
    # Print information based on format
    if args.long:
        print_long_format(user_details, args)
    else:
        print_short_format(user_details, args)

if __name__ == '__main__':
    main()
