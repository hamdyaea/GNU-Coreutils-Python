#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The chgrp command from GNU coreutils in Python3.  
Example of use: python3 chgrp.py staff file.txt
'''
import os
import grp
import argparse
import sys


def validate_group(group_name):
    """Vérifie si le groupe existe."""
    try:
        group_info = grp.getgrnam(group_name)
        return group_info.gr_gid
    except KeyError:
        print(f"Erreur : Le groupe '{group_name}' n'existe pas.", file=sys.stderr)
        sys.exit(1)


def change_group(file_path, gid, dereference):
    """Change le groupe d'un fichier ou répertoire."""
    try:
        if dereference or not os.path.islink(file_path):
            os.chown(file_path, -1, gid)
        else:
            os.lchown(file_path, -1, gid)
        return True
    except FileNotFoundError:
        print(f"Erreur : Le fichier ou répertoire '{file_path}' n'existe pas.", file=sys.stderr)
        return False
    except PermissionError:
        print(f"Permission refusée : '{file_path}'.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}.", file=sys.stderr)
        return False


def process_files(group_name, files, dereference):
    """Traite tous les fichiers donnés."""
    gid = validate_group(group_name)
    for file_path in files:
        if not change_group(file_path, gid, dereference):
            print(f"Échec du changement de groupe pour : {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Change le groupe des fichiers ou répertoires spécifiés."
    )
    parser.add_argument("group", help="Nom du groupe.")
    parser.add_argument("files", nargs="+", help="Fichiers ou répertoires à modifier.")
    parser.add_argument(
        "-n", "--no-dereference", action="store_true", help="Modifier les liens symboliques eux-mêmes."
    )

    args = parser.parse_args()

    dereference = not args.no_dereference
    process_files(args.group, args.files, dereference)


if __name__ == "__main__":
    main()

