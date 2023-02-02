# -*- coding: utf-8 -*-
#
# Copyright (C) DevCartel Co.,Ltd.
# Bangkok, Thailand
#
import sys
__version__ = '1.4.0'

if sys.version_info >= (3, 0):
    from pymt5.pymt5 import *
else:
    from pymt5 import *
