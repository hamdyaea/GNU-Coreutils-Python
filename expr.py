#!/usr/bin/env python3
'''
Name: Hamdy Abou El Anein
Email: hamdy.aea@protonmail.com
Date of creation:  20-11-2024
Last update: 20-11-2024
Version: 1.0
Description: The expr command from GNU coreutils in Python3.  
Example of use: python3 expr.py 5 + 3
'''

import sys
import operator

def evaluate_expression(args):
    """
    Evaluate mathematical expressions passed as arguments.
    Supports basic arithmetic operations.
    """
    # Supported operators
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '%': operator.mod
    }

    # Validate input
    if len(args) != 3:
        print("Error: Expression must be in format: number operator number")
        sys.exit(1)

    try:
        # Convert first and third arguments to numbers
        num1 = float(args[0])
        num2 = float(args[2])
        
        # Get the operator
        op = args[1]
        
        # Perform calculation
        if op not in ops:
            print(f"Error: Unsupported operator '{op}'")
            sys.exit(1)
        
        # Calculate and print result
        result = ops[op](num1, num2)
        print(int(result) if result.is_integer() else result)

    except ValueError:
        print("Error: Invalid numeric input")
        sys.exit(1)

def main():
    # Remove script name from arguments
    args = sys.argv[1:]
    
    if not args:
        print("Usage: ./expr.py number operator number")
        sys.exit(1)
    
    evaluate_expression(args)

if __name__ == "__main__":
    main()
