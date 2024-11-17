#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The test command from GNU coreutils in Python3.  
Example of use: python3 test.py -n "hello"
'''

import os
import sys

def print_help():
    """Affiche l'aide."""
    print(
        """Usage: test [EXPRESSION]
Evaluate EXPRESSION and return 0 if true, 1 if false.

Options:
  --help     display this help and exit
  --version  output version information and exit

Unary operators:
  -n STRING  the length of STRING is nonzero
  -z STRING  the length of STRING is zero
  -e FILE    FILE exists
  -f FILE    FILE exists and is a regular file
  -d FILE    FILE exists and is a directory

Binary operators:
  STRING1 = STRING2  the strings are equal
  STRING1 != STRING2 the strings are not equal
  INTEGER1 -eq INTEGER2 INTEGER1 is equal to INTEGER2
  INTEGER1 -ne INTEGER2 INTEGER1 is not equal to INTEGER2
  INTEGER1 -gt INTEGER2 INTEGER1 is greater than INTEGER2
  INTEGER1 -lt INTEGER2 INTEGER1 is less than INTEGER2
  INTEGER1 -ge INTEGER2 INTEGER1 is greater than or equal to INTEGER2
  INTEGER1 -le INTEGER2 INTEGER1 is less than or equal to INTEGER2"""
    )


def print_version():
    """Affiche la version."""
    print("test.py 1.0")


def evaluate_expression(expr):
    """Évalue l'expression fournie."""
    if not expr:
        # Aucun argument fourni : retourne False.
        return False

    if len(expr) == 1:
        # Si un seul argument est fourni
        if expr[0] == "--help":
            print_help()
            return True
        elif expr[0] == "--version":
            print_version()
            return True
        else:
            return bool(expr[0])

    elif len(expr) == 2:
        # Opérateurs unaires
        op, operand = expr
        return evaluate_unary(op, operand)

    elif len(expr) == 3:
        # Opérateurs binaires
        left, op, right = expr
        return evaluate_binary(left, op, right)

    else:
        print("test: too many arguments", file=sys.stderr)
        return False


def evaluate_unary(op, operand):
    """Évalue les opérateurs unaires."""
    if op == "-n":
        return len(operand) > 0
    elif op == "-z":
        return len(operand) == 0
    elif op == "-e":
        return os.path.exists(operand)
    elif op == "-f":
        return os.path.isfile(operand)
    elif op == "-d":
        return os.path.isdir(operand)
    else:
        print(f"test: unknown unary operator {op}", file=sys.stderr)
        return False


def evaluate_binary(left, op, right):
    """Évalue les opérateurs binaires."""
    try:
        if op == "=":
            return left == right
        elif op == "!=":
            return left != right
        elif op == "-eq":
            return int(left) == int(right)
        elif op == "-ne":
            return int(left) != int(right)
        elif op == "-gt":
            return int(left) > int(right)
        elif op == "-lt":
            return int(left) < int(right)
        elif op == "-ge":
            return int(left) >= int(right)
        elif op == "-le":
            return int(left) <= int(right)
        else:
            print(f"test: unknown binary operator {op}", file=sys.stderr)
            return False
    except ValueError:
        print(f"test: invalid integer comparison {left} {op} {right}", file=sys.stderr)
        return False


def main():
    # Récupère les arguments sans l'analyseur argparse
    expr = sys.argv[1:]

    if not expr:
        sys.exit(1)  # Aucune expression signifie faux.

    # Évalue l'expression
    result = evaluate_expression(expr)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

