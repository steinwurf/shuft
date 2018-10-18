#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil
import sys


async def upload(host, localpath, compress, **kwargs):
    """Compress, upload, remote uncompress and remove archieves."""

    connect_args = {k:v for k,v in kwargs.items() if k in
        ['port', 'known_hosts', 'username', 'password', ]}

    put_args = {k:v for k,v in kwargs.items() if k in ['remotepath', ]}

    async with asyncssh.connect(host, **connect_args) as conn:
        async with conn.start_sftp_client() as sftp:
            if compress is False:
                await sftp.put(localpath2,
                               preserve=True,
                               recurse=True,
                               **put_args)
                return

            archieve = shutil.make_archive('upload', 'gztar', base_dir=localpath)
            await sftp.put(archieve, preserve=True, **put_args)

            await conn.run('tar -xf ' +
                           os.path.join(kwargs['remotepath'],archieve) +
                           ' -C ' + kwargs['remotepath'], check=True)

            await sftp.remove(os.path.join(kwargs['remotepath'],archieve))
            os.remove(archieve)
