#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The unlink command from GNU coreutils in Python3.  
Example of use: python3 unlink.py file_to_delete.txt
'''
import os
import argparse
import sys

def print_version():
    print("unlink.py version 1.0")
    sys.exit(0)

def main():
    # Créer un parser pour les arguments
    parser = argparse.ArgumentParser(description="Simuler la commande unlink pour supprimer un fichier.")
    
    # Ajouter un argument optionnel --version
    parser.add_argument('--version', action='store_true', help='Afficher la version et quitter')

    # Ajouter un argument pour le fichier
    parser.add_argument('file', nargs='?', help='Le fichier à supprimer')  # rendre 'file' optionnel
    
    # Analyser les arguments
    args = parser.parse_args()

    # Si l'option --version est spécifiée, afficher la version et quitter
    if args.version:
        print_version()

    # Vérifier si un fichier a été fourni
    if not args.file:
        parser.print_help()
        sys.exit(1)

    # Supprimer le fichier spécifié
    try:
        os.unlink(args.file)
        print(f"Fichier '{args.file}' supprimé avec succès.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{args.file}' n'existe pas.")
    except PermissionError:
        print(f"Erreur : Permission refusée pour supprimer '{args.file}'.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()

