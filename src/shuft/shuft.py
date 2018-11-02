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

    try:
        async with asyncssh.connect(host, **connect_args) as conn:

            try:
                async with conn.start_sftp_client() as sftp:

                    if not await sftp.exists(remotepath):
                        try:
                            await sftp.mkdir(remotepath)
                        except (OSError, asyncssh.Error) as exc:
                            sys.exit('Failed to create remote dir: ' + str(exc))

                    if compress:
                        localpath = shutil.make_archive('upload',
                                                        'gztar',
                                                        base_dir=localpath)

                    try:
                        await sftp.put(localpath,
                                       preserve=True,
                                       recurse=True,
                                       remotepath=remotepath)
                    except (OSError, asyncssh.Error) as exc:
                        sys.exit('Failed to upload: ' + str(exc))

                    if compress:
                        try:
                            await conn.run('tar -xf ' +
                                           os.path.join(remotepath, localpath) +
                                           ' -C ' + remotepath, check=True)
                        except (OSError, asyncssh.Error) as exc:
                            sys.exit('Executing remote command failed: ' + str(exc))

                        try:
                            await sftp.remove(os.path.join(remotepath, localpath))
                        except (OSError, asyncssh.Error) as exc:
                            sys.exit('Removing remote file failed: ' + str(exc))

                        os.remove(localpath)

            except (OSError, asyncssh.Error) as exc:
                sys.exit('Failed to start sftp client: ' + str(exc))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('Connection to host failed: ' + str(exc))
