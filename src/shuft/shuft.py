import os
import shutil
import sys
import asyncio

import asyncssh


async def upload(localpath, hostname, remotepath, username):
    """Upload files and folders."""
    async with asyncssh.connect(host=hostname, username=username) as conn:
        async with conn.start_sftp_client() as sftp:
            await sftp.put(localpath, remotepath=remotepath, preserve=True, recurse=True)

async def upload_compressed(localpath, hostname, remotepath, username):
    """Compress, upload, remote uncompress and remove archieves."""
    async with asyncssh.connect(host=hostname, username=username) as conn:
        async with conn.start_sftp_client() as sftp:

            archieve = shutil.make_archive('upload', 'tar', base_dir=localpath)
            await sftp.put(archieve, remotepath=remotepath, preserve=True)
            await conn.run('tar -xf ' + os.path.join(remotepath,archieve) +
                           ' -C ' + remotepath, check=True)

            await sftp.remove(os.path.join(remotepath,archieve))
            os.remove(archieve)

def run(args):
    upload_command = upload

    if args.compress:
        upload_command = upload_compressed

    try:
        asyncio.get_event_loop().run_until_complete(upload_command(
            args.localpath,
            args.hostname,
            args.remotepath,
            args.username))

    except (OSError, asyncssh.Error) as exc:
        sys.exit('SFTP operation failed: ' + str(exc))
