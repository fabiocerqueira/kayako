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

class TestTicketNote(KayakoAPITest):

    SUBJECT = 'DELETEME'

    def tearDown(self):
        from kayako.objects import Department, Ticket
        dept = self.api.first(Department, module='tickets')
        test_tickets = self.api.filter(Ticket, args=(dept.id,), subject=self.SUBJECT)
        for ticket in test_tickets:
            ticket.delete()
        super(TestTicketNote, self).tearDown()

    def test_get(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketCustomField

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = 1
        ticket.ownerstaffid = 1
        ticket.type = 'default'
        ticket.add()

        custom_field_groups = api.get_all(TicketCustomField, ticket.id)

        ticket.delete()

        assert len(custom_field_groups), len(custom_field_groups)
        assert len(custom_field_groups[0].fields), len(custom_field_groups[0].fields)

        custom_field_group = custom_field_groups[0]
        custom_field = custom_field_group.fields[0]

        assert custom_field_group.id, custom_field_group.id
        assert custom_field_group.title, custom_field_group.title
        assert str(custom_field_group), str(custom_field_group)

        assert custom_field.id, custom_field.id
        assert custom_field.type, custom_field.type
        assert custom_field.title, custom_field.title
        assert custom_field.value is not UnsetParameter, custom_field.value
        assert str(custom_field), str(custom_field)
