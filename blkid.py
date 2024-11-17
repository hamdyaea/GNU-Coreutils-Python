#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The blkid command from GNU coreutils in Python3.  
Example of use: python3 blkid.py -p /dev/sda1
'''
import argparse
import os
import subprocess
import sys

def run_blkid_command(args):
    """
    Exécute les commandes simulées de blkid en fonction des arguments passés.
    """
    try:
        blkid_args = []

        if args.label:
            blkid_args.extend(["-L", args.label])
        if args.uuid:
            blkid_args.extend(["-U", args.uuid])
        if args.garbage:
            blkid_args.append("-g")
        if args.low_level:
            blkid_args.append("-p")
        if args.iolimits:
            blkid_args.append("-i")
        if args.output_format:
            blkid_args.extend(["-o", args.output_format])
        if args.tag:
            for tag in args.tag:
                blkid_args.extend(["-s", tag])
        if args.token:
            blkid_args.extend(["-t", args.token])
        if args.cache_file:
            blkid_args.extend(["-c", args.cache_file])
        if args.write_cache_file:
            blkid_args.extend(["-w", args.write_cache_file])
        if args.offset:
            blkid_args.extend(["-O", str(args.offset)])
        if args.size:
            blkid_args.extend(["-S", str(args.size)])
        if args.usages:
            blkid_args.extend(["-u", args.usages])

        if args.devices:
            blkid_args.extend(args.devices)

        # Commande blkid simulée
        cmd = ["blkid"] + blkid_args
        print(f"Exécution : {' '.join(cmd)}")  # Débogage
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)

    except FileNotFoundError:
        print("Erreur : blkid n'est pas disponible sur ce système.", file=sys.stderr)
        sys.exit(4)


def main():
    parser = argparse.ArgumentParser(
        description="Simule l'utilitaire blkid pour trouver/afficher les attributs des périphériques de blocs."
    )
    parser.add_argument("-L", "--label", help="Rechercher un périphérique par étiquette (LABEL).")
    parser.add_argument("-U", "--uuid", help="Rechercher un périphérique par UUID.")
    parser.add_argument("-g", "--garbage", action="store_true", help="Effectuer une collecte des ordures sur le cache blkid.")
    parser.add_argument("-p", "--low-level", action="store_true", help="Passer en mode de sondage bas niveau.")
    parser.add_argument("-i", "--iolimits", action="store_true", help="Afficher les limites d'E/S.")
    parser.add_argument("-o", "--output-format", choices=["full", "value", "list", "device", "udev", "export"], help="Spécifier le format de sortie.")
    parser.add_argument("-s", "--tag", action="append", help="Afficher uniquement les étiquettes correspondant à TAG.")
    parser.add_argument("-t", "--token", help="Rechercher des périphériques avec un TOKEN donné (NAME=value).")
    parser.add_argument("-c", "--cache-file", help="Lire depuis un fichier de cache spécifique.")
    parser.add_argument("-w", "--write-cache-file", help="Écrire le cache des périphériques dans un fichier spécifique.")
    parser.add_argument("-O", "--offset", type=int, help="Sonder à un décalage donné (mode bas niveau).")
    parser.add_argument("-S", "--size", type=int, help="Remplacer la taille du périphérique/fichier (mode bas niveau).")
    parser.add_argument("-u", "--usages", help="Restreindre les fonctions de sondage aux types d'utilisation définis.")
    parser.add_argument("devices", nargs="*", help="Périphériques à examiner.")

    args = parser.parse_args()
    run_blkid_command(args)


if __name__ == "__main__":
    main()

