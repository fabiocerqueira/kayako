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

    API_URL = 'https://support.employeerewards.com/api/index.php'
    API_KEY = 'a7f9507e-6538-99c4-29e3-852614ce3385'
    SECRET_KEY = 'NjAxYWMyZGUtMmYzNy1kYjA0LWM1NDktMWU4Yzg3MzdjYWFlODFiYjMxNmMtZmViZS1iMWM0LTY5NmYtNzE0YmQzMGMyNmRk'

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI(self.API_URL, self.API_KEY, self.SECRET_KEY)
