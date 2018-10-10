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
                        help='Path to the local folder or file.')

    parser.add_argument('hostname', type=str,
                        help='The hostname for the remote.')

    parser.add_argument('remotepath', type=str, help='''
        The base path on the remote where the content will be uploaded.
        ''')

    parser.add_argument('--username', type=str,
                        help='the username for logging in on the remote')

    parser.add_argument(
        '--compress', action='store_true',
        help='Compress target folder or file before transmission.')

    args = parser.parse_args()
    shuft.run(args)


if __name__ == "__main__":
    cli()
