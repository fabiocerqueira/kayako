# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 5, 2011

@author: evan
'''

import unittest

class TestKayakoObject(unittest.TestCase):

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI('url', 'key', 'secret')

    @property
    def kayako_object(self):
        from kayako.core.object import KayakoObject
        return KayakoObject(self.api)

    def test_kayako_object(self):
        self.assert_(self.kayako_object)

    def test_kayko_get(self):
        from kayako.exception import KayakoMethodNotImplementedError
        self.assertRaises(KayakoMethodNotImplementedError, self.kayako_object.get, self.api, 123)

    def test_kayko_add(self):
        from kayako.exception import KayakoMethodNotImplementedError
        self.assertRaises(KayakoMethodNotImplementedError, self.kayako_object.add)

    def test_kayko_save(self):
        from kayako.exception import KayakoMethodNotImplementedError
        self.assertRaises(KayakoMethodNotImplementedError, self.kayako_object.save)

    def test_kayko_delete(self):
        from kayako.exception import KayakoMethodNotImplementedError
        self.assertRaises(KayakoMethodNotImplementedError, self.kayako_object.delete)
