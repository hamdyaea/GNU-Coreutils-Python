#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The uptime command from GNU coreutils in Python3.  
Example of use: python3 uptime.py --pretty
'''


import argparse
import datetime
import os
import time
from pathlib import Path

def get_load_averages():
    """Get system load averages for 1, 5, and 15 minutes."""
    try:
        with open('/proc/loadavg', 'r') as f:
            loads = f.read().split()[:3]
            return [float(load) for load in loads]
    except (IOError, ValueError):
        return [0.0, 0.0, 0.0]

def get_uptime_seconds(container=False):
    """Get system uptime in seconds."""
    if container and os.environ.get('PROCPS_CONTAINER'):
        # For container uptime
        try:
            with open('/proc/uptime', 'r') as f:
                return float(f.read().split()[0])
        except (IOError, ValueError):
            return 0
    else:
        # For system uptime
        try:
            with open('/proc/uptime', 'r') as f:
                return float(f.read().split()[0])
        except (IOError, ValueError):
            return 0

def get_user_count():
    """Get number of currently logged in users."""
    try:
        users = set()
        utmp_path = Path('/var/run/utmp')
        if utmp_path.exists():
            # In a real implementation, you'd need to properly parse the utmp binary file
            # This is a simplified version that uses 'who' command output
            import subprocess
            result = subprocess.run(['who'], capture_output=True, text=True)
            return len(result.stdout.splitlines())
        return 0
    except Exception:
        return 0

def format_uptime(seconds, pretty=False):
    """Format uptime duration in human readable format."""
    days = int(seconds // (24 * 3600))
    hours = int((seconds % (24 * 3600)) // 3600)
    minutes = int((seconds % 3600) // 60)

    if pretty:
        parts = []
        if days > 0:
            parts.append(f"{days} {'day' if days == 1 else 'days'}")
        if hours > 0:
            parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        if minutes > 0:
            parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        return ", ".join(parts)
    else:
        if days > 0:
            return f"{days} day{'s' if days != 1 else ''}, {hours:02d}:{minutes:02d}"
        return f"{hours:02d}:{minutes:02d}"

def main():
    parser = argparse.ArgumentParser(description='Tell how long the system has been running.')
    parser.add_argument('-c', '--container', action='store_true',
                      help='show the container uptime instead of system uptime')
    parser.add_argument('-p', '--pretty', action='store_true',
                      help='show uptime in pretty format')
    parser.add_argument('-r', '--raw', action='store_true',
                      help='display raw values (seconds)')
    parser.add_argument('-s', '--since', action='store_true',
                      help='system up since, in yyyy-mm-dd HH:MM:SS format')
    parser.add_argument('-V', '--version', action='version',
                      version='uptime from procps-ng 3.3.17')

    args = parser.parse_args()

    # Get basic information
    uptime_seconds = get_uptime_seconds(args.container)
    current_time = time.time()
    user_count = get_user_count()
    load_averages = get_load_averages()

    # Handle different output formats
    if args.raw:
        print(f"{int(current_time)} {int(uptime_seconds)}")
        return

    if args.since:
        boot_time = datetime.datetime.fromtimestamp(current_time - uptime_seconds)
        print(boot_time.strftime('%Y-%m-%d %H:%M:%S'))
        return

    # Standard output format
    current_time_str = time.strftime("%H:%M:%S")
    uptime_str = format_uptime(uptime_seconds, args.pretty)
    
    if args.pretty:
        output = f"up {uptime_str}"
    else:
        output = f" {current_time_str} up {uptime_str},"
    
    output += f" {user_count} {'user' if user_count == 1 else 'users'},"
    output += f" load average: {load_averages[0]:.2f}, {load_averages[1]:.2f}, {load_averages[2]:.2f}"
    
    print(output)

if __name__ == "__main__":
    main()
