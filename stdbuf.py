#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The sdtbuf command GNU coreutils in Python3.  
Example of use: python3 stdbuf.py -o 1K ls /
'''

import sys
import subprocess
import io

class StdBuf:
    def __init__(self):
        self.input_buffer = None
        self.output_buffer = None
        self.error_buffer = None

    def parse_size(self, size_str):
        """Parse buffer size with units (K, M, G)"""
        if not size_str or size_str == '0':
            return 0
        
        units = {'K': 1024, 'M': 1024*1024, 'G': 1024*1024*1024}
        try:
            if size_str[-1] in units:
                return int(float(size_str[:-1]) * units[size_str[-1]])
            return int(size_str)
        except ValueError:
            print(f"Invalid buffer size: {size_str}", file=sys.stderr)
            sys.exit(1)

    def run(self, args):
        """Execute command with specified buffering"""
        # Parse stdbuf arguments
        buffer_args = {
            'input': '0',
            'output': '0',
            'error': '0'
        }
        command_start = 0

        for i, arg in enumerate(args):
            if arg == '-i':
                buffer_args['input'] = args[i+1]
                command_start = i+2
            elif arg == '-o':
                buffer_args['output'] = args[i+1]
                command_start = i+2
            elif arg == '-e':
                buffer_args['error'] = args[i+1]
                command_start = i+2

        # Validate command exists
        if command_start >= len(args):
            print("Error: No command specified", file=sys.stderr)
            sys.exit(1)

        # Parse buffer sizes
        input_buf = self.parse_size(buffer_args['input'])
        output_buf = self.parse_size(buffer_args['output'])
        error_buf = self.parse_size(buffer_args['error'])

        # Execute command
        try:
            # Note: This is a simplified version. Real stdbuf has more complex buffering
            process = subprocess.Popen(
                args[command_start:], 
                bufsize=output_buf,  # Most similar to stdbuf behavior
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Capture and print output
            stdout, stderr = process.communicate()
            
            # Mimic output buffering behavior
            print(stdout, end='')
            print(stderr, file=sys.stderr, end='')

            return process.returncode

        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    stdbuf = StdBuf()
    sys.exit(stdbuf.run(sys.argv[1:]))

if __name__ == "__main__":
    main()
