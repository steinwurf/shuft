#! /usr/bin/env python
# encoding: utf-8

import asyncio
import asyncssh
import os
import sys

import subprocess

import shuft

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

def generate_ssh_keys(testdirectory):
    ''' Generate a public and a private key and dump them in the testdir'''

    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    testdirectory.write_binary('private_key', private_key)
    testdirectory.write_binary('public_key', public_key)

async def start_server(cwd, port):

    class DummyFTPServer(asyncssh.SFTPServer):
        def __init__(self, conn):
            root = cwd
            super().__init__(conn, chroot=root)


    async def handle_client(process):
        bc_proc = subprocess.Popen('bc', shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    await asyncssh.listen('', port=port,
                          server_host_keys=[os.path.join(cwd, 'private_key')],
                          authorized_client_keys=os.path.join(cwd, 'public_key'),
                          sftp_factory=DummyFTPServer,)

def test_version():

    assert(shuft.__version__)


def test_upload_file(testdirectory):

    generate_ssh_keys(testdirectory)

    client_dir = testdirectory.mkdir('client')
    client_dir.write_text('test_file', 'test contex', 'utf8')
    client_file_dir = os.path.join(client_dir.path(), 'test_file')

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server(testdirectory.path(), 2222))

        loop.run_until_complete(shuft.upload(
            host='localhost',
            command='put',
            localpath=client_file_dir,
            remotepath='',
            port=2222,
            known_hosts=None,
            compress=False,
            client_keys=[os.path.join(testdirectory.path(), 'private_key')]))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    assert testdirectory.contains_file('test_file')


def test_upload_file_new_dir(testdirectory):

    generate_ssh_keys(testdirectory)

    client_dir = testdirectory.mkdir('client')
    bar_dir = client_dir.mkdir('bar')
    bar_dir.write_text('test_file', 'test contex', 'utf8')

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server(testdirectory.path(), 2223))

        loop.run_until_complete(shuft.upload(
            host='localhost',
            command='put',
            localpath=bar_dir.path(),
            remotepath='foo/',
            port=2223,
            known_hosts=None,
            compress=False,
            client_keys=[os.path.join(testdirectory.path(), 'private_key')]))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    assert testdirectory.contains_dir('foo')
    assert testdirectory.contains_file('foo/bar/test_file')

def test_upload_directory(testdirectory):

    generate_ssh_keys(testdirectory)

    client_dir = testdirectory.mkdir('client')
    foo_dir = client_dir.mkdir('foo')
    bar_dir = foo_dir.mkdir('bar')
    bar_dir.write_text('test_file', 'test contex', 'utf8')

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server(testdirectory.path(), 2224))

        loop.run_until_complete(shuft.upload(
            host='localhost',
            command='put',
            localpath=foo_dir.path(),
            remotepath='',
            port=2224,
            known_hosts=None,
            compress=False,
            client_keys=[os.path.join(testdirectory.path(), 'private_key')]))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))

    assert testdirectory.contains_dir('foo')
    assert testdirectory.contains_dir('foo/bar')
    assert testdirectory.contains_file('foo/bar/test_file')
