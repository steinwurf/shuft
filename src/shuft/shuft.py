#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil


async def upload(localpath, hostname, remotepath, username):
    """Upload files and folders."""
    async with asyncssh.connect(host=hostname, username=username) as conn:
        async with conn.start_sftp_client() as sftp:
            await sftp.put(localpath, remotepath=remotepath, preserve=True, recurse=True)

async def upload_compressed(localpath, hostname, remotepath, username):
    """Compress, upload, remote uncompress and remove archieves."""
    async with asyncssh.connect(host=hostname, username=username) as conn:
        async with conn.start_sftp_client() as sftp:

            archieve = shutil.make_archive('upload', 'gztar', base_dir=localpath)
            await sftp.put(archieve, remotepath=remotepath, preserve=True)
            await conn.run('tar -xf ' + os.path.join(remotepath,archieve) +
                           ' -C ' + remotepath, check=True)

            await sftp.remove(os.path.join(remotepath,archieve))
            os.remove(archieve)
