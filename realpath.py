#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein 
Email: hamdy.aea@protonmail.com
Date of creation:  24-11-2024
Last update: 24-11-2024
Version: 1.0
Description: The realpath command from GNU coreutils in Python3.  
Example of use:  python3 realpath.py file.txt
'''

import os
import sys
import errno
import argparse
from pathlib import Path

class RealpathResolver:
    def __init__(self, relative=False, quiet=False, no_symlinks=False, 
                 canonicalize=False, logical=False, physical=True, 
                 strip=False, zero=False, base_dir=None):
        self.relative = relative
        self.quiet = quiet
        self.no_symlinks = no_symlinks
        self.canonicalize = canonicalize
        self.logical = logical
        self.physical = physical
        self.strip = strip
        self.zero = zero
        self.base_dir = base_dir if base_dir else os.getcwd()
        
    def _handle_error(self, path, error):
        """Handle and report errors unless quiet mode is enabled."""
        if not self.quiet:
            print(f"realpath: {path}: {error}", file=sys.stderr)
        return None
        
    def _make_relative(self, path):
        """Convert absolute path to relative path from base_dir."""
        try:
            return os.path.relpath(path, self.base_dir)
        except ValueError:
            return path
            
    def _resolve_logical(self, path):
        """Resolve path logically (without resolving symlinks)."""
        try:
            resolved = os.path.abspath(path)
            if self.strip:
                resolved = os.path.basename(resolved)
            return resolved
        except OSError as e:
            return self._handle_error(path, str(e))
            
    def _resolve_physical(self, path):
        """Resolve path physically (resolving symlinks)."""
        try:
            resolved = os.path.realpath(path)
            if self.strip:
                resolved = os.path.basename(resolved)
            return resolved
        except OSError as e:
            return self._handle_error(path, str(e))
            
    def _canonicalize_path(self, path):
        """Canonicalize path, handling missing components."""
        try:
            p = Path(path)
            if self.canonicalize:
                # Try to resolve each component, stopping at first missing one
                parts = []
                current = Path()
                for part in p.parts:
                    current = current / part
                    try:
                        if not self.no_symlinks:
                            current = current.resolve()
                        else:
                            current = current.absolute()
                    except OSError:
                        # If component doesn't exist, just normalize the rest
                        remaining_parts = [part] + [str(p) for p in p.relative_to(current).parts[1:]]
                        current = current.parent / Path(*remaining_parts)
                        break
                p = current
            else:
                # Simple resolution
                if self.no_symlinks:
                    p = p.absolute()
                else:
                    p = p.resolve()
                    
            result = str(p)
            if self.strip:
                result = os.path.basename(result)
            return result
            
        except OSError as e:
            return self._handle_error(path, str(e))
            
    def resolve(self, path):
        """Resolve path according to specified options."""
        try:
            if self.logical:
                resolved = self._resolve_logical(path)
            elif self.physical:
                if self.canonicalize:
                    resolved = self._canonicalize_path(path)
                else:
                    resolved = self._resolve_physical(path)
            else:
                resolved = self._canonicalize_path(path)
                
            if resolved is None:
                return None
                
            if self.relative:
                resolved = self._make_relative(resolved)
                
            return resolved
            
        except OSError as e:
            return self._handle_error(path, str(e))

def main():
    parser = argparse.ArgumentParser(
        description='Print the resolved path of each path argument',
        formatter_class=argparse.RawDescriptionHelpFormatter)
        
    parser.add_argument('paths', nargs='+', help='Path(s) to resolve')
    parser.add_argument('-e', '--canonicalize-existing', action='store_true',
                        help='all components must exist')
    parser.add_argument('-m', '--canonicalize-missing', action='store_true',
                        help='no components need exist')
    parser.add_argument('-L', '--logical', action='store_true',
                        help='resolve ".." components before symlinks')
    parser.add_argument('-P', '--physical', action='store_true',
                        help='resolve symlinks as encountered (default)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='suppress error messages')
    parser.add_argument('--relative-base', metavar='DIR',
                        help='print paths relative to DIR')
    parser.add_argument('--relative-to', metavar='DIR',
                        help='print paths relative to DIR')
    parser.add_argument('-s', '--strip', '--no-newline', action='store_true',
                        help='strip filename suffix')
    parser.add_argument('-z', '--zero', action='store_true',
                        help='end each line with NUL, not newline')
    
    args = parser.parse_args()
    
    # Validate options
    if args.logical and args.physical:
        print("realpath: cannot specify both --logical and --physical", 
              file=sys.stderr)
        sys.exit(1)
        
    if args.canonicalize_existing and args.canonicalize_missing:
        print("realpath: cannot specify both --canonicalize-existing and "
              "--canonicalize-missing", file=sys.stderr)
        sys.exit(1)
        
    # Create resolver
    resolver = RealpathResolver(
        relative=bool(args.relative_to or args.relative_base),
        quiet=args.quiet,
        no_symlinks=args.logical,
        canonicalize=args.canonicalize_missing,
        logical=args.logical,
        physical=args.physical,
        strip=args.strip,
        zero=args.zero,
        base_dir=args.relative_to or args.relative_base
    )
    
    # Process all paths
    success = True
    for path in args.paths:
        resolved = resolver.resolve(path)
        if resolved is None:
            success = False
        else:
            end = '\0' if args.zero else '\n'
            print(resolved, end=end)
            
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
