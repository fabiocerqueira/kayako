# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 10, 2011

@author: evan
'''

import unittest

class TestNodeParser(unittest.TestCase):

    def _etree_with_data(self, data):
        from lxml import etree
        return etree.fromstring('<data>%s</data>' % data)

    def test__parse_int_required(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._parse_int('123', required=True) == 123
        self.assertRaises(TypeError, NodeParser._parse_int, None, required=True)
        self.assertRaises(ValueError, NodeParser._parse_int, '', required=True)
        self.assertRaises(ValueError, NodeParser._parse_int, 'abc', required=True)

    def test__parse_int_optional(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._parse_int('123', required=False, strict=False) == 123
        assert NodeParser._parse_int(None, required=False, strict=False) == None
        assert NodeParser._parse_int('', required=False, strict=False) == None
        assert NodeParser._parse_int('abc', required=False, strict=False) == None

    def test__parse_int_strict(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._parse_int('123', required=False, strict=True) == 123
        assert NodeParser._parse_int(None, required=False, strict=True) == None
        assert NodeParser._parse_int('', required=False, strict=True) == None
        self.assertRaises(ValueError, NodeParser._parse_int, 'abc', required=False, strict=True)

    def test__get_int_required(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_int(self._etree_with_data('123'), required=True) == 123
        self.assertRaises(AttributeError, NodeParser._get_int, None, required=True)
        self.assertRaises(TypeError, NodeParser._get_int, self._etree_with_data(''), required=True)
        self.assertRaises(ValueError, NodeParser._get_int, self._etree_with_data('abc'), required=True)

    def test__get_int_optional(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_int(self._etree_with_data('123'), required=False, strict=False) == 123
        assert NodeParser._get_int(None, required=False, strict=False) == None
        assert NodeParser._get_int(self._etree_with_data(''), required=False, strict=False) == None
        assert NodeParser._get_int(self._etree_with_data('abc'), required=False, strict=False) == None

    def test__get_int_strict(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_int(self._etree_with_data('123'), required=False, strict=True) == 123
        assert NodeParser._get_int(None, required=False, strict=True) == None
        assert NodeParser._get_int(self._etree_with_data(''), required=False, strict=True) == None
        self.assertRaises(ValueError, NodeParser._get_int, self._etree_with_data('abc'), required=False, strict=True)

    def test__get_string(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_string(self._etree_with_data('123')) == '123'
        assert NodeParser._get_string(None) == None
        assert NodeParser._get_string(self._etree_with_data('')) == None

    def test__get_boolean_required(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_boolean(self._etree_with_data('1'), required=True) == True
        assert NodeParser._get_boolean(self._etree_with_data('0'), required=True) == False
        self.assertRaises(AttributeError, NodeParser._get_boolean, None, required=True)
        self.assertRaises(TypeError, NodeParser._get_boolean, self._etree_with_data(''), required=True)
        self.assertRaises(ValueError, NodeParser._get_boolean, self._etree_with_data('abc'), required=True)

    def test__get_boolean_optional(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_boolean(self._etree_with_data('1'), required=False, strict=False) == True
        assert NodeParser._get_boolean(self._etree_with_data('0'), required=False, strict=False) == False
        assert NodeParser._get_boolean(None, required=False, strict=False) == None
        assert NodeParser._get_boolean(self._etree_with_data(''), required=False, strict=False) == None
        assert NodeParser._get_boolean(self._etree_with_data('abc'), required=False, strict=False) == None
        assert NodeParser._get_boolean(self._etree_with_data('2'), required=False, strict=False) == True

    def test__get_boolean_strict(self):
        from kayako.core.lib import NodeParser

        assert NodeParser._get_boolean(self._etree_with_data('1'), required=False, strict=True) == True
        assert NodeParser._get_boolean(self._etree_with_data('0'), required=False, strict=True) == False
        assert NodeParser._get_boolean(None, required=False, strict=True) == None
        assert NodeParser._get_boolean(self._etree_with_data(''), required=False, strict=True) == None
        self.assertRaises(ValueError, NodeParser._get_boolean, self._etree_with_data('abc'), required=False, strict=True)
        self.assertRaises(ValueError, NodeParser._get_boolean, self._etree_with_data('2'), required=False, strict=True)

    def test__get_date_required(self):
        import time
        from datetime import datetime
        from kayako.core.lib import NodeParser, FOREVER

        timestamp = int(time.mktime(datetime.now().timetuple()))
        now = datetime.fromtimestamp(timestamp)

        assert NodeParser._get_date(self._etree_with_data(timestamp), required=True) == now
        assert NodeParser._get_date(self._etree_with_data('0'), required=True) == FOREVER
        self.assertRaises(AttributeError, NodeParser._get_date, None, required=True)
        self.assertRaises(TypeError, NodeParser._get_date, self._etree_with_data(''), required=True)
        self.assertRaises(ValueError, NodeParser._get_date, self._etree_with_data('abc'), required=True)

    def test__get_date_optional(self):
        import time
        from datetime import datetime
        from kayako.core.lib import NodeParser, FOREVER

        timestamp = int(time.mktime(datetime.now().timetuple()))
        now = datetime.fromtimestamp(timestamp)

        assert NodeParser._get_date(self._etree_with_data(timestamp), required=False, strict=False) == now
        assert NodeParser._get_date(self._etree_with_data('0'), required=True) == FOREVER
        assert NodeParser._get_date(None, required=False, strict=False) == None
        assert NodeParser._get_date(self._etree_with_data(''), required=False, strict=False) == None
        assert NodeParser._get_date(self._etree_with_data('abc'), required=False, strict=False) == None

    def test__get_date_strict(self):
        import time
        from datetime import datetime
        from kayako.core.lib import NodeParser, FOREVER

        timestamp = int(time.mktime(datetime.now().timetuple()))
        now = datetime.fromtimestamp(timestamp)

        assert NodeParser._get_date(self._etree_with_data(timestamp), required=False, strict=True) == now
        assert NodeParser._get_date(self._etree_with_data('0'), required=True) == FOREVER
        assert NodeParser._get_date(None, required=False, strict=True) == None
        assert NodeParser._get_date(self._etree_with_data(''), required=False, strict=True) == None
        self.assertRaises(ValueError, NodeParser._get_date, self._etree_with_data('abc'), required=False, strict=True)




