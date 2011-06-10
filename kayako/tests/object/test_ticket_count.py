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

from kayako.tests import KayakoAPITest

class TestTicketCount(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import TicketCount

        api = self.api

        count = api.get_all(TicketCount)

        assert isinstance(count.departments, tuple)
        assert isinstance(count.statuses, tuple)
        assert isinstance(count.staff, tuple)
        assert isinstance(count.unassigned, tuple)
