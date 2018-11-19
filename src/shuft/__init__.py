#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
from pkg_resources import get_distribution

from shuft.shuft import upload
from shuft.shuft import download

from shuft.__main__ import run_command

__version__ = get_distribution(__name__).version
