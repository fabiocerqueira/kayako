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

    def test_get_nonexistant(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        obj = api.get(TicketNote, ticket.id, 'abc123')

        ticket.delete()

        assert obj is None

    def test_add_get_bare_staffid(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.contents = 'testing a post'
        ticket_note.staffid = 1
        ticket_note.add()

        self.log(ticket_note.id)

        obj2 = api.get(TicketNote, ticket.id, ticket_note.id)
        assert obj2 is not None
        ticket.delete()

    def test_add_get_bare_fullname(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        self.log(ticket)

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.contents = 'testing a post'
        ticket_note.fullname = 'testing'
        ticket_note.add()

        self.log(ticket_note)
        self.log(ticket_note.id)

        obj2 = api.get(TicketNote, ticket.id, ticket_note.id)
        assert obj2 is not None
        ticket.delete()

    def test_add_get_full_staffid(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.subject = 'test_post'
        ticket_note.contents = 'testing a post'
        ticket_note.staffid = 1
        ticket_note.notecolor = 1
        ticket_note.forstaff_id = 1
        ticket_note.add()

        obj2 = api.get(TicketNote, ticket.id, ticket_note.id)
        assert obj2 is not None
        ticket.delete()

    def test_add_get_full_fullname(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.subject = 'test_post'
        ticket_note.contents = 'testing a post'
        ticket_note.fullname = 'testing'
        ticket_note.notecolor = 1
        ticket_note.forstaff_id = 1
        ticket_note.add()

        obj2 = api.get(TicketNote, ticket.id, ticket_note.id)
        assert obj2 is not None
        ticket.delete()


    def test_get_all(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.subject = 'test_post'
        ticket_note.contents = 'testing a post'
        ticket_note.staffid = 1
        ticket_note.add()

        result = self.api.get_all(TicketNote, ticket.id)
        assert isinstance(result, list)
        assert result

        ticket = api.get(Ticket, ticket.id)
        assert ticket.notes[0].ticketid == ticket.id

        assert 'TicketNote ' in str(ticket.notes[0])

        ticket.delete()


    def test_add_missing_ticketid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.ticketid = 1
        ticket_note.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_missing_contents(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.contents = 'this is just a test'
        ticket_note.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_missing_staffid_and_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.contents = 'this is just a test'

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_add_both_staffid_and_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketNote

        ticket_note = self.api.create(TicketNote)

        ticket_note.ticketid = 1
        ticket_note.contents = 'this is just a test'
        ticket_note.staffid = 1
        ticket_note.fullname = 'test name'

        self.assertRaises(KayakoRequestError, ticket_note.add)

    def test_delete(self):
        from kayako.objects import Department, Ticket, TicketNote

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

        ticket_note = api.create(TicketNote)
        ticket_note.ticketid = ticket.id
        ticket_note.contents = 'testing a post'
        ticket_note.staffid = 1
        ticket_note.add()

        ticket_note.delete()

        ticket.delete()
