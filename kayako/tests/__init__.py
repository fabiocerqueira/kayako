# -*- coding: utf-8 -*-
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
