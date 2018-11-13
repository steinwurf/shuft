#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil
import sys


def connect_sftp(func):

    async def wrap(host,port, known_hosts, username, password, client_keys,
                   **kwargs):

        try:
            async with asyncssh.connect(host,
                                        port=port,
                                        known_hosts=known_hosts,
                                        username=username,
                                        password=password,
                                        client_keys=client_keys,
                                        ) as conn:

                try:
                    async with conn.start_sftp_client() as sftp:

                        await func(sftp, **kwargs)

                except (OSError, asyncssh.Error) as exc:
                    sys.exit('Failed to start sftp client: ' + str(exc))

        except (OSError, asyncssh.Error) as exc:
            sys.exit('Faield to establish connection: ' + str(exc))

    return wrap


@connect_sftp
async def upload(sftp, localpath, remotepath, compress, **kwargs):

    if not await sftp.exists(remotepath):
        try:
            await sftp.mkdir(remotepath)
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Failed to create remote dir: ' + str(exc))

    if compress:
        localpath = shutil.make_archive('upload',
                                        'gztar',
                                        root_dir=localpath,
                                        )
    try:
        await sftp.put(localpath,
                       preserve=True,
                       recurse=True,
                       remotepath=remotepath)
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Failed to upload: ' + str(exc))

    if compress:
        archieve = os.path.basename(localpath)

        try:
            await conn.run('tar -xf ' +
                           os.path.join(remotepath, archieve) +
                           ' -C ' + remotepath, check=True)
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Executing remote command failed: ' + str(exc))

        try:
            await sftp.remove(os.path.join(remotepath, archieve))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Removing remote file failed: ' + str(exc))

        os.remove(localpath)
