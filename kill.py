#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The kill command from GNU coreutils in Python3.  
Example of use:  python3 kill.py -l
'''


import os
import sys
import signal
import argparse
import logging
from typing import List, Dict, Optional

# Dictionary mapping signal names to their numbers
SIGNAL_MAP: Dict[str, int] = {
    # Standard signals
    'SIGHUP': 1,    # Hangup
    'SIGINT': 2,    # Interrupt
    'SIGQUIT': 3,   # Quit
    'SIGILL': 4,    # Illegal instruction
    'SIGTRAP': 5,   # Trace/breakpoint trap
    'SIGABRT': 6,   # Abort
    'SIGBUS': 7,    # Bus error
    'SIGFPE': 8,    # Floating point exception
    'SIGKILL': 9,   # Kill (cannot be caught or ignored)
    'SIGUSR1': 10,  # User defined signal 1
    'SIGSEGV': 11,  # Segmentation fault
    'SIGUSR2': 12,  # User defined signal 2
    'SIGPIPE': 13,  # Broken pipe
    'SIGALRM': 14,  # Alarm clock
    'SIGTERM': 15,  # Termination
    'SIGSTKFLT': 16,# Stack fault
    'SIGCHLD': 17,  # Child stopped or terminated
    'SIGCONT': 18,  # Continue
    'SIGSTOP': 19,  # Stop (cannot be caught or ignored)
    'SIGTSTP': 20,  # Keyboard stop
    'SIGTTIN': 21,  # Background process attempting read
    'SIGTTOU': 22,  # Background process attempting write
    'SIGURG': 23,   # Urgent condition on socket
    'SIGXCPU': 24,  # CPU time limit exceeded
    'SIGXFSZ': 25,  # File size limit exceeded
    'SIGVTALRM': 26,# Virtual timer expired
    'SIGPROF': 27,  # Profiling timer expired
    'SIGWINCH': 28, # Window size changed
    'SIGIO': 29,    # I/O possible
    'SIGPWR': 30,   # Power failure
    'SIGSYS': 31,   # Bad system call
}

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        stream=sys.stderr
    )

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description='Send signals to processes.',
        usage='%(prog)s [-s SIGNAL | -SIGNAL] PID...'
    )
    
    parser.add_argument(
        'pids',
        nargs='*',
        type=str,
        help='Process IDs or names to send signals to'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List signal names'
    )
    
    parser.add_argument(
        '-s', '--signal',
        type=str,
        default='SIGTERM',
        help='Specify the signal to send (name or number)'
    )
    
    return parser

def list_signals() -> None:
    """Print all available signals."""
    for name, num in sorted(SIGNAL_MAP.items(), key=lambda x: x[1]):
        print(f"{num}) {name[3:]} ({name})")

def parse_signal(signal_str: str) -> int:
    """
    Parse signal string to get signal number.
    Accepts signal names (with or without 'SIG' prefix) or numbers.
    """
    signal_str = signal_str.upper()
    
    # If it's a number
    if signal_str.isdigit():
        return int(signal_str)
    
    # Add 'SIG' prefix if not present
    if not signal_str.startswith('SIG'):
        signal_str = 'SIG' + signal_str
    
    # Look up in signal map
    if signal_str in SIGNAL_MAP:
        return SIGNAL_MAP[signal_str]
    
    logging.error(f"Invalid signal specification: {signal_str}")
    sys.exit(1)

def send_signal(pid_str: str, sig_num: int) -> bool:
    """
    Send signal to the specified process.
    Returns True if successful, False otherwise.
    """
    try:
        pid = int(pid_str)
        os.kill(pid, sig_num)
        return True
    except ValueError:
        logging.error(f"Invalid process id: {pid_str}")
    except ProcessLookupError:
        logging.error(f"Process {pid_str} does not exist")
    except PermissionError:
        logging.error(f"Permission denied for process {pid_str}")
    except OSError as e:
        logging.error(f"Error sending signal to process {pid_str}: {e}")
    return False

def main() -> None:
    """Main function implementing kill functionality."""
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()

    # Handle --list option
    if args.list:
        list_signals()
        sys.exit(0)

    # Check if we have PIDs to process
    if not args.pids:
        parser.print_help()
        sys.exit(1)

    # Parse signal specification
    try:
        # Handle cases like '-9' as first argument
        if args.pids[0].startswith('-') and args.pids[0][1:].isdigit():
            signal_spec = args.pids[0][1:]
            pids = args.pids[1:]
        else:
            signal_spec = args.signal
            pids = args.pids

        sig_num = parse_signal(signal_spec)

    except ValueError as e:
        logging.error(f"Invalid signal specification: {e}")
        sys.exit(1)

    # Send signal to each specified PID
    success = True
    for pid in pids:
        if not send_signal(pid, sig_num):
            success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
