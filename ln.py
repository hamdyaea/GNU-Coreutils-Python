#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The ln command from GNU coreutils in Python3.  
Example of use: python3 ln.py -s /path/to/target link_name
'''
import os
import sys

def create_symlink(target, link_name):
    try:
        # Créer le lien symbolique
        os.symlink(target, link_name)
        print(f"Lien symbolique créé : {link_name} -> {target}")
    except FileExistsError:
        print(f"Erreur : {link_name} existe déjà.")
    except Exception as e:
        print(f"Erreur lors de la création du lien symbolique : {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage : python3 ln.py -s TARGET LINK_NAME")
        sys.exit(1)

    option = sys.argv[1]
    target = sys.argv[2]
    link_name = sys.argv[3]

    # Vérifier si l'option -s est utilisée pour un lien symbolique
    if option == "-s":
        create_symlink(target, link_name)
    else:
        print("Option non supportée.")
        sys.exit(1)

if __name__ == "__main__":
    main()

