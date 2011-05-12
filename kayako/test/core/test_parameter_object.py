# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 9, 2011

@author: evan
'''

import unittest

class TestParameterObject(unittest.TestCase):

    def test_parameters(self):
        from kayako.core.lib import ParameterObject, UnsetParameter

        class obj(ParameterObject):
            __request_parameters__ = ['prop1', 'prop2']
            __response_parameters__ = ['resp1']

        o = obj(prop1='new')

        assert hasattr(o, 'prop1')
        assert hasattr(o, 'prop2')
        assert o.prop1 == 'new'
        assert o.prop2 == UnsetParameter
        assert not o.prop2

        o.resp1 = 'test'

        params = o.request_parameters
        assert 'prop1' in params
        assert 'prop2' not in params
        assert 'resp1' not in params
        respparams = o.response_parameters
        assert 'prop1' not in respparams
        assert 'prop2' not in respparams
        assert respparams['resp1'] == 'test'
        assert len(params) == 1

    def test_multiple_objects_can_have_different_values(self):
        from kayako.core.lib import ParameterObject

        class obj(ParameterObject):
            __request_parameters__ = ['prop1', 'prop2']

        obj1 = obj(prop1='old')
        obj2 = obj(prop1='new')

        assert obj1.prop1 != obj2.prop1

    def test_invalid_parameter(self):
        from kayako.core.lib import ParameterObject

        class obj(ParameterObject):
            __request_parameters__ = ['prop1', 'prop2']

        self.assertRaises(TypeError, obj, prop3='fake')
