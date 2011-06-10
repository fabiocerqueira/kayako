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

class TestTicketSearch(KayakoAPITest):

    SUBJECT = 'DELETEME'

    def tearDown(self):
        from kayako.objects import Department, Ticket
        dept = self.api.first(Department, module='tickets')
        test_tickets = self.api.filter(Ticket, args=(dept.id,), subject=self.SUBJECT)
        for ticket in test_tickets:
            ticket.delete()
        super(TestTicketSearch, self).tearDown()

    def test_search_all(self):
        from kayako.objects import Department, Ticket

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

        ticket_id = ticket.id

        self.log(ticket_id)

        tickets = api.ticket_search('test', ticketid=True, contents=True, author=True, email=True, creatoremail=True, fullname=True, notes=True, usergroup=True, userorganization=True, user=True, tags=True)
        ticket_ids = [ticket_item.id for ticket_item in tickets]

        ticket.delete()

        self.log(tickets)

        self.log(ticket_ids)

        assert ticket_id in ticket_ids
        assert len(tickets)

