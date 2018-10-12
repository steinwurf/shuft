#! /usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

from pkg_resources import get_distribution

from shuft.shuft import upload
from shuft.shuft import upload_compressed

__version__ = get_distribution('shuft').version
