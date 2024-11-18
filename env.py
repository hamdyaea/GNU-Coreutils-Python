#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  18-11-2024
Last update: 18-11-2024
Version: 1.0
Description: The env command from GNU coreutils in Python3  
Example of use: python3 env.py 
'''
import os
import sys
import argparse
import signal
import shlex

class EnvCommand:
    def __init__(self):
        self.parser = self.create_argument_parser()

    def create_argument_parser(self):
        """Create argument parser for env command."""
        parser = argparse.ArgumentParser(
            description='Run a program in a modified environment',
            add_help=False  # Disable default help to handle it manually
        )
        
        # Environment manipulation
        parser.add_argument('-i', '--ignore-environment', 
                            action='store_true',
                            help='Start with an empty environment')
        parser.add_argument('-u', '--unset', 
                            action='append', 
                            help='Remove variable from the environment')
        parser.add_argument('-0', '--null', 
                            action='store_true', 
                            help='End each output line with NUL, not newline')
        
        # Command modification
        parser.add_argument('-a', '--argv0', 
                            help='Pass ARG as the zeroth argument of COMMAND')
        parser.add_argument('-C', '--chdir', 
                            help='Change working directory to DIR')
        parser.add_argument('-S', '--split-string', 
                            help='Process and split string into separate arguments')
        parser.add_argument('-v', '--debug', 
                            action='store_true', 
                            help='Print verbose information for each processing step')
        
        # Signal handling
        parser.add_argument('--block-signal', 
                            help='Block delivery of specified signal(s)')
        parser.add_argument('--default-signal', 
                            help='Reset handling of signal(s) to default')
        parser.add_argument('--ignore-signal', 
                            help='Set handling of signal(s) to do nothing')
        parser.add_argument('--list-signal-handling', 
                            action='store_true', 
                            help='List non-default signal handling to stderr')
        
        # Additional arguments for environment variables and command
        parser.add_argument('env_vars', 
                            nargs='*', 
                            help='Environment variables and command')
        
        return parser

    def parse_env_vars(self, env_vars):
        """Parse environment variables from arguments."""
        env_dict = {}
        command_start = None
        
        for i, arg in enumerate(env_vars):
            if '=' in arg:
                key, value = arg.split('=', 1)
                env_dict[key] = value
            else:
                command_start = i
                break
        
        return env_dict, env_vars[command_start:] if command_start is not None else None

    def handle_signals(self, args):
        """Handle signal-related arguments."""
        if args.block_signal:
            self.block_signals(args.block_signal)
        if args.default_signal:
            self.reset_signal_handling(args.default_signal)
        if args.ignore_signal:
            self.ignore_signals(args.ignore_signal)
        if args.list_signal_handling:
            self.list_signal_handling()

    def block_signals(self, signals):
        """Block specified signals."""
        for sig in self.parse_signals(signals):
            signal.pthread_sigmask(signal.SIG_BLOCK, [sig])

    def reset_signal_handling(self, signals):
        """Reset signal handling to default."""
        for sig in self.parse_signals(signals):
            signal.signal(sig, signal.SIG_DFL)

    def ignore_signals(self, signals):
        """Ignore specified signals."""
        for sig in self.parse_signals(signals):
            signal.signal(sig, signal.SIG_IGN)

    def parse_signals(self, signals_str):
        """Parse signal names or numbers."""
        signals = []
        for sig in signals_str.split(','):
            try:
                # Try to convert to signal number if it's a number
                sig_num = int(sig)
                signals.append(sig_num)
            except ValueError:
                # Convert signal name to number
                try:
                    sig_num = getattr(signal, f'SIG{sig.upper()}')
                    signals.append(sig_num)
                except AttributeError:
                    print(f"Warning: Unknown signal '{sig}'", file=sys.stderr)
        return signals

    def list_signal_handling(self):
        """List non-default signal handling."""
        for name in dir(signal):
            if name.startswith('SIG') and not name.startswith('SIG_'):
                try:
                    sig = getattr(signal, name)
                    handler = signal.getsignal(sig)
                    if handler != signal.SIG_DFL:
                        print(f"{name}: {handler}", file=sys.stderr)
                except Exception:
                    pass

    def run(self):
        """Main env command execution."""
        # Parse arguments, leaving unknown arguments for command
        args, unknown = self.parser.parse_known_args()
        
        # Prepare environment
        if args.ignore_environment:
            os.environ.clear()
        
        # Process environment variables from arguments
        env_vars, unknown = self.parse_env_vars(unknown)
        os.environ.update(env_vars)
        
        # Unset variables
        if args.unset:
            for var in args.unset:
                os.environ.pop(var, None)
        
        # Handle signals
        self.handle_signals(args)
        
        # Change directory if specified
        if args.chdir:
            os.chdir(args.chdir)
        
        # If no command, print environment
        if not unknown:
            self.print_environment(args.null)
            return 0
        
        # Prepare command
        command = unknown[0]
        command_args = unknown[1:] if len(unknown) > 1 else []
        
        # Handle split-string option
        if args.split_string:
            command_args = shlex.split(args.split_string) + command_args
        
        # Debug output
        if args.debug:
            self.print_debug_info(command, command_args, env_vars)
        
        # Execute command
        try:
            # Use argv0 if specified, otherwise use command
            argv0 = args.argv0 or command
            os.execvpe(command, [argv0] + command_args, os.environ)
        except FileNotFoundError:
            print(f"env: '{command}': No such file or directory", file=sys.stderr)
            return 127
        except PermissionError:
            print(f"env: '{command}': Cannot invoke command", file=sys.stderr)
            return 126
        except Exception as e:
            print(f"env: Command execution failed: {e}", file=sys.stderr)
            return 125

    def print_environment(self, use_null=False):
        """Print environment variables."""
        end_char = '\0' if use_null else '\n'
        for key, value in sorted(os.environ.items()):
            print(f"{key}={value}", end=end_char)

    def print_debug_info(self, command, args, env_vars):
        """Print debug information for verbose mode."""
        print("-- Environment --", file=sys.stderr)
        for key, value in env_vars.items():
            print(f"{key}={value}", file=sys.stderr)
        print("\n-- Command --", file=sys.stderr)
        print(f"Command: {command}", file=sys.stderr)
        print("Arguments:", args, file=sys.stderr)

def main():
    env_cmd = EnvCommand()
    sys.exit(env_cmd.run())

if __name__ == '__main__':
    main()
