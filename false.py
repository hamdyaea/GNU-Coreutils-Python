#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email:  hamdy.aea@protonmail.com
Date of creation: 17-11-2024
Last update: 17-11-2024
Version:  1.0
Description:  The false command from GNU coreutils in Python3. 
Example of use: python3 false.py
'''
import sys
import argparse

def print_version():
    print("false.py version 1.0")
    sys.exit(0)

def main():
    # Créer un parser sans l'option --help pour éviter le conflit
    parser = argparse.ArgumentParser(description="Simuler la commande false.")
    parser.add_argument('--version', action='store_true', help='Afficher la version et quitter')

    # Analyser les arguments
    args = parser.parse_args()

    if args.version:
        print_version()
    else:
        sys.exit(1)  # Retourne le code d'erreur 1 (échec)

if __name__ == "__main__":
    main()

