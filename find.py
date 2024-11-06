#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  6-11-2024
Last update: 6-11-2024
Version: 1.0
Description: The find command from GNU coreutils in Python3  
Example of use: python3 find.py -name "test" /path/to/search
'''

import os
import sys
import argparse

def find(path, expression, follow_symlinks=False):
    # On parcourt le répertoire
    for root, dirs, files in os.walk(path, followlinks=follow_symlinks):
        for name in files + dirs:
            full_path = os.path.join(root, name)
            # On applique l'expression de recherche (exemple avec -name)
            if 'name' in expression:
                pattern = expression['name']
                if pattern in name:
                    print(full_path)
            # On pourrait ajouter d'autres expressions ici (comme -type)

def main():
    parser = argparse.ArgumentParser(description="GNU find command simplified")
    parser.add_argument("path", nargs="?", default=".", help="Répertoire à partir duquel la recherche commence")
    parser.add_argument("-name", help="Recherche par nom de fichier")
    parser.add_argument("-type", help="Recherche par type (fichier, répertoire, etc.)")
    parser.add_argument("-L", action="store_true", help="Suivre les liens symboliques")
    parser.add_argument("-P", action="store_true", help="Ne pas suivre les liens symboliques (comportement par défaut)")
    
    args = parser.parse_args()
    
    expression = {}
    if args.name:
        expression['name'] = args.name
    if args.type:
        expression['type'] = args.type  # À ajouter si on veut gérer les types de fichiers

    follow_symlinks = args.L  # Priorité à -L s'il est donné
    if args.P:
        follow_symlinks = False

    find(args.path, expression, follow_symlinks)

if __name__ == "__main__":
    main()

