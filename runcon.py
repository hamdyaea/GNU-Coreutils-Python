#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The runcon command from GNU coreutils in Python3.  
Example of use: python3 runcon.py -u system_u ls /
'''

import os
import sys
import subprocess
import shlex

class RunCon:
    def __init__(self):
        self.context = None
        self.type = None
        self.user = None
        self.role = None
        self.range = None

    def parse_context(self, context_str):
        """
        Parse SELinux context string
        Format: user:role:type:range
        """
        parts = context_str.split(':')
        if len(parts) != 4:
            print(f"Invalid context format: {context_str}", file=sys.stderr)
            sys.exit(1)
        
        self.user, self.role, self.type, self.range = parts
        return self

    def run(self, args):
        """
        Execute command with specified SELinux context
        """
        # Parse context flags
        context_specified = False
        context_index = 0

        for i, arg in enumerate(args):
            if arg == '-t':
                # Specify type
                if i + 1 < len(args):
                    self.type = args[i + 1]
                    context_specified = True
                    context_index = i
                    break
            elif arg == '-u':
                # Specify user
                if i + 1 < len(args):
                    self.user = args[i + 1]
                    context_specified = True
                    context_index = i
                    break
            elif arg == '-r':
                # Specify role
                if i + 1 < len(args):
                    self.role = args[i + 1]
                    context_specified = True
                    context_index = i
                    break
            elif arg.count(':') == 3:
                # Full context string
                self.parse_context(arg)
                context_specified = True
                context_index = i
                break

        # Validate command exists
        if not context_specified or context_index + 1 >= len(args):
            print("Usage: runcon [-t type] [-u user] [-r role] CONTEXT command", file=sys.stderr)
            sys.exit(1)

        # Prepare command to execute
        command = args[context_index + 1:]

        try:
            # Execute command
            result = subprocess.run(command, check=False)
            return result.returncode
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    runcon = RunCon()
    sys.exit(runcon.run(sys.argv[1:]))

if __name__ == "__main__":
    main()
