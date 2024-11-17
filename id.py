#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The id command from GNU coreutils in Python3.  
Example of use: python3 id.py --user --name
'''

import os
import sys
import argparse
import pwd
import grp

def get_user_info(username=None):
    """Return user and group information for the current process or a specified user."""
    if username:
        try:
            user = pwd.getpwnam(username)
        except KeyError:
            print(f"User '{username}' not found.")
            sys.exit(1)
    else:
        user = pwd.getpwuid(os.getuid())

    user_info = {
        'user': user.pw_name,
        'uid': user.pw_uid,
        'group': grp.getgrgid(user.pw_gid).gr_name,
        'gid': user.pw_gid,
        'groups': [g.gr_name for g in grp.getgrall() if user.pw_uid in [u.pw_uid for u in pwd.getpwall()]],
    }

    return user_info

def print_user_info(user_info, args):
    """Print user info based on the arguments."""
    output = []
    
    # By default, print the UID and GID and groups
    if not args.user and not args.group and not args.groups and not args.name:
        output.append(f"uid={user_info['uid']}({user_info['user']}) gid={user_info['gid']}({user_info['group']})")
        output.append(f"groups={','.join(user_info['groups'])}")

    if args.user:
        output.append(f"uid={user_info['uid']}({user_info['user']})")
    if args.group:
        output.append(f"gid={user_info['gid']}({user_info['group']})")
    if args.groups:
        groups = ','.join(user_info['groups'])
        output.append(f"groups={groups}")
    if args.name:
        output.append(f"Name: {user_info['user']}")
    if args.context:
        output.append("Security context: Not implemented in this version.")
    if args.real:
        output.append(f"Real UID={user_info['uid']} Real GID={user_info['gid']}")
    
    print(" ".join(output))

def main():
    parser = argparse.ArgumentParser(description="Print real and effective user and group IDs.")

    # Add options
    parser.add_argument('-g', '--group', action='store_true', help="print only the effective group ID")
    parser.add_argument('-G', '--groups', action='store_true', help="print all group IDs")
    parser.add_argument('-n', '--name', action='store_true', help="print a name instead of a number, for -ugG")
    parser.add_argument('-u', '--user', action='store_true', help="print only the effective user ID")
    parser.add_argument('-r', '--real', action='store_true', help="print the real ID instead of the effective ID, with -ugG")
    parser.add_argument('-Z', '--context', action='store_true', help="print only the security context of the process")
    parser.add_argument('--version', action='version', version="id.py 1.0", help="output version information and exit")
    parser.add_argument('username', nargs='?', type=str, help="specify a user to get information for")

    args = parser.parse_args()

    # Get user info
    user_info = get_user_info(args.username)

    # Print the requested information
    print_user_info(user_info, args)

if __name__ == "__main__":
    main()

