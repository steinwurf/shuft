#! /usr/bin/env python3
# encoding: utf-8

import asyncssh
import os
import shutil
import sys


def connect_sftp(func):

    async def wrap(host, port, known_hosts, username, password, client_keys,
                   **kwargs):

        try:
            async with asyncssh.connect(host,
                                        port=port,
                                        known_hosts=known_hosts,
                                        username=username,
                                        password=password,
                                        client_keys=client_keys,
                                        ) as connection:

                try:
                    async with connection.start_sftp_client() as sftp:
                        try:
                            await func(connection, sftp, **kwargs)
                        except (OSError, asyncssh.Error) as exc:
                            sys.exit('Failed to run command: ' + str(exc))

                except (OSError, asyncssh.Error) as exc:
                    sys.exit('Failed to start sftp client: ' + str(exc))

        except (OSError, asyncssh.Error) as exc:
            sys.exit('Faield to establish connection: ' + str(exc))

    return wrap


@connect_sftp
async def upload(connection, sftp, localpath, remotepath, compress, **kwargs):

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
            await connection.run(
                'tar -xf ' + os.path.join(remotepath, archieve) +
                ' -C ' + remotepath, check=True)
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Failed to unpack archieve on host: ' + str(exc))

        os.remove(localpath)

        try:
            await sftp.remove(os.path.join(remotepath, archieve))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Removing remote file failed: ' + str(exc))


@connect_sftp
async def download(connection, sftp, localpath, remotepath, compress, **kwargs):

    try:
        await sftp.exists(remotepath)
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Remotepath does not exists: ' + str(exc))

    os.makedirs(localpath, exist_ok=True)

    if compress:
        try:
            await connection.run(
                'tar -C ' + remotepath + ' -czf archive.tar .', check=True)
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Failed to compress download target on host: ' + str(exc))

        remotepath = 'archive.tar'
        localpath = os.path.join(localpath, 'archive.tar')

    try:
        await sftp.get(remotepath,
                       preserve=True,
                       recurse=True,
                       localpath=localpath,
                       )
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Failed to download: ' + str(exc))

    if compress:
        shutil.unpack_archive(localpath,
                              extract_dir=os.path.dirname(localpath),
                              )

        os.remove(localpath)

        try:
            await sftp.remove(remotepath)
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Removing remote file failed: ' + str(exc))
