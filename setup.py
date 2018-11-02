#! /usr/bin/env python
# encoding: utf-8

import io
import sys

from setuptools import setup, find_packages

with io.open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

if sys.version_info < (3, 5):
    raise RuntimeError("Requires Python 3.5+")

setup(
    name='shuft',
    use_scm_version=True,
    description=("Tool for uploading folders and files via sftp."),
    long_description=long_description,
    url='https://github.com/steinwurf/shuft',
    author='Steinwurf ApS',
    author_email='contact@steinwurf.com',
    license='BSD 3-clause "New" or "Revised" License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': ['shuft=shuft.__main__:run'],
    },
    keywords=('sftp'),
    packages=find_packages(where='src', exclude=['test']),
    package_dir={"": "src"},
    setup_requires=["setuptools_scm", "pytest-runner", ],
    install_requires=['asyncssh', ],
    tests_require=['pytest', 'pytest-testdirectory', 'cryptography', ],
)
