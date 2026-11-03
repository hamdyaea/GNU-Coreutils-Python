# GNU Coreutils in Python 3

This project is a Python 3 reimplementation of key GNU Coreutils commands. It provides Python-based alternatives for some of the most commonly used Linux utilities, enabling users to execute these commands within a Python environment.

## Features

This repository contains Python scripts that emulate the behavior of popular GNU Coreutils commands. The project serves as both a learning tool and a utility set for those who wish to use coreutils functionalities in Python.

## Installation process

1. Clone this repository:
   ```bash
   git clone https://github.com/hamdyaea/GNU-Coreutils-Python.git
   ```       
                        
##  
##  
##  
##  
## 
## GitAds Sponsored
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=hamdyaea/gnu-coreutils-python@github)](https://gitads.dev/v1/ad-track?source=hamdyaea/gnu-coreutils-python@github)



<!-- GitAds-Verify: I82ZSDRB4TBGTZ5IJKZJRGKIEE13CI4V -->


## Safety maintenance

Maintainer: Hamdy Abou El Anein — hamdy.aea@protonmail.com

`rm.py` now requires `-r` for recursive removal, supports empty-directory removal with `-d`, unlinks directory and dangling symlinks without traversing their targets, respects per-file confirmation, and reports errors with a nonzero exit status. Filesystem root and dot operands are always protected. Run `python3 -m unittest -v test_rm_safety`: all destructive test operations are confined to temporary directories.

This educational collection is not a drop-in GNU Coreutils replacement. Mixed `-f`/`-i` ordering and race-resistant fd-based traversal are not implemented; do not use it on untrusted concurrently modified trees. Other commands have independent compatibility gaps (for example cp parses interactive flags without implementing the prompt, and wc differs on empty or unterminated input). Contributor attribution, including Mehdi Marhol in pwd.py, is preserved. Review the PR before using any file-modifying command.
