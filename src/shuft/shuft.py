import os
import shutil
import sys
import asyncio

import asyncssh


async def upload(localpath, remote, remotepath, username):
    """Upload files and folders."""
    async with asyncssh.connect(host=remote, username=username) as conn:
        async with conn.start_sftp_client() as sftp:
            await sftp.put(localpath, remotepath=remotepath, preserve=True, recurse=True)

async def upload_compressed(localpath, remote, remotepath, username):
    """Compress, upload, remote uncompress and remove archieves."""
    async with asyncssh.connect(host=remote, username=username) as conn:
        async with conn.start_sftp_client() as sftp:

            archieve = shutil.make_archive('upload', 'zip', base_dir=localpath)
            await sftp.put(archieve, remotepath=remotepath, preserve=True, recurse=True)
            await conn.run('unzip -o -q ' + remotepath + archieve +
                           ' -d ' + remotepath, check=True)

            await sftp.remove(remotepath + archieve)
            os.remove(archieve)

def run(args):
    upload_command = upload

    if args.zip:
        upload_command = upload_compressed

    try:
        asyncio.get_event_loop().run_until_complete(upload_command(
            args.localpath,
            args.remote,
            args.remotepath,
            args.username))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))
