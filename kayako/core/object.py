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
from kayako.core.lib import ParameterObject, NodeParser, UnsetParameter
from kayako.exception import KayakoMethodNotImplementedError, KayakoRequestError, KayakoResponseError

class KayakoRequestParser(NodeParser):
    ''' 
    Overrides NodeParser methods to raise KayakoResponseErrors instead of 
    ValueError, AttributeError, and TypeError when parsing nodes/data.
    '''

    @staticmethod
    def _parse_int(data, required=True, strict=True):
        try:
            return NodeParser._parse_int(data, required=required, strict=strict)
        except Exception, error:
            raise KayakoResponseError('There was an error parsing the response (_parse_int(%s, required=%s, strict=%s):\n\t%s' % (data, required, strict, error))

    @staticmethod
    def _parse_date(data, required=True, strict=True):
        try:
            return NodeParser._parse_date(data, required=required, strict=strict)
        except Exception, error:
            raise KayakoResponseError('There was an error parsing the response (_parse_date(%s, required=%s, strict=%s):\n\t%s' % (data, required, strict, error))

    @staticmethod
    def _get_int(node, required=True, strict=True):
        try:
            return NodeParser._get_int(node, required=required, strict=strict)
        except Exception, error:
            raise KayakoResponseError('There was an error parsing the response (_get_int(%s, required=%s, strict=%s):\n\t%s' % (node, required, strict, error))

    @staticmethod
    def _get_boolean(node, required=True, strict=True):
        try:
            return NodeParser._get_boolean(node, required=required, strict=strict)
        except Exception, error:
            raise KayakoResponseError('There was an error parsing the response (_get_boolean(%s, required=%s, strict=%s):\n\t%s' % (node, required, strict, error))

    @staticmethod
    def _get_date(node, required=True, strict=True):
        try:
            return NodeParser._get_date(node, required=required, strict=strict)
        except Exception, error:
            raise KayakoResponseError('There was an error parsing the response (_get_date(%s, required=%s, strict=%s):\n\t%s' % (node, required, strict, error))

    def __str__(self):
        return '<KayakoRequestParser at %s>' % (hex(id(self)))

class KayakoObject(ParameterObject, KayakoRequestParser):
    ''' Kayako Object class meant to built from a factory. '''

    id = UnsetParameter
    api = None
    controller = None

    def __init__(self, api, **parameters):
        ParameterObject.__init__(self, **parameters)
        self.api = api

    ## Persistence Layer

    @classmethod
    def get_all(cls, api, *args, **kwargs):
        ''' Get all instances of this object from Kayako. '''
        raise KayakoMethodNotImplementedError('GET ALL %s is not implemented for this object.' % cls.__name__)

    @classmethod
    def get(cls, api, id):
        ''' Get an instance of this object by ID '''
        raise KayakoMethodNotImplementedError('GET %s not implemented (id:%s)' % (cls.__name__, id))

    def _add(self, controller, *required_parameters):
        '''
        Refactored method to check required parameters before adding. Also checks
        that 'id,' if present, is an UnsetParameter.
        Returns the response returned by the API call.
        '''
        parameters = self.request_parameters
        if 'id' in parameters:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))
        for required_parameter in required_parameters:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))
        return self.api._request(controller, 'POST', **parameters)

    def add(self):
        ''' Add a new object to Kayako '''
        raise KayakoMethodNotImplementedError('POST %s not implemented' % (self.__class__.__name__))

    def _save(self, controller, *required_parameters):
        '''
        Refactored method to check required parameters before saving. Also checks
        that 'id,' if present, is an UnsetParameter.
        Returns the response returned by the API call.
        '''
        parameters = self.request_parameters
        if 'id' not in parameters:
            raise KayakoRequestError('Cannot save a non-existent %s. Use add instead.' % self.__class__.__name__)
        for required_parameter in required_parameters:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot save %s: Missing required field: %s. (id: %s)' % (self.__class__.__name__, required_parameter, self.id))
        return self.api._request(controller, 'PUT', **parameters)

    def save(self):
        ''' Save an existing object to Kayako '''
        raise KayakoMethodNotImplementedError('PUT %s not implemented' % (self.__class__.__name__))

    def _delete(self, controller):
        '''
        Refactored method to delete an object from Kayako.
        '''
        if self.id is UnsetParameter:
            raise KayakoRequestError('Cannot delete a non-existent %s. The ID of the %s to delete has not been specified.' % (self.__class__.__name__, self.__class__.__name__))
        self.api._request(controller, 'DELETE')
        self.id = UnsetParameter

    def delete(self):
        ''' Delete an object from Kayako '''
        raise KayakoMethodNotImplementedError('DELETE %s not implemented' % (self.__class__.__name__))

    def __str__(self):
        return '<%s at %s>' % (self.__class__.__name__, hex(id(self)))

    def __repr__(self):
        if self.__request_parameters__:
            params = self.__request_parameters__[:]
        else:
            params = []
        if self.__response_parameters__:
            params.extend(self.__response_parameters__)
        all_parameters = self._parameters_from_list(set(params))
        return '%s(%s, **%s)' % (self.__class__.__name__, self.api, all_parameters)

