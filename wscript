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
    with bld.create_virtualenv(cwd=bld.bldnode.abspath()) as venv:
        venv.pip_install(packages=['wheel', 'setuptools_scm'])

    # Build an universal wheeel and a source package
    venv.run(cmd='python setup.py sdist', cwd=bld.path)
    venv.run(cmd='python setup.py bdist_wheel --universal', cwd=bld.path)

    # Run the unit-tests
    if bld.options.run_tests:
        venv.pip_install(packages=[
            'pytest', 'pytest-testdirectory', 'cryptography'])
        venv.run(cmd='python setup.py pytest', cwd=bld.path)
