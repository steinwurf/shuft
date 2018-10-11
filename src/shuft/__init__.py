#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

from setuptools_scm import get_version

from shuft.shuft import upload
from shuft.shuft import upload_compressed

__version__ = get_version()
