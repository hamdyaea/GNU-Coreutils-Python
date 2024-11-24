#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The dd command from GNU coreutils in Python3.  
Example of use: python3 dd.py if=source.img of=destination.img
'''


import os
import sys
import time
import signal
import argparse
from datetime import datetime
from typing import BinaryIO, Optional, Dict, Any

class DDStats:
    def __init__(self):
        self.bytes_copied = 0
        self.start_time = time.time()
        self.blocks_in = 0
        self.blocks_out = 0
        self.partial_in = 0
        self.partial_out = 0

    def print_stats(self, final: bool = False) -> None:
        """Print transfer statistics."""
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            elapsed = 0.000001  # Avoid division by zero
            
        speed = self.bytes_copied / elapsed
        
        records_in = f"{self.blocks_in}+{self.partial_in}" if self.partial_in else str(self.blocks_in)
        records_out = f"{self.blocks_out}+{self.partial_out}" if self.partial_out else str(self.blocks_out)
        
        msg = (
            f"{self.bytes_copied} bytes ({self.bytes_copied/1024/1024:.1f} MB) copied, "
            f"{elapsed:.6f} seconds, "
            f"{speed/1024/1024:.1f} MB/s\n"
            f"{records_in} records in\n"
            f"{records_out} records out"
        )
        
        if final:
            print(msg)
        else:
            print(msg, file=sys.stderr)

class DD:
    def __init__(self, args: Dict[str, str]):
        self.args = args
        self.stats = DDStats()
        self.setup_signal_handlers()

    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for SIGUSR1 and SIGINT."""
        signal.signal(signal.SIGUSR1, self.handle_sigusr1)
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigusr1(self, signum: int, frame: Any) -> None:
        """Handle SIGUSR1 by printing current statistics."""
        self.stats.print_stats()

    def handle_sigint(self, signum: int, frame: Any) -> None:
        """Handle SIGINT (Ctrl+C) by printing final statistics and exiting."""
        self.stats.print_stats(final=True)
        sys.exit(130)  # 128 + SIGINT(2)

    def open_file(self, filename: str, mode: str) -> BinaryIO:
        """Open a file or device with proper handling of special files."""
        if filename == '-':
            return sys.stdin.buffer if 'r' in mode else sys.stdout.buffer
        
        if filename in ['/dev/null', 'NUL']:
            return open(os.devnull, mode)
            
        return open(filename, mode)

    def convert_size(self, size_str: str) -> int:
        """Convert size string with optional suffix to bytes."""
        if not size_str:
            return 0
            
        suffixes = {
            'c': 1,        # bytes
            'w': 2,        # words
            'b': 512,      # blocks
            'k': 1024,     # kilobytes
            'M': 1024**2,  # megabytes
            'G': 1024**3,  # gigabytes
        }
        
        if size_str[-1] in suffixes:
            return int(size_str[:-1]) * suffixes[size_str[-1]]
        return int(size_str)

    def copy(self) -> None:
        """Perform the copy operation."""
        # Convert sizes
        bs = self.convert_size(self.args.get('bs', ''))
        ibs = self.convert_size(self.args.get('ibs', '')) if self.args.get('ibs') else bs or 512
        obs = self.convert_size(self.args.get('obs', '')) if self.args.get('obs') else bs or 512
        count = self.convert_size(self.args.get('count', ''))
        skip = self.convert_size(self.args.get('skip', ''))
        seek = self.convert_size(self.args.get('seek', ''))

        try:
            with self.open_file(self.args['if'], 'rb') as inf, \
                 self.open_file(self.args['of'], 'wb') as outf:
                
                # Skip input blocks if requested
                if skip > 0:
                    inf.seek(skip * ibs)
                
                # Seek output blocks if requested
                if seek > 0:
                    outf.seek(seek * obs)
                
                # Main copy loop
                buffer = bytearray(ibs)
                blocks_copied = 0
                
                while True:
                    if count and blocks_copied >= count:
                        break
                    
                    # Read input
                    bytes_read = inf.readinto(buffer)
                    if bytes_read == 0:  # EOF
                        break
                    
                    # Update input statistics
                    if bytes_read == ibs:
                        self.stats.blocks_in += 1
                    else:
                        self.stats.partial_in += 1
                    
                    # Handle conversion and write output
                    data_to_write = buffer[:bytes_read]
                    
                    # Handle conversion flags
                    conv_flags = self.args.get('conv', '').split(',')
                    if conv_flags and conv_flags[0]:
                        if 'lcase' in conv_flags:
                            data_to_write = data_to_write.lower()
                        if 'ucase' in conv_flags:
                            data_to_write = data_to_write.upper()
                        if 'ascii' in conv_flags:
                            data_to_write = data_to_write.decode('ascii').encode('ascii')
                    
                    # Write output in obs-sized chunks
                    for i in range(0, len(data_to_write), obs):
                        chunk = data_to_write[i:i + obs]
                        bytes_written = outf.write(chunk)
                        
                        # Update output statistics
                        if bytes_written == obs:
                            self.stats.blocks_out += 1
                        else:
                            self.stats.partial_out += 1
                        
                        self.stats.bytes_copied += bytes_written
                        
                        # Sync if requested
                        if conv_flags and 'fsync' in conv_flags:
                            outf.flush()
                            os.fsync(outf.fileno())
                    
                    blocks_copied += 1
                
                # Final sync if requested
                if conv_flags and 'fsync' in conv_flags:
                    outf.flush()
                    os.fsync(outf.fileno())

        except IOError as e:
            print(f"dd: {str(e)}", file=sys.stderr)
            sys.exit(1)

def parse_command_line() -> Dict[str, str]:
    """Parse command line arguments in dd style (arg=value)."""
    args = {}
    for arg in sys.argv[1:]:
        if '=' not in arg:
            print(f"dd: invalid argument '{arg}'", file=sys.stderr)
            sys.exit(1)
            
        key, value = arg.split('=', 1)
        args[key] = value
    return args

def main() -> None:
    """Main program entry point."""
    if len(sys.argv) < 3:
        print("Usage: dd if=SOURCE of=DEST [bs=N] [count=N] [skip=N] [seek=N] [conv=CONV]", file=sys.stderr)
        sys.exit(1)
        
    args = parse_command_line()
    
    # Check required arguments
    if 'if' not in args:
        print("dd: missing 'if=' operand", file=sys.stderr)
        sys.exit(1)
    if 'of' not in args:
        print("dd: missing 'of=' operand", file=sys.stderr)
        sys.exit(1)
    
    dd = DD(args)
    dd.copy()
    dd.stats.print_stats(final=True)

if __name__ == '__main__':
    main()
