#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version:  1.0
Description:  The sleep command from GNU coreutils in Python3. 
Example of use: python3 sleep.py 5
'''

import sys
import time
import signal

def handle_interrupt(signum, frame):
    """Handle interrupt signals (Ctrl+C)"""
    print("\nInterrupted", file=sys.stderr)
    sys.exit(1)

def parse_duration(duration_str):
    """
    Parse sleep duration with support for:
    - Whole numbers (seconds)
    - Decimal numbers
    - Suffixes: s (seconds), m (minutes), h (hours), d (days)
    """
    try:
        # Remove whitespace and convert to lowercase
        duration_str = duration_str.strip().lower()

        # Handle suffixes
        if duration_str.endswith('s'):
            return float(duration_str[:-1])
        elif duration_str.endswith('m'):
            return float(duration_str[:-1]) * 60
        elif duration_str.endswith('h'):
            return float(duration_str[:-1]) * 3600
        elif duration_str.endswith('d'):
            return float(duration_str[:-1]) * 86400

        # Default to seconds
        return float(duration_str)

    except ValueError:
        print(f"Invalid duration: {duration_str}", file=sys.stderr)
        sys.exit(1)

def main():
    # Register signal handler for interrupt
    signal.signal(signal.SIGINT, handle_interrupt)

    # Check if arguments are provided
    if len(sys.argv) < 2:
        print("Usage: sleep DURATION[SUFFIX]", file=sys.stderr)
        sys.exit(1)

    # Calculate total sleep time
    total_sleep = 0
    for arg in sys.argv[1:]:
        total_sleep += parse_duration(arg)

    try:
        # Perform the sleep
        time.sleep(total_sleep)
    except Exception as e:
        print(f"Sleep error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
