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
from kayako.test import KayakoAPITest

class TestTicketPriority(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import TicketPriority
        result = self.api.get_all(TicketPriority)
        assert isinstance(result, list)

    def test_get(self):
        from kayako.objects import TicketPriority
        result = self.api.get(TicketPriority, 1)
        assert 'TicketPriority' in str(result)
        self.assertEqual(result.id, 1)

class TestTicketStatus(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import TicketStatus
        result = self.api.get_all(TicketStatus)
        assert isinstance(result, list)

    def test_get(self):
        from kayako.objects import TicketStatus
        result = self.api.get(TicketStatus, 1)
        assert 'TicketStatus' in str(result)
        self.assertEqual(result.id, 1)

class TestTicketType(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import TicketType
        result = self.api.get_all(TicketType)
        #print result
        assert isinstance(result, list)

    def test_get(self):
        from kayako.objects import TicketType
        result = self.api.get(TicketType, 1)
        assert 'TicketType' in str(result)
        self.assertEqual(result.id, 1)



