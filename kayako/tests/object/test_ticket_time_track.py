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

class TestTicketTimeTrack(KayakoAPITest):

    SUBJECT = 'DELETEME'

    def tearDown(self):
        from kayako.objects import Department, Ticket
        dept = self.api.first(Department, module='tickets')
        test_tickets = self.api.filter(Ticket, args=(dept.id,), subject=self.SUBJECT)
        for ticket in test_tickets:
            ticket.delete()
        super(TestTicketTimeTrack, self).tearDown()

    def test_get_nonexistant(self):
        from kayako.objects import Department, Ticket, TicketTimeTrack

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

        obj = api.get(TicketTimeTrack, ticket.id, 'abc123')

        ticket.delete()

        assert obj is None

    def test_add_get(self):
        from datetime import datetime
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketTimeTrack, Staff, User
        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        staff = api.get(Staff, 0)
        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_time_track = api.create(TicketTimeTrack)
        ticket_time_track.ticketid = ticket.id
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = staff.id
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344
        ticket_time_track.add()

        obj2 = api.get(TicketTimeTrack, ticket.id, ticket_time_track.id)

        ticket.delete()

        assert ticket_time_track.id is not UnsetParameter
        assert obj2 is not None

    def test_get_all(self):
        from datetime import datetime
        from kayako.objects import Department, Ticket, TicketTimeTrack, Staff, User

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        staff = api.get(Staff, 0)
        user = api.get(User, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_time_track = api.create(TicketTimeTrack)
        ticket_time_track.ticketid = ticket.id
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = staff.id
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344
        ticket_time_track.add()

        result = api.get_all(TicketTimeTrack, ticket.id)

        assert isinstance(result, list)
        assert result
        assert ticket_time_track.id in [t.id for t in result]

        ticket_time_track.delete()
        ticket.delete()

    def test_add_missing_ticketid(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = 1
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_contents(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.staffid = 1
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_staffid(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_worktimeline(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = 1
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_billtimeline(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = 1
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_timespent(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = 1
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timebillable = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_missing_timebillable(self):
        from datetime import datetime
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = 1
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = 1
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344

        self.assertRaises(KayakoRequestError, ticket_time_track.add)

    def test_add_delete(self):
        from datetime import datetime
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketTimeTrack, User, Staff

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        user = api.get(User, 0)
        staff = api.get(Staff, 0)

        ticket = api.create(Ticket)
        ticket.subject = self.SUBJECT
        ticket.fullname = 'Unit Test'
        ticket.email = 'test@example.com'
        ticket.contents = 'test'
        ticket.departmentid = dept.id
        ticket.ticketstatusid = 1
        ticket.ticketpriorityid = 1
        ticket.tickettypeid = 1
        ticket.userid = user.id
        ticket.ownerstaffid = user.id
        ticket.type = 'default'
        ticket.add()

        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.ticketid = ticket.id
        ticket_time_track.contents = 'DELETEME'
        ticket_time_track.staffid = staff.id
        ticket_time_track.worktimeline = datetime.now()
        ticket_time_track.billtimeline = datetime.now()
        ticket_time_track.timespent = 2344
        ticket_time_track.timebillable = 2344
        ticket_time_track.add()

        old_id = ticket_time_track.id

        ticket_time_track.delete()
        ticket.delete()

        assert old_id is not UnsetParameter
        assert ticket_time_track.contents == 'DELETEME'

    def test_delete_unadded(self):
        from kayako.core.lib import UnsetParameter
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketTimeTrack
        ticket_time_track = self.api.create(TicketTimeTrack)
        ticket_time_track.id = UnsetParameter
        ticket_time_track.ticketid = 1
        self.assertRaises(KayakoRequestError, ticket_time_track.delete)
        ticket_time_track.id = 1
        ticket_time_track.ticketid = UnsetParameter
        self.assertRaises(KayakoRequestError, ticket_time_track.delete)
