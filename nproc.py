#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0 
Description: The nproc command from GNU coreutils in Python3. 
Example of use: python3 nproc.py --all
'''
import os
import sys
import multiprocessing

def get_cpu_count(ignore=False):
    """
    Get number of processing units available
    
    Args:
    ignore (bool): Ignore number of restricted CPUs
    """
    try:
        if ignore:
            # Total number of CPUs in the system
            return os.cpu_count()
        else:
            # Number of processing units available to the process
            return len(os.sched_getaffinity(0))
    except Exception:
        # Fallback to multiprocessing method
        return multiprocessing.cpu_count()

def main():
    # Parse command-line arguments
    ignore = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            ignore = True
        else:
            print("Usage: nproc [--all]", file=sys.stderr)
            sys.exit(1)
    
    # Print number of processing units
    print(get_cpu_count(ignore))

if __name__ == "__main__":
    main()
