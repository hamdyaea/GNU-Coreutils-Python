#!/usr/bin/env python3

# Developer : Mehdi Marhol
# kbmehdi69@gmail.com

# This software is a basic copy of the famous ls command in Linux coreutils.

import os
import sys


def show_all_files():
    """
    Show all files, including hidden ones.
    """
    show_dir_contents(show_all=True)


def show_almost_all_files():
    """
    Show almost all files, excluding '.' and '..'
    """
    show_dir_contents(almost_all=True)


def show_only_visible_files():
    """
    Show only visible (non-hidden) files
    """
    show_dir_contents()


# Dictionary mapping options to functions
options = {
    "-a": show_all_files,
    "--all": show_all_files,
    "-A": show_almost_all_files,
    "--almost-all": show_almost_all_files
}


def show_dir_contents(path=".", show_all=False, almost_all=False):
    """
    Lists files in the specified directory

    Parameters:
    - path (str): Directory path to list files from
    - show_all (boolean): If True, includes hidden files
    - almost_all (boolean): If True, includes hidden files except '.' and '..'
    """
    try:
        # Get all files in the directory
        files = os.listdir(path)

        if show_all:
            pass  # Show all files, including hidden ones
        elif almost_all:
            # Exclude '.' and '..'
            files = [f for f in files if f not in ('.', '..')]
        else:
            # Only show non-hidden files
            files = [f for f in files if not f.startswith('.')]

        # Print each file or directory name on a single line
        for f in files:
            print(f)

    except FileNotFoundError:
        print("Directory not found.")
    except PermissionError:
        print("Access denied.")


if __name__ == "__main__":
    # Check in command-line for possible  arguments
    if len(sys.argv) > 1:
        option = sys.argv[1]
        # Call the corresponding function from the options dictionary
        action = options.get(option, show_only_visible_files)  # Default to showing only visible files
        action()
    else:
        show_only_visible_files()
