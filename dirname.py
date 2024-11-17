#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2204
Version: 1.0
Description: The dirname command from GNU coreutils in Python3.  
Example of use: python3 dirname.py /usr/bin/
'''
import os
import argparse
import sys

def dirname(path):
    """
    Cette fonction retourne le chemin du répertoire contenant le fichier ou dossier.
    Si le chemin ne contient pas de '/', elle retourne '.'
    """
    # Si le chemin contient un '/', on enlève le dernier composant
    if '/' in path:
        # Si le chemin se termine par une barre oblique, on la supprime avant de passer à dirname
        if path.endswith('/'):
            path = path.rstrip('/')
        return os.path.dirname(path)
    return '.'

def print_version():
    print("dirname.py version 1.0")

def main():
    parser = argparse.ArgumentParser(description="Retirer le dernier composant d'un chemin de fichier")

    # Argument --version pour afficher la version du programme
    parser.add_argument('--version', action='store_true', help="Afficher la version")
    
    # Argument -z ou --zero pour terminer chaque ligne avec un caractère NUL
    parser.add_argument('-z', '--zero', action='store_true', help="Terminer chaque ligne avec NUL au lieu d'une nouvelle ligne")
    
    # Ajouter des arguments pour les noms de fichiers à traiter
    parser.add_argument('names', nargs='*', help="Nom(s) de fichier ou répertoire")

    args = parser.parse_args()

    # Si l'option --version est utilisée
    if args.version:
        print_version()
        return

    # Si aucun nom n'est fourni, on affiche un message d'aide
    if not args.names:
        print("Usage: dirname [OPTION] NAME...")
        sys.exit(1)

    # Traitement de chaque nom de fichier fourni
    for name in args.names:
        result = dirname(name)
        
        # Si l'option -z est activée, on termine avec un caractère NUL
        if args.zero:
            print(result, end='\0')
        else:
            print(result)

if __name__ == "__main__":
    main()

