#! /usr/bin/env python
# encoding: utf-8

import os
import waflib

def options(opt):

    opt.add_option(
        '--run_tests', default=False, action='store_true',
        help='Run all unit tests')

def configure(conf):
    pass


def build(bld):

    # Create a virtualenv in the source folder and build universal wheel
    # Make sure the virtualenv Python module is in path
    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:
        venv.pip_install(packages=['wheel', 'setuptools_scm'])

    if not bld.options.run_tests:
        venv.run(cmd='python setup.py bdist_wheel --universal', cwd=bld.path)

    # Run the unit-tests
    if bld.options.run_tests:
        venv.pip_install(packages=[
            'pytest', 'pytest-testdirectory', 'cryptography'])
        venv.run(cmd='python setup.py pytest', cwd=bld.path)
