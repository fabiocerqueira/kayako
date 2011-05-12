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

from kayako.test import KayakoAPITest

class TestTicketPost(KayakoAPITest):

    def test_get_all(self):
        from kayako.objects import Department, Ticket, TicketPost

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'test_post'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = 1
        ticket_post.add()

        result = self.api.get_all(TicketPost, ticket.id)
        assert isinstance(result, list)
        assert result

        ticket_post.delete()
        ticket.delete()

    def test_get(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketPost

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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

        assert ticket.id is not UnsetParameter

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'test_post'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = 1
        ticket_post.add()
        assert ticket_post.ticketid == ticket.id

        ticket = api.get(Ticket, ticket.id)
        assert ticket.posts[0].ticketid == ticket.id

        result = self.api.get(TicketPost, ticket.id, ticket_post.id)
        assert result.id == ticket_post.id

        assert 'TicketPost ' in str(result)

        ticket_post.delete()
        ticket.delete()

    def test_add_missing_ticketid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost

        ticket_post = self.api.create(TicketPost)

        ticket_post.subject = 'test note'
        ticket_post.contents = 'this is just a test'
        ticket_post.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_post.add)

    def test_add_missing_subject(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost

        ticket_post = self.api.create(TicketPost)

        ticket_post.ticketid = 1
        ticket_post.contents = 'this is just a test'
        ticket_post.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_post.add)

    def test_add_missing_contents(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost

        ticket_post = self.api.create(TicketPost)

        ticket_post.ticketid = 1
        ticket_post.subject = 'test note'
        ticket_post.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_post.add)

    def test_add_missing_userid_and_staffid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost

        ticket_post = self.api.create(TicketPost)

        ticket_post.ticketid = 1
        ticket_post.subject = 'test note'
        ticket_post.contents = 'this is just a test'

        self.assertRaises(KayakoRequestError, ticket_post.add)

    def test_add_with_both_userid_and_staffid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost

        ticket_post = self.api.create(TicketPost)

        ticket_post.ticketid = 1
        ticket_post.subject = 'test note'
        ticket_post.contents = 'this is just a test'
        ticket_post.userid = 'test name'
        ticket_post.staffid = 1

        self.assertRaises(KayakoRequestError, ticket_post.add)

    def test_add_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department, Ticket, TicketPost

        api = self.api

        depts = api.get_all(Department)
        for dept in depts:
            if dept.module == 'tickets':
                break

        ticket = api.create(Ticket)
        ticket.subject = 'DELETE_ME'
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

        ticket_post = api.create(TicketPost)
        ticket_post.ticketid = ticket.id
        ticket_post.subject = 'DELETE_ME'
        ticket_post.contents = 'testing a post'
        ticket_post.userid = 1
        ticket_post.add()

        assert ticket_post.id is not UnsetParameter
        ticket_post.delete()
        ticket.delete()

    def test_delete_unadded(self):
        from kayako.core.lib import UnsetParameter
        from kayako.exception import KayakoRequestError
        from kayako.objects import TicketPost
        ticket_post = self.api.create(TicketPost)
        ticket_post.id = UnsetParameter
        ticket_post.ticketid = 1
        self.assertRaises(KayakoRequestError, ticket_post.delete)
        ticket_post.id = 1
        ticket_post.ticketid = UnsetParameter
        self.assertRaises(KayakoRequestError, ticket_post.delete)
