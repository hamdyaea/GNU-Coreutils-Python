#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com	
Date of creation:  13-11-2024
Last update: 13-11-2024
Version: 1.0
Description: The chroot command from GNU coreutils in Python3.  
Example of use: sudo python3 chroot.py /path/to/newroot /bin/ls
'''
import os
import sys
import subprocess
import pwd
import grp

def print_help():
    help_text = """
    Usage: chroot [OPTION] NEWROOT [COMMAND [ARG]...]
    Run COMMAND with root directory set to NEWROOT.

    Options:
      --groups=G_LIST     specify supplementary groups as g1,g2,...,gN
      --userspec=USER:GROUP specify user and group (ID or name) to use
      --skip-chdir        do not change working directory to '/'
      --help              display this help and exit
      --version           output version information and exit

    If no command is given, run '"$SHELL" -i' (default: '/bin/sh -i').
    """
    print(help_text)

def print_version():
    version_text = "chroot 1.0"
    print(version_text)

def change_root(new_root):
    try:
        os.chroot(new_root)
    except PermissionError:
        print("Permission denied. You must be root to use chroot.")
        sys.exit(125)
    except Exception as e:
        print(f"chroot failed: {e}")
        sys.exit(125)

def set_user_and_group(user_group):
    user, group = user_group.split(':')
    uid = pwd.getpwnam(user).pw_uid if user else None
    gid = grp.getgrnam(group).gr_gid if group else None
    if uid is not None:
        os.setuid(uid)
    if gid is not None:
        os.setgid(gid)

def set_groups(g_list):
    groups = [grp.getgrnam(g).gr_gid for g in g_list.split(',')]
    os.setgroups(groups)

def main():
    new_root = None
    command = ["/bin/sh", "-i"]  # default shell
    skip_chdir = False

    # Parse arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith("--"):
            if arg == "--help":
                print_help()
                return
            elif arg == "--version":
                print_version()
                return
            elif arg.startswith("--userspec="):
                user_group = arg.split("=", 1)[1]
                set_user_and_group(user_group)
            elif arg.startswith("--groups="):
                groups = arg.split("=", 1)[1]
                set_groups(groups)
            elif arg == "--skip-chdir":
                skip_chdir = True
            else:
                print(f"Unknown option: {arg}")
                sys.exit(125)
        else:
            if not new_root:
                new_root = arg
            else:
                command = sys.argv[i:]
                break
        i += 1

    if not new_root:
        print("Error: NEWROOT argument is required")
        sys.exit(125)

    change_root(new_root)

    if not skip_chdir:
        os.chdir("/")

    # Run the command
    try:
        result = subprocess.run(command)
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(f"Command not found: {command[0]}")
        sys.exit(127)
    except PermissionError:
        print(f"Permission denied for command: {command[0]}")
        sys.exit(126)

if __name__ == "__main__":
    main()

