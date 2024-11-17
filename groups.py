#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The groups command from GNU coreutils in Python3  
Example of use: python3 groups.py username
'''

import sys
import argparse
import os
import grp
import pwd

def get_groups_for_user(username=None):
    """Return a list of groups a user belongs to."""
    if username is None:
        # If no username is provided, get the groups for the current user
        username = os.getlogin()
    
    # Get the user's ID
    user_info = pwd.getpwnam(username)
    
    # Get the list of groups for the user
    groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem or g.gr_name == user_info.pw_name]
    return groups

def main():
    parser = argparse.ArgumentParser(
        description="Print group memberships for each USERNAME or, if no USERNAME is specified, for the current process."
    )
    parser.add_argument(
        "usernames", nargs="*", default=[os.getlogin()], 
        help="The usernames to query. If no USERNAME is provided, the current user is used."
    )
    parser.add_argument(
        "--version", action="version", version="groups.py 1.0", 
        help="Show version and exit."
    )
    
    args = parser.parse_args()

    # Process each username and print their groups
    for username in args.usernames:
        groups = get_groups_for_user(username)
        print(f"{username}: {', '.join(groups)}")

if __name__ == "__main__":
    main()

