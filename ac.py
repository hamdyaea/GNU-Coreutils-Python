#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description:  The ac command from GNU coreutils in python3. 
Example of use: python3 ac.py -p
'''
import argparse
import struct
import os
import time
from collections import defaultdict

WTMP_FILE = "/var/log/wtmp"

# Structure basée sur Linux
# À adapter selon votre système en vérifiant /usr/include/utmp.h.
WTMP_STRUCT = "hi32s4s32s256shhiii4i"
WTMP_SIZE = struct.calcsize(WTMP_STRUCT)

def parse_wtmp(file_path):
    """
    Parse le fichier wtmp et retourne les enregistrements.
    """
    records = []
    with open(file_path, "rb") as f:
        while chunk := f.read(WTMP_SIZE):
            if len(chunk) != WTMP_SIZE:
                print(f"Enregistrement incomplet ignoré (taille: {len(chunk)}).")
                continue
            try:
                record = struct.unpack(WTMP_STRUCT, chunk)
                records.append(record)
            except struct.error as e:
                print(f"Erreur de dépaquetage : {e}")
    return records

def decode_safe(data, encoding="utf-8"):
    """
    Décode les données en chaînes de caractères en gérant les erreurs.
    """
    return data.decode(encoding, errors="replace").strip("\x00")

def calculate_times(records, individual_totals=False, daily_totals=False, print_zeros=False, all_days=False):
    """
    Calcule les temps de connexion à partir des enregistrements.
    """
    users = defaultdict(float)
    days = defaultdict(float)

    for record in records:
        user = decode_safe(record[2])  # Décodage sécurisé du nom d'utilisateur
        timestamp = record[10]
        time_struct = time.localtime(timestamp)
        day_key = time.strftime("%Y-%m-%d", time_struct)

        if user not in ["reboot", "shutdown"]:
            users[user] += 1.0  # Simule le temps accumulé (en heures)
            days[day_key] += 1.0

    return users, days

def print_totals(users, days, individual_totals, daily_totals, print_zeros):
    """
    Affiche les totaux calculés.
    """
    if daily_totals:
        for day, total in sorted(days.items()):
            if total > 0 or print_zeros:
                print(f"{day} total {total:.2f}")
    if individual_totals:
        for user, total in sorted(users.items()):
            if total > 0 or print_zeros:
                print(f"{user} {total:.2f}")

    grand_total = sum(users.values())
    print(f"Total: {grand_total:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Affiche des statistiques sur les temps de connexion des utilisateurs.")
    parser.add_argument("-d", "--daily-totals", action="store_true", help="Afficher les totaux quotidiens.")
    parser.add_argument("-p", "--individual-totals", action="store_true", help="Afficher les totaux individuels par utilisateur.")
    parser.add_argument("-z", "--print-zeros", action="store_true", help="Afficher les totaux même s'ils sont nuls.")
    parser.add_argument("-a", "--all-days", action="store_true", help="Afficher tous les jours, même sans activité.")
    parser.add_argument("-f", "--file", default=WTMP_FILE, help="Spécifier un fichier wtmp différent.")
    parser.add_argument("-V", "--version", action="version", version="1.2", help="Afficher la version.")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Erreur : Le fichier {args.file} n'existe pas.")
        return

    records = parse_wtmp(args.file)
    if not records:
        print("Aucun enregistrement trouvé dans le fichier wtmp.")
        return

    users, days = calculate_times(records, args.individual_totals, args.daily_totals, args.print_zeros, args.all_days)
    print_totals(users, days, args.individual_totals, args.daily_totals, args.print_zeros)

if __name__ == "__main__":
    main()

