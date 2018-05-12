#!/usr/bin/env python
import argparse
import os

# This allows me to use relative imports while this is part of the package and regular imports once it is installed
try:
    from . import dash_interface
except ValueError:
    from behrdownloader import dash_interface


def parse_args():
    parser = argparse.ArgumentParser(description="Python utility to download BEHR files")
    subparsers = parser.add_subparsers()
    parser_dash_cl = subparsers.add_parser('dash', help='Download monthly tar files from the official DASH archives; '
                                                        'call {} dash --help to see subcommand options'.format(os.path.basename(__file__)))
    dash_interface.parse_args(parser_dash_cl)

    args = parser.parse_args()
    args.driver_fxn(**vars(args))


if __name__ == '__main__':
    parse_args()
