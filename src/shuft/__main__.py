#! /usr/bin/env python3
# encoding: utf-8

import argparse
import asyncio
import asyncssh
import sys

import shuft


def cli(args):
    """Command line."""
    parser = argparse.ArgumentParser(description='''
        Upload directories or files, e.g.
        "shuft local_dir files.server.com /tmp/remote_dir/ --username USER"'
        ''')

    parser.add_argument('localpath', type=str,
                        help='Path to the local folder or file.')

    parser.add_argument('host', type=str,
                        help='The name of the host for the remote.')

    parser.add_argument('remotepath', type=str, help='''
        The base path on the remote where the content will be uploaded.
        ''')

    parser.add_argument('--username', type=str,
                        help='the username for logging in on the remote')

    parser.add_argument(
        '--compress', action='store_true',
        help='Compress target folder or file before transmission.')

    parser.add_argument(
        '--version', action='store_true',
        help='Print the version number.')

    args = parser.parse_args(args)

    try:
        asyncio.get_event_loop().run_until_complete(shuft.upload(args))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))


if __name__ == "__main__":
    cli(sys.argv[1:])
