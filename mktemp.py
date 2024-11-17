#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: the mktemp command from GNU coreutils in Python3.  
Example of use: python3 mktemp.py tmp.XXXXXXXXXX
'''
import os
import tempfile
import argparse

def create_temp_file_or_dir(template, directory=None, is_dir=False, suffix=None, dry_run=False):
    """
    Crée un fichier ou un répertoire temporaire basé sur un modèle de nom (template).
    
    :param template: Modèle de nom de fichier/répertoire (doit contenir au moins trois 'X' consécutifs).
    :param directory: Répertoire dans lequel créer le fichier/répertoire temporaire (optionnel).
    :param is_dir: Si True, crée un répertoire au lieu d'un fichier.
    :param suffix: Suffixe à ajouter au nom généré (optionnel).
    :param dry_run: Si True, affiche le nom sans créer le fichier/répertoire.
    """
    # Définir le répertoire par défaut si non fourni
    if directory is None:
        directory = os.environ.get('TMPDIR', '/tmp')

    # Vérifier si le modèle contient 'X' (comme requis par mktemp)
    if 'X' not in template:
        raise ValueError("Le modèle de nom (template) doit contenir au moins trois 'X' consécutifs.")

    # Appliquer le suffixe si fourni
    if suffix:
        template = template.rstrip('X') + suffix

    # Créer le fichier ou répertoire temporaire
    if dry_run:
        print(f"Dry-run: {os.path.join(directory, template)}")
    else:
        if is_dir:
            temp_dir = tempfile.mkdtemp(prefix=template, dir=directory)
            print(temp_dir)
        else:
            temp_file = tempfile.mktemp(prefix=template, dir=directory)
            print(temp_file)

def main():
    parser = argparse.ArgumentParser(description="Simuler la commande mktemp pour créer un fichier ou un répertoire temporaire.")
    parser.add_argument('template', nargs='?', default='tmp.XXXXXXXXXX', help="Modèle du nom à créer. Doit contenir au moins trois 'X'.")
    parser.add_argument('-p', '--tmpdir', help="Répertoire où créer le fichier/répertoire temporaire.")
    parser.add_argument('-s', '--suffix', help="Suffixe à ajouter au modèle de nom.")
    parser.add_argument('-u', '--dry-run', action='store_true', help="Affiche seulement le nom sans créer le fichier/répertoire.")
    parser.add_argument('-q', '--quiet', action='store_true', help="Supprime les messages d'erreur.")
    parser.add_argument('--version', action='version', version="1.0", help="Afficher la version du script.")

    # Option pour créer un répertoire (dossier) au lieu d'un fichier
    parser.add_argument('-d', '--directory', action='store_true', help="Créer un répertoire au lieu d'un fichier")

    args = parser.parse_args()

    try:
        create_temp_file_or_dir(
            template=args.template,
            directory=args.tmpdir,
            is_dir=args.directory,
            suffix=args.suffix,
            dry_run=args.dry_run
        )
    except Exception as e:
        if not args.quiet:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    main()

