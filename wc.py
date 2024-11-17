#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description:  The wc command from GNU coreutils in Python3. 
Example of use: echo "Hello world" | python3 wc.py -l -w -c
'''
import os
import sys
import argparse

def count_lines_words_bytes(file):
    lines = 0
    words = 0
    bytes_count = 0
    max_line_length = 0

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            lines += 1
            words += len(line.split())
            bytes_count += len(line.encode('utf-8'))
            max_line_length = max(max_line_length, len(line.rstrip('\n')))
    
    return lines, words, bytes_count, max_line_length

def print_total(counts):
    total_lines = sum(count[0] for count in counts)
    total_words = sum(count[1] for count in counts)
    total_bytes = sum(count[2] for count in counts)
    total_max_line_length = max(count[3] for count in counts)
    print(f"total {total_lines} {total_words} {total_bytes} {total_max_line_length}")

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Simuler la commande wc pour compter les lignes, mots, et octets.")
    
    parser.add_argument('-c', '--bytes', action='store_true', help='Afficher le nombre d\'octets')
    parser.add_argument('-m', '--chars', action='store_true', help='Afficher le nombre de caractères')
    parser.add_argument('-l', '--lines', action='store_true', help='Afficher le nombre de lignes')
    parser.add_argument('-w', '--words', action='store_true', help='Afficher le nombre de mots')
    parser.add_argument('-L', '--max-line-length', action='store_true', help='Afficher la longueur de la ligne la plus longue')
    parser.add_argument('--total', choices=['auto', 'always', 'only', 'never'], default='auto', help='Quand afficher les totaux')
    parser.add_argument('--files0-from', type=str, help='Lire les noms de fichiers NUL-terminés à partir de F')
    parser.add_argument('files', nargs='*', help='Fichiers à traiter')
    
    args = parser.parse_args()

    # Si aucun fichier n'est spécifié, utiliser stdin
    if not args.files and not args.files0_from:
        args.files.append('-')

    counts = []
    
    if args.files0_from:
        # Lire les noms de fichiers NUL-terminés
        if args.files0_from == '-':
            files = sys.stdin.read().split('\0')
        else:
            with open(args.files0_from, 'r') as f:
                files = f.read().split('\0')
        
        files = [f for f in files if f]  # Supprimer les entrées vides
    else:
        files = args.files
    
    # Traitement des fichiers
    for filename in files:
        if filename == '-':
            # Si le fichier est "-", lire depuis stdin
            input_data = sys.stdin.read()
            lines = input_data.splitlines()
            word_count = sum(len(line.split()) for line in lines)
            byte_count = len(input_data.encode('utf-8'))
            max_line_length = max(len(line.rstrip('\n')) for line in lines)
            line_count = len(lines)
        else:
            line_count, word_count, byte_count, max_line_length = count_lines_words_bytes(filename)

        if args.lines:
            print(line_count, end=" ")
        if args.words:
            print(word_count, end=" ")
        if args.bytes:
            print(byte_count, end=" ")
        if args.max_line_length:
            print(max_line_length, end=" ")
        
        print(filename)
        
        counts.append((line_count, word_count, byte_count, max_line_length))
    
    # Afficher les totaux si nécessaire
    if args.total == 'always' or (args.total == 'auto' and len(files) > 1):
        print_total(counts)

if __name__ == "__main__":
    main()

