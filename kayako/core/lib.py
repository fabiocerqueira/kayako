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

from datetime import datetime

__all__ = [
    'UnsetParameter',
    'FOREVER',
    'ParameterObject',
    'NodeParser',
]

class _unsetparameter(object):

    def __nonzero__(self):
        return False

    def __call__(self):
        return self

    def __repr__(self):
        return 'UnsetParameter()'

    def __str__(self):
        return '??'

class _forever(object):

    def __int__(self):
        return 0

    def __repr__(self):
        return '0'

    def __str__(self):
        return '<Forever>'

UnsetParameter = _unsetparameter()
FOREVER = _forever()

class ParameterObject(object):
    '''
    An object used to build a dictionary around different parameter types.

    __request_parameters__ = []
        A list of parameters used to REQUEST an object (GET/POST/PUT/DELETE)

    __response_parameters__ = []
        A list of parameters used only when receiving object properties.
        
    request_parameters
        This objects dictionary of request_parameters containing only set
        parameters.
        
    response_parameters
        This objects dictionary of response_parameters containing only set
        parameters.
    '''

    __request_parameters__ = None
    ''' 
    A list of parameters used to REQUEST an object (GET/POST/PUT/DELETE)
    '''
    __response_parameters__ = None
    '''
    A list of parameters used only when receiving object properties.
    '''

    def __init__(self, **parameters):
        '''
        Creates this parameter object setting parameter values as given by
        keyword arguments.
        '''
        if self.__request_parameters__:
            unset_parameters = self.__request_parameters__[:]
        else:
            unset_parameters = []
        if self.__response_parameters__:
            unset_parameters.extend(self.__response_parameters__)
        all_parameters = set(unset_parameters)
        for parameter, value in parameters.iteritems():
            if parameter not in all_parameters:
                raise TypeError("'%s' is an invalid keyword argument for %s" % (parameter, self.__class__.__name__))
            else:
                setattr(self, parameter, value)
                unset_parameters.remove(parameter)
        for unset_parameter in unset_parameters:
            setattr(self, unset_parameter, UnsetParameter)

    def _parameters_from_list(self, list):
        '''
        Returns parameters based on a list.
        '''
        params = {}
        for parameter in list:
            attribute = getattr(self, parameter)
            if attribute is not UnsetParameter:
                params[parameter] = attribute
        return params

    @property
    def request_parameters(self):
        '''
        Return a dictionary of this objects request parameters.
        '''
        return self._parameters_from_list(self.__request_parameters__)

    @property
    def response_parameters(self):
        '''
        Return a dictionary of this objects response parameters.
        '''
        return self._parameters_from_list(self.__response_parameters__)

    def __str__(self):
        return '<ParamterObject at %s>' % (hex(id(self)))


class NodeParser(object):
    ''' Methods to parse text data from an lxml etree object. '''

    @staticmethod
    def _parse_int(data, required=True, strict=True):
        ''' Simply parses data as an int.
        If its required, invalid data will raise a ValueError or TypeError.
        If its not required, but is strict and there is data, invalid data will
        raise a ValueError.
        If it is not required and is not strict, invalid data returns None.
        '''
        if required:
            return int(data)
        else:
            if data:
                try:
                    return int(data)
                except ValueError:
                    if strict:
                        raise

    @staticmethod
    def _parse_date(data, required=True, strict=True):
        '''
        Return an integer, or FOREVER. See _parse_int for information on 
        required and strict.
        '''
        value = NodeParser._parse_int(data, required=required, strict=strict)
        if value is None:
            return None
        elif value == 0:
            return FOREVER
        else:
            return value

    @staticmethod
    def _get_int(node, required=True, strict=True):
        '''
        Pulls out an integer from the etree on the given node.
        If it is required, it will assume everything is present, otherwise the
        return value could be None.
        If strict is True, it will parse any available text as an integer, 
        raising ValueError if it does not parse.
        Otherwise, unparsable text is ignored.  Required implies Strict.
        '''
        if required:
            return int(node.text)
        else:
            if node is not None and node.text:
                try:
                    return int(node.text)
                except ValueError:
                    if strict:
                        raise

    @staticmethod
    def _get_string(node):
        '''
        Pulls out the text of a given node.  Returns None if missing.
        '''
        if node is not None:
            return node.text

    @staticmethod
    def _get_boolean(node, required=True, strict=True):
        '''
        Returns the boolean value of an integer node.  See _get_int for details
        about required and strict.
        '''
        value = NodeParser._get_int(node, required=required, strict=strict)
        if value is None:
            return None
        else:
            if not strict:
                return bool(value)
            else:
                if value == 0:
                    return False
                elif value == 1:
                    return True
                else:
                    raise ValueError('Value for node not 1 or 0')

    @staticmethod
    def _get_date(node, required=True, strict=True):
        '''
        Return an integer, or FOREVER.  See _get_int for details about required
        and strict.
        '''
        value = NodeParser._get_int(node, required=required, strict=strict)
        if value is None:
            return None
        elif value == 0:
            return FOREVER
        else:
            return datetime.fromtimestamp(value)

    def __str__(self):
        return '<NodeParser at %s>' % (hex(id(self)))
