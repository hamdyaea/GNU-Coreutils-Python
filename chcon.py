#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The chcon GNU coreutils command in Python3.  
Example of use: python3 chcon.py "user_u:role_r:type_t:s0" file1.txt file2.txt
'''
import argparse
import subprocess
import os
import sys

VERSION = "1.0"

def change_security_context(context, files, user=None, role=None, type=None, range=None, reference=None, recursive=False, verbose=False, dereference=True):
    """
    Change the SELinux security context of each file.
    """
    for file in files:
        cmd = ["chcon"]

        if recursive:
            cmd.append("-R")

        if reference:
            cmd.extend(["--reference", reference])
        else:
            if user:
                cmd.extend(["-u", user])
            if role:
                cmd.extend(["-r", role])
            if type:
                cmd.extend(["-t", type])
            if range:
                cmd.extend(["-l", range])

        if not dereference:
            cmd.append("-h")
        
        cmd.append(context)
        cmd.append(file)
        
        if verbose:
            print(f"Running command: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)

def main():
    """
    Main entry point for the script.
    """
    parser = argparse.ArgumentParser(
        description="Change the SELinux security context of files"
    )
    parser.add_argument(
        "context", 
        help="Security context to assign (e.g., user:role:type:range)"
    )
    parser.add_argument(
        "files", 
        nargs='+', 
        help="Files to apply the security context to"
    )
    parser.add_argument(
        "-u", "--user", 
        help="Set user in the security context"
    )
    parser.add_argument(
        "-r", "--role", 
        help="Set role in the security context"
    )
    parser.add_argument(
        "-t", "--type", 
        help="Set type in the security context"
    )
    parser.add_argument(
        "-l", "--range", 
        help="Set range in the security context"
    )
    parser.add_argument(
        "--reference", 
        help="Use reference file's security context"
    )
    parser.add_argument(
        "-R", "--recursive", 
        action="store_true", 
        help="Apply recursively to directories"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Print detailed output for each file"
    )
    parser.add_argument(
        "--no-dereference", 
        action="store_true", 
        help="Affect symbolic links instead of the referenced file"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"chcon.py {VERSION}",
        help="Display version information"
    )

    args = parser.parse_args()

    # Check if the context and files are provided
    if not args.context or not args.files:
        print("Error: context and at least one file are required.")
        sys.exit(1)

    # Determine whether to dereference or not
    dereference = not args.no_dereference

    # Call function to change the security context
    change_security_context(
        args.context, 
        args.files, 
        user=args.user, 
        role=args.role, 
        type=args.type, 
        range=args.range, 
        reference=args.reference, 
        recursive=args.recursive, 
        verbose=args.verbose, 
        dereference=dereference
    )

if __name__ == "__main__":
    main()

