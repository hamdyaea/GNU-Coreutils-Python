#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The timeout command from GNU coreutils in Python3.  
Example of use: python3 timeout.py 10s command 
'''

import os
import sys
import time
import signal
import subprocess
import argparse
import re

class TimeoutCommand:
    def __init__(self):
        self.parser = self.create_argument_parser()

    def create_argument_parser(self):
        """Create argument parser for timeout command."""
        parser = argparse.ArgumentParser(
            description='Run a command with a time limit',
            add_help=False  # Disable default help
        )
        
        # Timeout and signal options
        parser.add_argument('-k', '--kill-after', 
                            help='Send KILL signal after specified duration')
        parser.add_argument('-s', '--signal', 
                            default='TERM', 
                            help='Signal to send on timeout (default: TERM)')
        
        # Behavior modifiers
        parser.add_argument('--preserve-status', 
                            action='store_true',
                            help='Exit with the same status as COMMAND')
        parser.add_argument('--foreground', 
                            action='store_true',
                            help='Allow COMMAND to read from TTY and get TTY signals')
        parser.add_argument('-v', '--verbose', 
                            action='store_true',
                            help='Diagnose signals sent upon timeout')
        
        # Duration and command arguments
        parser.add_argument('duration', 
                            help='Timeout duration')
        parser.add_argument('command', 
                            nargs=argparse.REMAINDER, 
                            help='Command to run')
        
        return parser

    def parse_duration(self, duration_str):
        """Parse duration string to seconds."""
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([smhd])?$', duration_str)
        if not match:
            raise ValueError(f"Invalid duration format: {duration_str}")
        
        value = float(match.group(1))
        unit = match.group(2) or 's'
        
        units = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400
        }
        
        return value * units[unit]

    def get_signal_number(self, signal_name):
        """Convert signal name to signal number."""
        try:
            # Try to get signal number directly
            return getattr(signal, f'SIG{signal_name.upper()}')
        except AttributeError:
            try:
                # Try to convert from string number
                return int(signal_name)
            except ValueError:
                print(f"timeout: invalid signal '{signal_name}'", file=sys.stderr)
                sys.exit(125)

    def run(self):
        """Main timeout command execution."""
        # Parse arguments
        args = self.parser.parse_args()
        
        # Validate input
        if not args.command:
            print("timeout: missing command", file=sys.stderr)
            sys.exit(125)
        
        # Parse durations
        try:
            timeout_duration = self.parse_duration(args.duration)
            kill_duration = (self.parse_duration(args.kill_after) 
                             if args.kill_after else None)
        except ValueError as e:
            print(f"timeout: {e}", file=sys.stderr)
            sys.exit(125)
        
        # Get signal to send
        timeout_signal = self.get_signal_number(args.signal)
        
        try:
            # Run the command
            start_time = time.time()
            
            # Use subprocess to run the command
            process = subprocess.Popen(args.command)
            
            while process.poll() is None:
                # Check if timeout has been reached
                elapsed_time = time.time() - start_time
                
                if elapsed_time >= timeout_duration:
                    # Send timeout signal
                    if args.verbose:
                        print(f"timeout: sending {args.signal} signal to {process.pid}", 
                              file=sys.stderr)
                    
                    os.kill(process.pid, timeout_signal)
                    
                    # Wait for kill-after duration if specified
                    if kill_duration:
                        try:
                            process.wait(timeout=kill_duration)
                        except subprocess.TimeoutExpired:
                            # Force kill if still running
                            if args.verbose:
                                print(f"timeout: sending KILL signal to {process.pid}", 
                                      file=sys.stderr)
                            os.kill(process.pid, signal.SIGKILL)
                    
                    # Wait for process to terminate
                    process.wait()
                    
                    # Exit with appropriate status
                    if not args.preserve_status:
                        sys.exit(124)
                    
                    break
                
                # Small sleep to prevent busy waiting
                time.sleep(0.1)
            
            # Return the command's exit status
            sys.exit(process.returncode or 0)
        
        except FileNotFoundError:
            print(f"timeout: cannot run '{args.command[0]}'", file=sys.stderr)
            sys.exit(127)
        except PermissionError:
            print(f"timeout: cannot invoke '{args.command[0]}'", file=sys.stderr)
            sys.exit(126)
        except Exception as e:
            print(f"timeout: unexpected error: {e}", file=sys.stderr)
            sys.exit(125)

def main():
    timeout_cmd = TimeoutCommand()
    timeout_cmd.run()

if __name__ == '__main__':
    main()
