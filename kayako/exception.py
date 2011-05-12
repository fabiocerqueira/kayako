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
