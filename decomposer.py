#!/usr/bin/env python3

from dataclasses import asdict
import json
import argparse
import os
import sys

from lib.igz import processIgz
from lib.utils import compareMagicByte

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='IGZ to JSON Converter')
    parser.add_argument('-i', '--input', required=True, help='Input file name')
    parser.add_argument('-o', '--output', required=True, help='Output file name')
    parser.add_argument('-f', '--force', action='store_true', help='Force overwrite output file')
    args = parser.parse_args()

    # Check input file exists
    if not os.path.exists(args.input):
        sys.exit(f"Error: Input file '{args.input}' does not exist")

    # Check output file existence
    if os.path.exists(args.output):
        if not args.force:
            # Ask for user confirmation
            response = input(f"Output file '{args.output}' exists. Overwrite? [y/N] ").strip().lower()
            if response not in ('y', 'yes'):
                print("Operation canceled")
                sys.exit(1)
                
    # If we get here, all checks passed
    print(f"Processing {args.input} -> {args.output}")
    # Add your file processing logic here

    igzMagicB = 0x49475A01
    igzMagicL = 0x015A4749

    with open(args.input, 'rb') as f:
        magic = f.read(4)
        if not magic:
            sys.exit(f"Error: Input file '{args.input}' is not an valid IGZ file")

        isIgzB = compareMagicByte(magic, igzMagicB)
        isIgzL = compareMagicByte(magic, igzMagicL)

        if isIgzB:
            print('IGZ (Big Endian) Found')
            igzFile = processIgz(f, byteorder="big")
            jsonC = json.dumps(asdict(igzFile), indent=2)
            with open(args.output, "w") as outfile:
                outfile.write(jsonC)
        elif isIgzL:
            print('IGZ (Little Endian) Found')
            igzFile = processIgz(f, byteorder="little")
            jsonC = json.dumps(asdict(igzFile), indent=2)
            with open(args.output, "w") as outfile:
                outfile.write(jsonC)
        else:
            sys.exit(f"Error: Input file '{args.input}' is not an valid IGZ file")

if __name__ == '__main__':
    main()
