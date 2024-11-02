#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  2-11-2024
Last update: 2-11-2024
Version: 1.0
Description: A clone of the uname command from coreutils in Python3  
Example of use: python3 uname.py -a
'''

import argparse
import platform
import os

def print_uname(options):
    uname_data = {
        "-s": platform.system(),
        "-n": platform.node(),
        "-r": platform.release(),
        "-v": platform.version(),
        "-m": platform.machine(),
        "-p": platform.processor() or "unknown",
        "-i": platform.uname().processor or "unknown",
        "-o": os.name if os.name != 'posix' else "GNU/Linux",
    }

    if options.all:
        output = " ".join(uname_data[key] for key in uname_data if uname_data[key] != "unknown")
        print(output)
    else:
        output = []
        # On vérifie les options avec des clés appropriées
        if options.kernel_name:
            output.append(uname_data["-s"])
        if options.nodename:
            output.append(uname_data["-n"])
        if options.kernel_release:
            output.append(uname_data["-r"])
        if options.kernel_version:
            output.append(uname_data["-v"])
        if options.machine:
            output.append(uname_data["-m"])
        if options.processor:
            output.append(uname_data["-p"])
        if options.hardware_platform:
            output.append(uname_data["-i"])
        if options.operating_system:
            output.append(uname_data["-o"])

        # Affiche les résultats
        print(" ".join(output) if output else uname_data["-s"])

def main():
    parser = argparse.ArgumentParser(description="Print certain system information.")
    parser.add_argument("-a", "--all", action="store_true", help="print all information")
    parser.add_argument("-s", "--kernel-name", action="store_true", help="print the kernel name")
    parser.add_argument("-n", "--nodename", action="store_true", help="print the network node hostname")
    parser.add_argument("-r", "--kernel-release", action="store_true", help="print the kernel release")
    parser.add_argument("-v", "--kernel-version", action="store_true", help="print the kernel version")
    parser.add_argument("-m", "--machine", action="store_true", help="print the machine hardware name")
    parser.add_argument("-p", "--processor", action="store_true", help="print the processor type (non-portable)")
    parser.add_argument("-i", "--hardware-platform", action="store_true", help="print the hardware platform (non-portable)")
    parser.add_argument("-o", "--operating-system", action="store_true", help="print the operating system")
    parser.add_argument("--version", action="version", version="uname.py 1.0", help="output version information and exit")

    options = parser.parse_args()
    print_uname(options)

if __name__ == "__main__":
    main()

