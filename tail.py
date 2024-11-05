#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  5-11-2024
Last update: 5-11-2024
Version: 1.0
Description: The tail command from GNU coreutils in python3.  
Example of use: python3 tail.py -n 20 myfile.txt
'''
import os
import sys
import time
import argparse

def tail(file, num_lines=10, num_bytes=None, follow=False, zero_terminated=False):
    if file == '-':
        f = sys.stdin
    else:
        f = open(file, 'rb' if num_bytes is not None else 'r')

    if num_bytes is not None:
        # Read the last num_bytes
        f.seek(0, os.SEEK_END)
        size = f.tell()
        start = max(0, size - num_bytes)
        f.seek(start)
        data = f.read()
        if zero_terminated:
            print(data.decode(errors='replace').replace('\n', '\0'), end='')
        else:
            print(data.decode(errors='replace'), end='')
    else:
        # Read the last num_lines
        lines = []
        if zero_terminated:
            for line in f:
                lines.append(line.replace(b'\0', b'\n').decode(errors='replace'))
                if len(lines) > num_lines:
                    lines.pop(0)
        else:
            for line in f:
                lines.append(line)  # No decode needed here
                if len(lines) > num_lines:
                    lines.pop(0)

        print(''.join(lines), end='')

    if follow:
        try:
            while True:
                if not os.path.exists(file):  # Check if the file still exists
                    print(f"\nFile '{file}' has been removed or renamed.")
                    break
                
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                if zero_terminated:
                    print(line.replace(b'\0', b'\n').decode(errors='replace'), end=' ')
                else:
                    print(line, end='')  # No decode needed here either

        except KeyboardInterrupt:
            print("\nStopped by user.")
        finally:
            f.close()  # Ensure the file is closed properly

def main():
    parser = argparse.ArgumentParser(description='Output the last part of files')
    parser.add_argument('files', nargs='*', default=['-'], help='Files to read from')
    parser.add_argument('-n', '--lines', type=int, default=10, help='Output the last NUM lines')
    parser.add_argument('-c', '--bytes', type=int, help='Output the last NUM bytes')
    parser.add_argument('-f', '--follow', action='store_true', help='Output appended data as the file grows')
    parser.add_argument('-z', '--zero-terminated', action='store_true', help='Line delimiter is NUL, not newline')
    
    args = parser.parse_args()

    for file in args.files:
        if args.bytes is not None and args.lines is not None:
            print("Error: Cannot use both -c and -n options.")
            sys.exit(1)
        tail(file, num_lines=args.lines, num_bytes=args.bytes, follow=args.follow, zero_terminated=args.zero_terminated)

if __name__ == '__main__':
    main()

