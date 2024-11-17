#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description:  the yes command from GNU coreutils in Python3. 
Example of use: python3 yes.py hello world
'''
import sys
import argparse

def print_version():
    print("yes.py version 1.0")
    sys.exit(0)

def main():
    # Créer un parser pour les arguments
    parser = argparse.ArgumentParser(description="Simuler la commande yes.")
    parser.add_argument('strings', nargs='*', default=['y'], help='Chaîne(s) à répéter (par défaut: "y")')
    parser.add_argument('--version', action='store_true', help='Afficher la version et quitter')

    # Analyser les arguments
    args = parser.parse_args()

    if args.version:
        print_version()
    
    # Répéter les chaînes spécifiées
    while True:
        print(" ".join(args.strings))

if __name__ == "__main__":
    main()

