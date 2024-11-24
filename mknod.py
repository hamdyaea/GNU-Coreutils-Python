#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The mknod command from GNU coreutils in Python3.  
Example of use: sudo python3 mknod.py /dev/null c 1 3 
'''


import os
import sys
import stat
import grp
import pwd
import argparse

class MknodCreator:
    def __init__(self, mode=None, major=None, minor=None):
        self.mode = mode
        self.major = major
        self.minor = minor

    def _parse_permission(self, mode_str):
        """Parse permission string (like '644') to mode bits."""
        try:
            return int(mode_str, 8)
        except ValueError:
            return None

    def _get_device_number(self):
        """Create device number from major and minor numbers."""
        if self.major is None or self.minor is None:
            return None
        return os.makedev(self.major, self.minor)

    def _validate_user_group(self, user, group):
        """Validate and get uid/gid from user/group names."""
        try:
            if user is not None:
                try:
                    uid = int(user)
                except ValueError:
                    uid = pwd.getpwnam(user).pw_uid
            else:
                uid = -1

            if group is not None:
                try:
                    gid = int(group)
                except ValueError:
                    gid = grp.getgrnam(group).gr_gid
            else:
                gid = -1

            return uid, gid
        except (KeyError, ValueError):
            raise ValueError(f"Invalid user or group: {user}:{group}")

    def create_node(self, path, node_type, user=None, group=None, perms=None):
        """
        Create a special file node.
        
        Args:
            path: Path where to create the node
            node_type: Type of node ('p'|'b'|'c')
            user: Username or UID
            group: Group name or GID
            perms: Permission string (e.g. '644')
        """
        try:
            # Determine file type
            if node_type == 'p':
                mode = stat.S_IFIFO
            elif node_type == 'b':
                mode = stat.S_IFBLK
            elif node_type == 'c':
                mode = stat.S_IFCHR
            else:
                raise ValueError(f"Invalid node type: {node_type}")

            # Add permissions
            if perms is not None:
                permission_bits = self._parse_permission(perms)
                if permission_bits is None:
                    raise ValueError(f"Invalid permission mode: {perms}")
                mode |= permission_bits
            else:
                # Default permissions: rw-rw-rw- for pipes, rw-rw---- for devices
                if node_type == 'p':
                    mode |= 0o666
                else:
                    mode |= 0o660

            # Create the special file
            if node_type == 'p':
                os.mkfifo(path, mode)
            else:
                if os.geteuid() != 0:
                    raise PermissionError("Creating device nodes requires root privileges")
                
                device = self._get_device_number()
                if device is None:
                    raise ValueError("Major and minor numbers required for device nodes")
                
                os.mknod(path, mode, device)

            # Set ownership if specified
            if user is not None or group is not None:
                try:
                    uid, gid = self._validate_user_group(user, group)
                    os.chown(path, uid, gid)
                except ValueError as e:
                    os.unlink(path)  # Clean up on error
                    raise e

            return True

        except OSError as e:
            print(f"mknod: cannot create special file '{path}': {str(e)}", 
                  file=sys.stderr)
            return False
        except ValueError as e:
            print(f"mknod: {str(e)}", file=sys.stderr)
            return False

def parse_mode(mode_str):
    """Parse mode string to determine node type and permissions."""
    if not mode_str:
        return None, None

    # Handle mode string formats
    if mode_str[0] == '0':
        # Octal format (e.g., 0600)
        try:
            mode = int(mode_str, 8)
            node_type = mode & stat.S_IFMT
            perms = mode & 0o777
            if node_type == stat.S_IFIFO:
                return 'p', oct(perms)[2:]
            elif node_type == stat.S_IFBLK:
                return 'b', oct(perms)[2:]
            elif node_type == stat.S_IFCHR:
                return 'c', oct(perms)[2:]
            else:
                return None, None
        except ValueError:
            return None, None
    else:
        # Standard format (e.g., p644)
        node_type = mode_str[0]
        if node_type in ['p', 'b', 'c']:
            perms = mode_str[1:] if len(mode_str) > 1 else None
            return node_type, perms
        return None, None

def main():
    parser = argparse.ArgumentParser(
        description='Create special files (FIFO, block, character)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  mknod.py p myfifo                Create a FIFO named 'myfifo'
  mknod.py c 1 3 /dev/null         Create a character device '/dev/null'
  mknod.py b 8 0 /dev/sda          Create a block device '/dev/sda'
        ''')

    parser.add_argument('name', help='Name of the special file to create')
    parser.add_argument('type', choices=['p', 'b', 'c'], 
                        help='Type (p: FIFO, b: block, c: character)')
    parser.add_argument('major', nargs='?', type=int, 
                        help='Major device number (for block/character devices)')
    parser.add_argument('minor', nargs='?', type=int, 
                        help='Minor device number (for block/character devices)')
    parser.add_argument('-m', '--mode', 
                        help='File permission bits (octal)')
    parser.add_argument('--user', help='User (name or numeric id)')
    parser.add_argument('--group', help='Group (name or numeric id)')

    args = parser.parse_args()

    # Validate arguments
    if args.type in ['b', 'c']:
        if args.major is None or args.minor is None:
            print("mknod: Major and minor numbers required for device nodes", 
                  file=sys.stderr)
            sys.exit(1)
    else:
        if args.major is not None or args.minor is not None:
            print("mknod: Major and minor numbers not allowed for FIFO", 
                  file=sys.stderr)
            sys.exit(1)

    # Create mknod instance
    creator = MknodCreator(
        mode=args.mode,
        major=args.major,
        minor=args.minor
    )

    # Create the node
    success = creator.create_node(
        args.name,
        args.type,
        user=args.user,
        group=args.group,
        perms=args.mode
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
