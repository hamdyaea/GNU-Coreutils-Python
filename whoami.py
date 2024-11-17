#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The whoami command from GNU coreutils in Python3.  
Example of use: python3 whoami.py
'''
import os
import sys
import argparse

def print_user():
    # Utilise os.getlogin() pour obtenir le nom de l'utilisateur courant
    user_name = os.getlogin()
    print(user_name)

def print_version():
    print("whoami.py version 1.0")

def main():
    parser = argparse.ArgumentParser(description="Affiche le nom d'utilisateur associé à l'ID utilisateur effectif courant.")

    # Option pour afficher la version
    parser.add_argument('--version', action='store_true', help="Afficher la version")

    # Pas besoin d'ajouter '--help' manuellement, argparse le fait déjà.
    # parser.add_argument('--help', action='help', help="Afficher l'aide")  # Supprimé

    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        print_user()

if __name__ == "__main__":
    main()

