#! /usr/bin/env python3
# encoding: utf-8

import argparse
import asyncio
import asyncssh
import sys

import shuft


commands = {'upload': shuft.upload}

def cli():
    """Command line."""
    parser = argparse.ArgumentParser(description='''
        Upload directories or files
        ''')

    args = sys.argv[1:]

    parser.add_argument('--command', choices=['upload'], required=True,
        help='the task to perform.')

    parser.add_argument('--host', type=str, required=True,
        help='the remote host to connect to.')

    parser.add_argument('--localpath', type=str, default="",
        help='path to the local folder or file.')

    parser.add_argument('--remotepath', type=str, default="",
        help='path to the remote folder or file.')

    parser.add_argument('--port', type=int, default=22,
        help='port number on the remote (defaults to 22).')

    parser.add_argument('--known_hosts', type=str, default=(),
        help='list of known hosts, if set to None accepts any.')

    parser.add_argument('--username', type=str, default=None,
        help='username for logging in on the remote, defaults to the current user')

    parser.add_argument('--password', type=str, default=None,
        help='password for logging in on the remote')

    parser.add_argument('--client_keys', type=list, default=(),
        help='list of client private key(s)')

    parser.add_argument('--compress', action='store_true', help='''
        whether to compress target folder or file before transmission.
        Requires that the host accepts ssh connections and has tar available''')

    args = parser.parse_args(args)

    if args.known_hosts == 'None':
        args.known_hosts = None

    return args


def run():

    if sys.version_info[0] < 3.5:
        raise Exception("Must be using Python 3.5 or newer")

    args = cli()

    try:
        asyncio.get_event_loop().run_until_complete(run_command(**vars(args)))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))

async def run_command(command, **kwargs):

    await commands[command](**kwargs)

if __name__ == "__main__":

    run()
