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

import logging
import unittest

# TODO: Local testing

class KayakoTest(unittest.TestCase):

    LOG_NAME = 'kayako_test'

    def log(self, *args, **kwargs):
        log = logging.getLogger(KayakoTest.LOG_NAME)
        log.debug(*args, **kwargs)

    def setUp(self, *args, **kwargs):
        log = logging.getLogger(KayakoTest.LOG_NAME)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s KAYAKO-TEST  %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

        unittest.TestCase.setUp(self, *args, **kwargs)


class KayakoAPITest(KayakoTest):

    API_URL = 'https://support.employeerewards.com/api/index.php'
    API_KEY = ''
    SECRET_KEY = ''

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI(self.API_URL, self.API_KEY, self.SECRET_KEY)

    def setUp(self, *args, **kwargs):

        log = logging.getLogger('kayako')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)-15s KAYAKO-%(levelname)-5s %(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

        return KayakoTest.setUp(self, *args, **kwargs)
