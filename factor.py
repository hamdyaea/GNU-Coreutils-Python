#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  17-11-2024
Last update: 17-11-2024
Version: 1.0
Description: The factor command from GNU coreutils in Python3  
Example of use: python3 factor.py 12 15 37
'''

import sys
import argparse
import math

def prime_factors(n):
    """Return the prime factors of a number."""
    factors = []
    
    # Handle 2 separately for efficiency
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check for odd factors from 3 to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    
    # If n is a prime number greater than 2
    if n > 2:
        factors.append(n)
    
    return factors

def format_factors(factors, exponents=False):
    """Format factors as 'p^e' or just 'p' depending on the `exponents` flag."""
    factor_dict = {}
    for factor in factors:
        factor_dict[factor] = factor_dict.get(factor, 0) + 1
    
    result = []
    for factor, count in sorted(factor_dict.items()):
        if exponents and count > 1:
            result.append(f"{factor}^{count}")
        else:
            result.append(str(factor))
    
    return ' '.join(result)

def process_input(numbers, exponents):
    """Process a list of numbers, print their prime factors."""
    for num in numbers:
        factors = prime_factors(num)
        print(f"{num}: {format_factors(factors, exponents)}")

def main():
    parser = argparse.ArgumentParser(
        description="Print the prime factors of each specified integer NUMBER."
    )
    parser.add_argument(
        "-e", "--exponents", action="store_true", 
        help="Print repeated factors in form p^e unless e is 1."
    )
    parser.add_argument(
        "--version", action="version", version="factor.py 1.0", 
        help="Show version and exit."
    )
    parser.add_argument(
        "numbers", nargs="*", type=int, default=None,
        help="Numbers to factorize. If not specified, read from standard input."
    )
    args = parser.parse_args()

    if not args.numbers:
        # Read numbers from standard input
        try:
            numbers = [int(line.strip()) for line in sys.stdin]
        except ValueError:
            print("Error: Invalid number input.", file=sys.stderr)
            sys.exit(1)
    else:
        numbers = args.numbers

    # Process the numbers
    process_input(numbers, args.exponents)

if __name__ == "__main__":
    main()

