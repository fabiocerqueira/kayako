# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the GNU General Public License (GPL)
#-----------------------------------------------------------------------------
'''
Created on May 5, 2011

@author: evan
'''

import unittest

# TODO: Local testing

class KayakoAPITest(unittest.TestCase):

    SECRET_KEY = ''
    API_KEY = ''
    API_URL = ''

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI(self.API_URL, self.API_KEY, self.SECRET_KEY)
