#! /usr/bin/env python3
# encoding: utf-8

import argparse
import shuft


def cli():
    """Command line."""
    parser = argparse.ArgumentParser(description='''
        Upload directories or files, e.g.
        "shuft local_dir files.server.com /tmp/remote_dir/ --username USER"'
        ''')
    parser.add_argument('localpath', type=str,
                        help='an integer for the accumulator')

    parser.add_argument('remote', type=str,
                        help='an integer for the accumulator')

    parser.add_argument('remotepath', type=str,
                        help='an integer for the accumulator')

    parser.add_argument('--username', type=str,
                        help='an integer for the accumulator')

    parser.add_argument('--zip', action='store_true',
                        help='an integer for the accumulator')

    args = parser.parse_args()
    shuft.run(args)


if __name__ == "__main__":
    cli()
