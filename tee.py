#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The tee command from GNU coreutils in Python3.  
Example of use: echo "Hello, World!" | python3 tee.py output.txt
'''
#!/usr/bin/env python3

import argparse
import os
import signal
import sys

def tee(files, append=False, ignore_sigint=False):
    """Implémente la commande tee."""
    mode = "a" if append else "w"
    open_files = []

    if ignore_sigint:
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Ouvrir les fichiers spécifiés
    for file in files:
        try:
            open_files.append(open(file, mode))
        except OSError as e:
            print(f"tee: {file}: {e}", file=sys.stderr)

    try:
        while True:
            data = sys.stdin.read(1024)
            if not data:
                break

            # Écrire dans la sortie standard
            sys.stdout.write(data)
            sys.stdout.flush()

            # Écrire dans chaque fichier
            for f in open_files:
                try:
                    f.write(data)
                    f.flush()
                except OSError as e:
                    print(f"tee: Error writing to {f.name}: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        if not ignore_sigint:
            raise
    finally:
        # Fermer tous les fichiers ouverts
        for f in open_files:
            f.close()

def main():
    parser = argparse.ArgumentParser(description="Duplicate standard input to standard output and files.")
    parser.add_argument("files", nargs="*", help="Files to write to.")
    parser.add_argument("-a", "--append", action="store_true", help="Append to the files instead of overwriting.")
    parser.add_argument("-i", "--ignore-sigint", action="store_true", help="Ignore the SIGINT signal.")
    parser.add_argument("--version", action="version", version="tee.py 1.0")

    args = parser.parse_args()
    
    tee(args.files, append=args.append, ignore_sigint=args.ignore_sigint)

if __name__ == "__main__":
    main()

