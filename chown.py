#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email:  hamdy.aea@protonmail.com
Date of creation:  4-11-2024
Last update: 4-11-2024
Version: 1.0
Description: The chown command from GNU coreutils in Python3  
Example of use: python3 chown.py user:group /path/to/file
'''
import os
import pwd
import grp
import sys

def change_ownership(path, user, group):
    try:
        if user:
            uid = pwd.getpwnam(user).pw_uid
        else:
            uid = -1  # Do not change UID

        if group:
            gid = grp.getgrnam(group).gr_gid
        else:
            gid = -1  # Do not change GID

        os.chown(path, uid, gid)
        print(f"Ownership of {path} changed to {user}:{group}")
    except KeyError as e:
        print(f"Warning: Unable to get UID/GID for '{e.args[0]}'. Please use numeric UID/GID.")
        return  # Early exit if user/group not found
    except OSError as e:
        print(f"Error changing ownership: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 chown.py <user:group> <file>")
        sys.exit(1)

    user_group = sys.argv[1].split(':')
    user = user_group[0] if len(user_group) > 0 else None
    group = user_group[1] if len(user_group) > 1 else None
    file_path = sys.argv[2]

    change_ownership(file_path, user, group)

