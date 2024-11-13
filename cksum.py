#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  13-11-2024
Last update: 13-11-2024
Version:  1.0
Description: The cksum command from coreutils in Python3. 
Example of use: python3 cksum.py -a sha256 file.txt
'''
import sys
import hashlib
import base64
import os

def print_help():
    help_text = """
    Usage: cksum [OPTION]... [FILE]...
    Print or verify checksums using the specified algorithm and options.

    Options:
      -a, --algorithm=TYPE   select the digest type (crc32, md5, sha1, sha256, sha512, etc.)
      --base64               emit base64-encoded digests, not hexadecimal
      -c, --check            read checksums from the FILEs and check them
      -l, --length=BITS      set digest length in bits (only valid for certain algorithms)
      --raw                  emit raw binary digest, not hexadecimal
      --tag                  create a BSD-style checksum (the default)
      --untagged             create an untagged checksum
      -z, --zero             end each output line with NUL instead of newline
      --help                 display this help and exit
      --version              output version information and exit

    Examples:
      cksum -a sha256 file.txt    Compute SHA256 checksum of file.txt
      cksum --base64 file.txt     Compute checksum in Base64 encoding
    """
    print(help_text)

def print_version():
    print("cksum 1.0")

def compute_checksum(filepath, algorithm="crc32", base64_output=False, raw_output=False, untagged=False):
    try:
        hash_func = hashlib.new(algorithm)
    except ValueError:
        print(f"Error: Unsupported algorithm '{algorithm}'")
        sys.exit(1)
        
    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            hash_func.update(chunk)

    digest = hash_func.digest() if raw_output else hash_func.hexdigest()

    if base64_output:
        digest = base64.b64encode(digest.encode()).decode()
    
    if untagged:
        output = f"{digest}  {filepath}"
    else:
        output = f"{algorithm.upper()} ({filepath}) = {digest}"
        
    print(output)

def main():
    algorithm = "crc32"
    base64_output = False
    raw_output = False
    untagged = False
    files = []

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ("--help", "-h"):
            print_help()
            return
        elif arg in ("--version"):
            print_version()
            return
        elif arg.startswith("--algorithm=") or arg == "-a":
            algorithm = arg.split("=")[1] if "=" in arg else sys.argv[i+1]
            if "=" not in arg:
                i += 1
        elif arg == "--base64":
            base64_output = True
        elif arg == "--raw":
            raw_output = True
        elif arg == "--untagged":
            untagged = True
        else:
            files.append(arg)
        i += 1

    if not files:
        print("Error: No files specified")
        sys.exit(1)

    for filepath in files:
        if os.path.isfile(filepath):
            compute_checksum(filepath, algorithm, base64_output, raw_output, untagged)
        else:
            print(f"Error: File not found - {filepath}")
            sys.exit(1)

if __name__ == "__main__":
    main()

