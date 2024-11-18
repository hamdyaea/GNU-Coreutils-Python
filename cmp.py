#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The cmp command from GNU coreutils in Python3.  
Example of use: python3 cmp.py file1.txt file2.txt
'''
import argparse
import sys


def parse_skip_value(skip):
    """Convertit une valeur de SKIP avec des suffixes multiplicatifs en entier."""
    if skip is None:
        return 0

    suffix_multipliers = {
        "kB": 1000,
        "K": 1024,
        "MB": 1000000,
        "M": 1048576,
        "GB": 1000000000,
        "G": 1073741824,
    }

    for suffix, multiplier in suffix_multipliers.items():
        if skip.endswith(suffix):
            return int(skip[:-len(suffix)]) * multiplier

    return int(skip)


def compare_files(file1, file2, skip1=0, skip2=0, limit=None, verbose=False, print_bytes=False):
    """Compare deux fichiers octet par octet."""
    differing_bytes = []
    try:
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            # Skip initial bytes
            f1.seek(skip1)
            f2.seek(skip2)

            byte_count = 0
            while True:
                b1 = f1.read(1)
                b2 = f2.read(1)

                if not b1 or not b2 or (limit is not None and byte_count >= limit):
                    break

                if b1 != b2:
                    differing_bytes.append((byte_count + 1, b1, b2))
                    if not verbose:
                        return False

                byte_count += 1

        if verbose:
            for offset, b1, b2 in differing_bytes:
                print(f"Byte {offset}: {b1.hex()} {b2.hex()}")

        return len(differing_bytes) == 0

    except FileNotFoundError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Compare two files byte by byte.")
    parser.add_argument("file1", help="Premier fichier à comparer.")
    parser.add_argument("file2", help="Second fichier à comparer.")
    parser.add_argument(
        "-b", "--print-bytes", action="store_true", help="Imprime les octets qui diffèrent."
    )
    parser.add_argument(
        "-i",
        "--ignore-initial",
        type=str,
        help="Ignore les premiers octets. Utilisez SKIP ou SKIP1:SKIP2.",
    )
    parser.add_argument(
        "-l", "--verbose", action="store_true", help="Affiche les octets différents."
    )
    parser.add_argument(
        "-n", "--bytes", type=int, help="Compare au maximum LIMIT octets."
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Ne produit aucune sortie, retourne uniquement le statut.",
    )
    parser.add_argument("--version", action="version", version="cmp.py 1.0")

    args = parser.parse_args()

    # Gérer les arguments SKIP
    skip1, skip2 = 0, 0
    if args.ignore_initial:
        if ":" in args.ignore_initial:
            skip1, skip2 = args.ignore_initial.split(":")
        else:
            skip1 = args.ignore_initial

        skip1 = parse_skip_value(skip1)
        skip2 = parse_skip_value(skip2)

    # Comparaison des fichiers
    are_equal = compare_files(
        args.file1,
        args.file2,
        skip1=skip1,
        skip2=skip2,
        limit=args.bytes,
        verbose=args.verbose,
        print_bytes=args.print_bytes,
    )

    # Résultats
    if args.silent:
        sys.exit(0 if are_equal else 1)
    elif are_equal:
        print("Les fichiers sont identiques.")
    else:
        print("Les fichiers sont différents.")
        sys.exit(1)


if __name__ == "__main__":
    main()

