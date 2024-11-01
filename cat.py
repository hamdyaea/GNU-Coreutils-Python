# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com

# This software is a copy of the famous cat linux software from coreutils.

import sys

def cat(files, show_all=False, number_nonblank=False, show_ends=False, 
        number_all=False, squeeze_blank=False, show_tabs=False, show_nonprinting=False):
    for file in files:
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
                
                if squeeze_blank:
                    lines = squeeze_empty(lines)

                for i, line in enumerate(lines):
                    # Apply options
                    if show_nonprinting:
                        line = show_nonprint(line)

                    if show_ends:
                        line = line.rstrip('\n') + '$\n'
                    
                    if show_tabs:
                        line = line.replace('\t', '^I')

                    if number_all:
                        print(f"{i + 1}\t{line}", end='')
                    elif number_nonblank and line.strip():
                        print(f"{i + 1}\t{line}", end='')
                    else:
                        print(line, end='')

        except FileNotFoundError:
            print(f"The {file} is not found.")
        except IOError as e:
            print(f"Error while opening {file}: {e}")

def squeeze_empty(lines):
    """Squeeze multiple empty lines into a single empty line."""
    squeezed = []
    for line in lines:
        if line.strip() == '':
            if not (squeezed and squeezed[-1].strip() == ''):
                squeezed.append(line)
        else:
            squeezed.append(line)
    return squeezed

def show_nonprint(line):
    """Show non-printing characters using ^ and M- notation."""
    # Replace non-printing characters, except for line feed and tab
    return ''.join(f'^{char}' if ord(char) < 32 else char for char in line)

if __name__ == "__main__":
    # Default values for options
    show_all = False
    number_nonblank = False
    show_ends = False
    number_all = False
    squeeze_blank = False
    show_tabs = False
    show_nonprinting = False

    # Process arguments
    args = sys.argv[1:]
    files = []
    
    for arg in args:
        if arg.startswith('-'):
            # Handle options
            if arg in ('-A', '--show-all'):
                show_all = True
            elif arg in ('-b', '--number-nonblank'):
                number_nonblank = True
            elif arg in ('-e'):
                show_nonprinting = True
                show_ends = True
            elif arg in ('-E', '--show-ends'):
                show_ends = True
            elif arg in ('-n', '--number'):
                number_all = True
            elif arg in ('-s', '--squeeze-blank'):
                squeeze_blank = True
            elif arg in ('-t', '--show-tabs'):
                show_tabs = True
            elif arg in ('-u'):
                pass  # Ignored
            elif arg in ('-v', '--show-nonprinting'):
                show_nonprinting = True
            elif arg in ('--help'):
                print("Usage: python3 Cat.py [file ...] [options]\n")
                print("Options:")
                print("  -A, --show-all       equivalent to -vET")
                print("  -b, --number-nonblank number nonempty output lines, overrides -n")
                print("  -e                    equivalent to -vE")
                print("  -E, --show-ends      display $ at end of each line")
                print("  -n, --number         number all output lines")
                print("  -s, --squeeze-blank  suppress repeated empty output lines")
                print("  -t, --show-tabs      display TAB characters as ^I")
                print("  -u                    (ignored)")
                print("  -v, --show-nonprinting use ^ and M- notation, except for LFD and TAB")
                print("  --help                display this help and exit")
                print("  --version             output version information and exit")
                sys.exit()
            elif arg in ('--version'):
                print("Cat.py version 1.0")
                sys.exit()
        else:
            files.append(arg)

    if files:
        cat(files, show_all, number_nonblank, show_ends, number_all, squeeze_blank, show_tabs, show_nonprinting)
    else:
        print("Usage: python3 Cat.py [file ...]")

