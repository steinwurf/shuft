#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil
import sys


async def upload(host, localpath, remotepath, compress, **kwargs):
    """Compress, upload, remote uncompress and remove archieves."""

    connect_args = {k:v for k,v in kwargs.items() if k in
        ['port', 'known_hosts', 'username', 'password', 'client_keys' ]}

    async with asyncssh.connect(host, **connect_args) as conn:
        async with conn.start_sftp_client() as sftp:

            if not await sftp.exists(remotepath):
                await sftp.mkdir(remotepath)

            if compress:
                localpath = shutil.make_archive('upload',
                                                'gztar',
                                                base_dir=localpath)

            await sftp.put(localpath,
                           preserve=True,
                           recurse=True,
                           remotepath=remotepath)

            if compress:
                await conn.run('tar -xf ' +
                               os.path.join(remotepath, localpath) +
                               ' -C ' + remotepath, check=True)

                await sftp.remove(os.path.join(remotepath, localpath))
                os.remove(localpath)
