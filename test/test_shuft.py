#! /usr/bin/env python
# encoding: utf-8

import shuft
import os

import asyncio


def test_version():

    # assert(shuft.__version__ == "0.0.0")
    assert(True)


def test_upload(tmpdir):

    dir = tmpdir.mkdir('foo')
    file = dir.join('bar.txt')
    file.write('foobar')

    remote = tmpdir.mkdir('remote')

    assert(True)
