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

    @property
    def read(self):
        '''
        Returns the read function of the first readable argument in this
        exception.
        '''
        if self.args:
            for arg in self.args:
                if hasattr(arg, 'read'):
                    if callable(arg.read):
                        return arg.read
                    else:
                        return lambda: arg.read


class KayakoInitializationError(KayakoError):
    pass

# COMM ERRORS

class KayakoIOError(KayakoError):
    pass

# REQUEST ERRORS

class KayakoRequestError(KayakoIOError):
    pass

class KayakoMethodNotImplementedError(KayakoRequestError):
    '''
    An exception for when an HTTP request method is not implemented for an
    object.
    '''
    pass

# RESPONSE ERROR

class KayakoResponseError(KayakoIOError):
    pass
