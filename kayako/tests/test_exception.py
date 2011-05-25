# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 17, 2011

@author: evan
'''

import unittest

class TestException(unittest.TestCase):

    def test_KayakoError(self):
        from kayako.exception import KayakoError
        error = KayakoError('fail')
        assert str(error)
