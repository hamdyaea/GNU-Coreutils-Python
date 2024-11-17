#!/usr/bin/env python3
'''
Name:  Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version:  1.0
Description: The time command from GNU coreutils in Python3. 
Example of use:  python3 time.py sleep 2
'''

import os
import sys
import subprocess
import time
import resource
import argparse

def format_time(seconds):
    """Format elapsed time in hh:mm:ss or seconds for portability."""
    if seconds >= 60:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    return f"{seconds:.3f}s"

def collect_resource_usage():
    """Retrieve detailed resource usage statistics."""
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "user_time": usage.ru_utime,
        "sys_time": usage.ru_stime,
        "max_resident_memory": usage.ru_maxrss,
        "minor_page_faults": usage.ru_minflt,
        "major_page_faults": usage.ru_majflt,
        "voluntary_context_switches": usage.ru_nvcsw,
        "involuntary_context_switches": usage.ru_nivcsw,
    }

def run_command(args, output_file=None, append=False, portable=False):
    """Run a command and measure its execution time."""
    start_time = time.time()
    try:
        result = subprocess.run(args, check=False)
        exit_code = result.returncode
    except FileNotFoundError:
        print(f"Command not found: {args[0]}", file=sys.stderr)
        sys.exit(127)
    except PermissionError:
        print(f"Permission denied: {args[0]}", file=sys.stderr)
        sys.exit(126)
    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        sys.exit(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    usage = collect_resource_usage()

    # Format output
    if portable:
        output = (
            f"real {elapsed_time:.6f}\n"
            f"user {usage['user_time']:.6f}\n"
            f"sys {usage['sys_time']:.6f}\n"
        )
    else:
        output = (
            f"real {format_time(elapsed_time)}\n"
            f"user {usage['user_time']:.3f}s\n"
            f"sys {usage['sys_time']:.3f}s\n"
            f"max_resident_memory {usage['max_resident_memory']} KB\n"
            f"minor_page_faults {usage['minor_page_faults']}\n"
            f"major_page_faults {usage['major_page_faults']}\n"
            f"voluntary_context_switches {usage['voluntary_context_switches']}\n"
            f"involuntary_context_switches {usage['involuntary_context_switches']}\n"
        )

    # Write output
    if output_file:
        mode = "a" if append else "w"
        with open(output_file, mode) as f:
            f.write(output)
    else:
        print(output, end="")

    sys.exit(exit_code)

def main():
    parser = argparse.ArgumentParser(
        description="Run a command and measure its execution time and resource usage.",
        add_help=False
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute.")
    parser.add_argument("-p", "--portability", action="store_true", help="Use portable output format.")
    parser.add_argument("-o", "--output", metavar="file", help="Write output to a file.")
    parser.add_argument("-a", "--append", action="store_true", help="Append to the output file instead of overwriting.")
    parser.add_argument("--help", action="store_true", help="Display help and exit.")
    parser.add_argument("--version", action="store_true", help="Display version and exit.")

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(0)

    if args.version:
        print("time.py 1.0")
        sys.exit(0)

    if not args.command:
        print("time: missing command", file=sys.stderr)
        sys.exit(1)

    run_command(
        args.command,
        output_file=args.output,
        append=args.append,
        portable=args.portability
    )

if __name__ == "__main__":
    main()

