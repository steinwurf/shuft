#! /usr/bin/env python
# encoding: utf-8

import io

from setuptools import setup, find_packages

with io.open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='shuft',
    use_scm_version=True,
    description=("Tool for uploading folders and files via sftp."),
    long_description=long_description,
    url='https://github.com/steinwurf/',
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
        'Programming Language :: Python',
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
