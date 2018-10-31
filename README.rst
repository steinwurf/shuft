Shuft
=====

A small command line tool for uploading and downloading files and folders to and from a sftp server.
Uses asyncssh and is pip installable for easy use in automated tasks.

.. image:: https://img.shields.io/travis-ci/steinwurf/shuft/master.svg?style=flat-square&logo=travis
    :target: https://travis-ci.org/steinwurf/shuft


* Upload a file or folder to a sftp server.
* Requires Python 3.5 or newer.


Getting started
---------------

In your virtual python environment of choice, install the shuft pip package.

.. code-block::

    python pip install shuft

Basic usage.

.. code-block::

    python shuft --command upload --host files.mydomain.com --localpath my_folder --remotepath /uploads/



Run with ''--help' for addtional options.

.. code-block::

    shuft --help

    usage: __main__.py [-h] --command {upload} --host HOST [--localpath LOCALPATH]
                       [--remotepath REMOTEPATH] [--port PORT]
                       [--known_hosts KNOWN_HOSTS] [--username USERNAME]
                       [--password PASSWORD] [--client_keys CLIENT_KEYS]
                       [--compress]

    Upload directories or files

    optional arguments:
      -h, --help            show this help message and exit
      --command {upload}    the task to perform.
      --host HOST           the remote host to connect to.
      --localpath LOCALPATH
                            path to the local folder or file.
      --remotepath REMOTEPATH
                            path to the remote folder or file.
      --port PORT           port number on the remote (defaults to 22).
      --known_hosts KNOWN_HOSTS
                            list of known hosts, if set to None accepts any.
      --username USERNAME   username for logging in on the remote, defaults to the
                            current user
      --password PASSWORD   password for logging in on the remote
      --client_keys CLIENT_KEYS
                            list of client private key(s)
      --compress            whether to compress target folder or file before
                            transmission. Requires that the host accepts ssh
                            connections and has tar available
