#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version:  1.0
Description:  The mkfifo command from GNU coreutils in Python3. 
Example of use: python3 mkfifo.py mypipe
'''


import os
import sys
import stat
import argparse
import errno

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create named pipes (FIFOs)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  mkfifo pipe     Create a FIFO named 'pipe'
  mkfifo -m 644 pipe     Create a FIFO with specific permissions
        '''
    )
    
    parser.add_argument(
        'names',
        nargs='+',
        help='Names of FIFOs to create'
    )
    
    parser.add_argument(
        '-m', '--mode',
        type=lambda x: int(x, 8),  # Convert octal string to integer
        default=0o666,
        help='Set file permission bits (as in chmod), default is 666 in octal'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0'
    )
    
    return parser.parse_args()

def create_fifo(name, mode):
    """
    Create a FIFO with the given name and mode.
    
    Args:
        name (str): Name of the FIFO to create
        mode (int): Permission bits for the FIFO
        
    Returns:
        bool: True if successful, False if an error occurred
    """
    try:
        os.mkfifo(name, mode)
        return True
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(f"mkfifo: cannot create fifo '{name}': File exists", 
                  file=sys.stderr)
        elif e.errno == errno.EACCES:
            print(f"mkfifo: cannot create fifo '{name}': Permission denied", 
                  file=sys.stderr)
        else:
            print(f"mkfifo: cannot create fifo '{name}': {e.strerror}", 
                  file=sys.stderr)
        return False

def main():
    """Main program entry point."""
    args = parse_args()
    
    # Create each requested FIFO
    exit_code = 0
    for name in args.names:
        if not create_fifo(name, args.mode):
            exit_code = 1
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
