#! /usr/bin/env python
# encoding: utf-8

import shuft

import subprocess

import asyncio

def test_version():

    assert(shuft.__version__)

def test_cli():

    # start local server
    # python -m pyftpdlib -i localhost --port 2122 -w -u TEST -P PASSS

    subprocess.Popen(['python', '-m pyftpdlib', '-i localhost', '-w', '-u TEST', '-P PASSS'])





    # shuft.cli(['foo','localhost','', '--username', 'TEST', '--password', 'PASSS', '--port', '2121'])
    # assert(True)

    try:
        asyncio.get_event_loop().run_until_complete(
            shuft.cli(['foo', 'localhost', '', '--username', 'TEST', '--password', 'PASSS', '--port', '2121']))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))
