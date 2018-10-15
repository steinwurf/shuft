#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil


async def upload(args):
    """Compress, upload, remote uncompress and remove archieves."""
    async with asyncssh.connect(args.host, username=args.username) as conn:
        async with conn.start_sftp_client() as sftp:

            if not args.compress:
                await sftp.put(localpath, remotepath=args.remotepath,
                                preserve=True, recurse=True)
                return

            archieve = shutil.make_archive(
                'upload', 'gztar', base_dir=args.localpath)

            await sftp.put(archieve, remotepath=args.emotepath, preserve=True)

            await conn.run('tar -xf ' + os.path.join(args.remotepath,archieve) +
                           ' -C ' + args.remotepath, check=True)

            await sftp.remove(os.path.join(args.remotepath,archieve))
            os.remove(archieve)
