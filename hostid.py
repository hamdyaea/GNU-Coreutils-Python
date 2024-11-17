#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The hostid command from GNU coreutils in Python3.  
Example of use: python3 hostid.py
'''

import uuid
import argparse

def get_hostid():
    """Return the numeric identifier for the current host in hexadecimal format."""
    # Retrieve the host's MAC address
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    # Take the first 8 characters (we simulate the host id from the MAC address)
    hostid = int(mac[:8], 16)
    return hex(hostid)

def main():
    # Création du parser pour les arguments
    parser = argparse.ArgumentParser(
        description="Print the numeric identifier (in hexadecimal) for the current host."
    )

    # Ajouter l'option version
    parser.add_argument(
        "--version", action="version", version="hostid.py 1.0",
        help="Show version and exit."
    )

    # Ajouter une option pour l'argument help
    # Cela est géré automatiquement par argparse, donc on n'a pas besoin de l'ajouter explicitement

    # Parser les arguments
    args = parser.parse_args()

    # Si aucun argument n'est passé, afficher l'ID de l'hôte
    # args contient les informations des arguments parsés, et ne sera vide que si aucun argument n'a été passé
    if len(vars(args)) == 0:
        hostid = get_hostid()
        print(hostid)

if __name__ == "__main__":
    main()



