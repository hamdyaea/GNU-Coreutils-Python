#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email:  hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The sum command from GNU coreutils in Python3.  
Example of use: echo "Hello, World!" | python3 sum.py
'''
import argparse
import os
import sys

def bsd_checksum(file):
    """Calculer le checksum BSD et le nombre de blocs de 1 Ko."""
    checksum = 0
    blocks = 0
    with open(file, "rb") as f:
        while chunk := f.read(1024):
            blocks += 1
            checksum = (checksum + sum(chunk)) & 0xFFFF  # 16 bits
    return checksum, blocks

def sysv_checksum(file):
    """Calculer le checksum System V et le nombre de blocs de 512 octets."""
    checksum = 0
    blocks = 0
    with open(file, "rb") as f:
        while chunk := f.read(512):
            blocks += 1
            checksum += sum(chunk)
    checksum &= 0xFFFF  # 16 bits
    return checksum, blocks

def process_file(file, algorithm):
    """Traiter un fichier donné avec l'algorithme spécifié."""
    if file == "-":
        file = "/dev/stdin"
    if not os.path.isfile(file) and file != "/dev/stdin":
        print(f"sum: {file}: No such file", file=sys.stderr)
        return None, None
    return algorithm(file)

def main():
    parser = argparse.ArgumentParser(description="Checksum and count blocks of a file.")
    parser.add_argument("files", nargs="*", default=["-"], help="Files to process (default: standard input).")
    parser.add_argument("-r", action="store_true", help="Use BSD sum algorithm (default), 1K blocks.")
    parser.add_argument("-s", "--sysv", action="store_true", help="Use System V sum algorithm, 512-byte blocks.")
    parser.add_argument("--version", action="version", version="sum.py 1.0")
    
    args = parser.parse_args()

    # Déterminer l'algorithme à utiliser
    if args.sysv:
        algorithm = sysv_checksum
    else:
        algorithm = bsd_checksum

    for file in args.files:
        checksum, blocks = process_file(file, algorithm)
        if checksum is not None:
            print(f"{checksum} {blocks} {file if file != '/dev/stdin' else ''}")

if __name__ == "__main__":
    main()

