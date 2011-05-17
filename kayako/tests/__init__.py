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

# TODO: Local testing

class KayakoAPITest(unittest.TestCase):

    API_URL = ''
    API_KEY = ''
    SECRET_KEY = ''

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI(self.API_URL, self.API_KEY, self.SECRET_KEY)
