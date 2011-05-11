# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''
Created on May 5, 2011

@author: evan
'''

class KayakoError(StandardError):
    pass

class KayakoInitializationError(KayakoError):
    pass

# REQUEST ERRORS

class KayakoRequestError(KayakoError):
    pass

class KayakoMethodNotImplementedError(KayakoRequestError):
    '''
    An exception for when an HTTP request method is not implemented for an
    object.
    '''
    pass

# RESPONSE ERROR

class KayakoResponseError(KayakoError):
    pass
