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

    def test_kayako_error_no_read(self):
        from kayako.exception import KayakoError
        error = KayakoError()
        assert error.read is None

    def test_kayako_error_read_function(self):
        from StringIO import StringIO
        from kayako.exception import KayakoError
        error = KayakoError(StringIO('abc'))
        assert error.read == 'abc'

    def test_kayako_error_read_attribute(self):
        from kayako.exception import KayakoError
        class Read(object):
            read = 'abc123'
        error = KayakoError(Read())
        assert error.read == 'abc123'


