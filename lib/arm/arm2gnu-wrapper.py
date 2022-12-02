#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run

if __name__ == '__main__':
    parser = ArgumentParser(description='Wraps around the Perl script to pipe input and output')
    parser.add_argument('--program', help="Line to feed to subprocess.run as program")
    parser.add_argument('infile', type=Path, help='Source file')
    args = parser.parse_args()

    run(args.program.split(), stdin=args.infile.open(), check=True)
