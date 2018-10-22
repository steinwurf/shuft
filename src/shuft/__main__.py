#! /usr/bin/env python3
# encoding: utf-8

import argparse
import asyncio
import asyncssh
import sys

import shuft


async def cli(args):
    """Command line."""
    parser = argparse.ArgumentParser(description='''
        Upload directories or files, e.g.
        "shuft local_dir files.server.com /tmp/remote_dir/ --username USER"'
        ''')

    parser.add_argument('--host', type=str, required=True,
        help='The name of the host for the remote.')

    parser.add_argument('--command', choices=['put'], required=True,
        help='The task to perform.')

    parser.add_argument('--localpath', type=str, default="",
        help='Path to the local folder or file.')

    parser.add_argument('--remotepath', type=str, default="",
        help='Path to the remote folder or file.')

    parser.add_argument('--port', type=int, default=22,
        help='The port number on the remote.')

    parser.add_argument('--known_hosts', type=str, default=(),
        help='List of known hosts, if set to None accept any.')

    parser.add_argument('--username', type=str, default=None,
        help='the username for logging in on the remote')

    parser.add_argument('--client_keys', type=list, default=(),
        help='List of client keys')

    parser.add_argument('--password', type=str, default=None,
        help='the password for logging in on the remote')

    parser.add_argument('--compress', action='store_true',
        help='Compress target folder or file before transmission.')

    args = parser.parse_args(args)

    if args.known_hosts == 'None':
        args.known_hosts = None

    await shuft.upload(**vars(args))


if __name__ == "__main__":

    try:
        asyncio.get_event_loop().run_until_complete(cli(sys.argv[1:]))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))
