#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  13-11-2024
Last update: 13-11-2024
Version: 1.0
Description: The md5sum command from coreutils in Python3  
Example of use: python3 md5sum.py file.txt
'''
import hashlib
import sys
import os

def compute_md5(file_path, binary_mode=False):
    """Calculer la somme de contrôle MD5 d'un fichier"""
    hash_md5 = hashlib.md5()
    mode = 'rb' if binary_mode else 'r'

    with open(file_path, mode) as f:
        while chunk := f.read(4096):
            if not binary_mode:
                chunk = chunk.encode()
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

def print_md5sum(file_path, binary_mode=False, bsd_tag=False, zero_terminated=False):
    """Imprime la somme MD5 du fichier avec les options spécifiées"""
    md5_hash = compute_md5(file_path, binary_mode)
    separator = "\0" if zero_terminated else "\n"
    mode_char = '*' if binary_mode else ' '
    if bsd_tag:
        print(f"MD5 ({file_path}) = {md5_hash}", end=separator)
    else:
        print(f"{md5_hash} {mode_char}{file_path}", end=separator)

def check_md5sum(file_path, quiet=False, strict=False):
    """Vérifie la somme de contrôle d'un fichier avec les valeurs stockées"""
    with open(file_path, "r") as f:
        for line in f:
            expected_hash, file_name = line.strip().split("  ")
            computed_hash = compute_md5(file_name, binary_mode=True)

            if computed_hash == expected_hash:
                if not quiet:
                    print(f"{file_name}: OK")
            else:
                if strict:
                    sys.exit(1)
                print(f"{file_name}: FAILED")

def main():
    binary_mode = False
    check_mode = False
    bsd_tag = False
    zero_terminated = False
    quiet = False
    strict = False

    files = []

    # Parsing des arguments
    args = iter(sys.argv[1:])
    for arg in args:
        if arg in ("-b", "--binary"):
            binary_mode = True
        elif arg in ("-c", "--check"):
            check_mode = True
        elif arg == "--tag":
            bsd_tag = True
        elif arg in ("-z", "--zero"):
            zero_terminated = True
        elif arg == "--quiet":
            quiet = True
        elif arg == "--strict":
            strict = True
        elif arg == "--help":
            print("Usage: md5sum [OPTION]... [FILE]...\nCompute and check MD5 checksums.")
            return
        elif arg == "--version":
            print("md5sum 1.0")
            return
        else:
            files.append(arg)

    if check_mode:
        for file_path in files:
            check_md5sum(file_path, quiet, strict)
    else:
        for file_path in files:
            if os.path.isfile(file_path):
                print_md5sum(file_path, binary_mode, bsd_tag, zero_terminated)
            else:
                print(f"Error: File not found - {file_path}")
                sys.exit(1)

if __name__ == "__main__":
    main()

