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
import sys
import unittest

LOG_NAME = 'kayako_test'
log = logging.getLogger(LOG_NAME)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s KAYAKO-TEST  %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

log = logging.getLogger('kayako')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)-15s KAYAKO-%(levelname)-5s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

class KayakoTest(unittest.TestCase):

    def log(self, *args, **kwargs):
        log = logging.getLogger(LOG_NAME)
        log.debug(*args, **kwargs)
        sys.stderr.flush()



class KayakoAPITest(KayakoTest):

    API_URL = ''
    API_KEY = ''
    SECRET_KEY = ''

    @property
    def api(self):
        from kayako.api import KayakoAPI
        return KayakoAPI(self.API_URL, self.API_KEY, self.SECRET_KEY)
