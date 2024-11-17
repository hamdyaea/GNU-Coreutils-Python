#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description: The shuf command from GNU coreutils in Python3. 
Example of use: python3 shuf.py -i 1-10
'''
import argparse
import random
import sys

def shuffle_lines(input_lines, count=None, repeat=False, zero_terminated=False):
    """
    Mélange les lignes d'entrée de manière aléatoire.

    :param input_lines: Liste des lignes à mélanger.
    :param count: Nombre maximal de lignes à afficher (si spécifié).
    :param repeat: Si True, autoriser la répétition des lignes.
    :param zero_terminated: Si True, utiliser '\0' comme délimiteur de ligne au lieu de '\n'.
    :return: Liste des lignes mélangées.
    """
    if repeat:
        return random.choices(input_lines, k=count) if count else input_lines
    else:
        random.shuffle(input_lines)
        if count:
            return input_lines[:count]
        return input_lines

def read_input(args):
    """
    Lit l'entrée en fonction des arguments fournis : fichier ou entrée standard.
    
    :param args: Arguments de la ligne de commande.
    :return: Liste des lignes lues depuis le fichier ou stdin.
    """
    if args.input_range:
        lo, hi = map(int, args.input_range.split('-'))
        input_lines = [str(i) for i in range(lo, hi + 1)]
    elif args.echo:
        input_lines = args.echo
    else:
        if args.input_file:
            with open(args.input_file, 'r') as f:
                input_lines = f.readlines()
        else:
            input_lines = sys.stdin.readlines()

    if args.zero_terminated:
        input_lines = [line.rstrip('\0') for line in input_lines]
    else:
        input_lines = [line.rstrip('\n') for line in input_lines]
        
    return input_lines

def write_output(output_lines, args):
    """
    Écrit les lignes de sortie, soit dans un fichier, soit sur stdout.
    
    :param output_lines: Liste des lignes à écrire.
    :param args: Arguments de la ligne de commande.
    """
    if args.output_file:
        with open(args.output_file, 'w') as f:
            for line in output_lines:
                f.write(f"{line}{'\0' if args.zero_terminated else '\n'}")
    else:
        for line in output_lines:
            print(f"{line}{'\0' if args.zero_terminated else ''}")

def main():
    parser = argparse.ArgumentParser(description="Générer des permutations aléatoires des lignes d'entrée.")
    parser.add_argument('input', nargs='?', help="Le fichier d'entrée ou stdin s'il est vide.")
    parser.add_argument('-e', '--echo', nargs='*', help="Traite chaque argument comme une ligne d'entrée.")
    parser.add_argument('-i', '--input-range', metavar="LO-HI", help="Traite chaque nombre de LO à HI comme une ligne d'entrée.")
    parser.add_argument('-n', '--head-count', type=int, help="Affiche au maximum COUNT lignes.")
    parser.add_argument('-o', '--output', dest='output_file', help="Écrit le résultat dans le fichier FILE.")
    parser.add_argument('--random-source', help="Obtenez des octets aléatoires depuis FILE.")
    parser.add_argument('-r', '--repeat', action='store_true', help="Les lignes peuvent être répétées.")
    parser.add_argument('-z', '--zero-terminated', action='store_true', help="Le délimiteur de ligne est NUL (\\0) au lieu de NEWLINE.")
    parser.add_argument('--version', action='version', version="1.0", help="Afficher la version.")
    
    args = parser.parse_args()

    # Lire les lignes d'entrée selon les options spécifiées
    input_lines = read_input(args)

    # Mélanger les lignes de manière aléatoire
    shuffled_lines = shuffle_lines(input_lines, count=args.head_count, repeat=args.repeat, zero_terminated=args.zero_terminated)

    # Écrire les résultats
    write_output(shuffled_lines, args)

if __name__ == "__main__":
    main()

