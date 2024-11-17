#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The who command from GNU coreutils in Python3.  
Example of use: python3 who.py -a
'''
import os
import sys
import argparse
import time
import subprocess

def print_header():
    print("NAME     LINE   TIME")

def print_user_info():
    users = os.popen('who').readlines()
    for user in users:
        print(user.strip())

def print_boot_time():
    boot_time_str = os.popen('uptime -s').read().strip()  # Date de démarrage système
    boot_time = time.mktime(time.strptime(boot_time_str, "%Y-%m-%d %H:%M:%S"))  # Convertir en secondes depuis l'époque UNIX
    formatted_boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time))  # Formater le temps
    print(f"Last boot: {formatted_boot_time}")

def print_runlevel():
    runlevel = subprocess.getoutput("runlevel")
    print(f"Current runlevel: {runlevel}")

def print_processes():
    processes = os.popen('ps -eo user,cmd').readlines()
    for process in processes[1:]:
        print(process.strip())

def print_logged_users():
    # Utiliser 'who' pour obtenir les utilisateurs connectés
    users = os.popen('who').readlines()
    logged_users = [user.split()[0] for user in users]  # Extraire les noms des utilisateurs
    print(f"Logged users: {', '.join(logged_users)}")

def print_count():
    user_count = len(os.popen('who').readlines())
    print(f"Number of users logged in: {user_count}")

def print_last_clock_change():
    last_change = subprocess.getoutput('last -x | grep shutdown | head -n 1')
    print(f"Last clock change: {last_change}")

def who_command(args):
    if args.heading:
        print_header()

    if args.all:
        print_user_info()
        print_boot_time()
        print_runlevel()
        print_processes()
        print_logged_users()
        print_count()
        print_last_clock_change()

    if args.boot:
        print_boot_time()

    if args.dead:
        print("Dead processes not implemented in this mock version.")

    if args.login:
        print("System login processes not implemented in this mock version.")

    if args.lookup:
        print("Attempting to canonicalize hostnames not implemented in this mock version.")

    if args.short:
        print_user_info()

    if args.time:
        print_last_clock_change()

    if args.count:
        print_count()

    if args.users:
        print_logged_users()

def main():
    parser = argparse.ArgumentParser(description="Simuler la commande who pour afficher les utilisateurs connectés.")

    parser.add_argument('-a', '--all', action='store_true', help="Equivalent à -b -d --login -p -r -t -T -u")
    parser.add_argument('-b', '--boot', action='store_true', help="Heure du dernier démarrage du système")
    parser.add_argument('-d', '--dead', action='store_true', help="Afficher les processus morts")
    parser.add_argument('-H', '--heading', action='store_true', help="Afficher les en-têtes de colonnes")
    parser.add_argument('-l', '--login', action='store_true', help="Afficher les processus de connexion système")
    parser.add_argument('--lookup', action='store_true', help="Essayer de résoudre les hôtes via DNS")
    parser.add_argument('-m', action='store_true', help="Afficher le nom d'hôte et l'utilisateur associés à stdin")
    parser.add_argument('-p', '--process', action='store_true', help="Afficher les processus actifs lancés par init")
    parser.add_argument('-q', '--count', action='store_true', help="Afficher le nombre d'utilisateurs connectés")
    parser.add_argument('-r', '--runlevel', action='store_true', help="Afficher le niveau d'exécution actuel")
    parser.add_argument('-s', '--short', action='store_true', help="Afficher seulement nom, ligne et heure")
    parser.add_argument('-t', '--time', action='store_true', help="Afficher le dernier changement d'heure système")
    parser.add_argument('-T', '--mesg', action='store_true', help="Ajouter le statut du message de l'utilisateur")
    parser.add_argument('-u', '--users', action='store_true', help="Lister les utilisateurs connectés")
    parser.add_argument('--message', action='store_true', help="Même que -T")
    parser.add_argument('--writable', action='store_true', help="Même que -T")
    parser.add_argument('--version', action='version', version="who.py version 1.0", help="Afficher la version")

    parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    who_command(args)

if __name__ == "__main__":
    main()

