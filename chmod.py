#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  4.11.2024
Last update: 4.11.2024
Version:  1.0
Description: The command chmod from GNU coreutils in Python3 
Example of use: python3 chmod.py u+x fichier.txt
'''
import os
import stat
import sys

def apply_numeric_mode(file_path, mode):
    """Applique les permissions numériques spécifiées à un fichier."""
    new_mode = int(mode, 8)  # Convertir en entier base 8
    os.chmod(file_path, new_mode)
    print(f"Changed permissions for {file_path} to {oct(new_mode)}")

def parse_symbolic_mode(permission_str, current_mode):
    """Parse et applique les permissions symboliques spécifiées."""
    user_map = {
        'u': stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
        'g': stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP,
        'o': stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH,
        'a': (stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
              stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
              stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)
    }
    perm_map = {'r': stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
                'w': stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
                'x': stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH}

    operation = None
    users = 0
    permissions = 0

    for char in permission_str:
        if char in user_map:
            users |= user_map[char]
        elif char in '+-=':
            operation = char
        elif char in perm_map:
            permissions |= perm_map[char]
        elif char == ',':
            # Applique les changements pour chaque segment séparé par des virgules
            current_mode = update_mode(current_mode, users, permissions, operation)
            users, permissions, operation = 0, 0, None

    # Applique le dernier segment
    if operation:
        current_mode = update_mode(current_mode, users, permissions, operation)

    return current_mode

def update_mode(current_mode, users, permissions, operation):
    """Met à jour les permissions en fonction de l'opération (+, -, =) spécifiée."""
    if operation == '+':
        current_mode |= (users & permissions)
    elif operation == '-':
        current_mode &= ~(users & permissions)
    elif operation == '=':
        current_mode &= ~users  # Réinitialise les permissions pour les utilisateurs spécifiés
        current_mode |= (users & permissions)
    return current_mode

def main(args):
    if len(args) < 2:
        print("Usage: chmod.py <mode> <file>")
        return
    
    permission_str = args[0]
    file_path = args[1]

    # Vérifiez si les permissions sont numériques
    if permission_str.isdigit():
        apply_numeric_mode(file_path, permission_str)
    else:
        # Appliquer les changements symboliques
        current_mode = stat.S_IMODE(os.lstat(file_path).st_mode)
        new_mode = parse_symbolic_mode(permission_str, current_mode)
        os.chmod(file_path, new_mode)
        print(f"Changed permissions for {file_path} to {oct(new_mode)}")

if __name__ == "__main__":
    main(sys.argv[1:])

