# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jun 8, 2011

@author: evan
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.objects.ticket.ticket_note import TicketNote
from kayako.objects.ticket.ticket_post import TicketPost
from kayako.objects.ticket.ticket_time_track import TicketTimeTrack
from kayako.exception import KayakoRequestError, KayakoResponseError

class Ticket(KayakoObject):
    '''
    Kayako Ticket API Object.
    
    subject          The Ticket Subject
    fullname         Full Name of creator
    email            Email Address of creator
    contents         The contents of the first ticket post
    departmentid     The Department ID
    ticketstatusid   The Ticket Status ID
    ticketpriorityid The Ticket Priority ID
    tickettypeid     The Ticket Type ID
    userid           The User ID, if the ticket is to be created as a user.
    staffid          The Staff ID, if the ticket is to be created as a staff
    ownerstaffid     The Owner Staff ID, if you want to set an Owner for this
                     ticket
    type             The ticket type: 'default' or 'phone' 
    '''

    controller = '/Tickets/Ticket'

    __parameters__ = [
        'id',
        'subject',
        'fullname',
        'email',
        'contents',
        'departmentid',
        'ticketstatusid',
        'ticketpriorityid', # synonym for priorityid
        'tickettypeid',
        'userid',
        'staffid',
        'ownerstaffid',
        'type',
        'flagtype',
        'displayid',
        'statusid',
        'typeid',
        'userorganization',
        'userorganizationid',
        'ownerstaffname',
        'lastreplier',
        'creationtime',
        'lastactivity',
        'laststaffreply',
        'lastuserreply',
        'slaplanid',
        'nextreplydue',
        'resolutiondue',
        'replies',
        'ipaddress',
        'creator',
        'creationmode',
        'creationtype',
        'isescalated',
        'escalationruleid',
        'tags',
        'watchers',
        'workflows',
        'notes',
        'posts',
        'timetracks',
    ]

    __required_add_parameters__ = ['subject', 'fullname', 'email', 'contents', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'tickettypeid', ]
    __add_parameters__ = ['subject', 'fullname', 'email', 'contents', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'tickettypeid', 'userid', 'staffid', 'ownerstaffid', 'type']

    __save_parameters__ = ['subject', 'fullname', 'email', 'departmentid', 'ticketstatusid', 'ticketpriorityid', 'ownerstaffid', 'userid', ]

    @classmethod
    def _parse_ticket(cls, api, ticket_tree):

        ticketid = cls._parse_int(ticket_tree.get('id'))

        workflows = [dict(id=workflow_node.get('id'), title=workflow_node.get('title')) for workflow_node in ticket_tree.findall('workflow')]
        watchers = [dict(staffid=watcher_node.get('staffid'), name=watcher_node.get('name')) for watcher_node in ticket_tree.findall('watcher')]
        notes = [TicketNote(api, **TicketNote._parse_ticket_note(ticket_note_tree, ticketid)) for ticket_note_tree in ticket_tree.findall('note') if ticket_note_tree.get('type') == 'ticket']
        timetracks = [TicketTimeTrack(api, **TicketTimeTrack._parse_ticket_time_track(ticket_time_track_tree, ticketid)) for ticket_time_track_tree in ticket_tree.findall('note') if ticket_note_tree.get('type') == 'timetrack']

        posts = []
        posts_node = ticket_tree.find('posts')
        if posts_node is not None:
            posts = [TicketPost(api, **TicketPost._parse_ticket_post(ticket_post_tree, ticketid)) for ticket_post_tree in posts_node.findall('post')]

        params = dict(
            id=ticketid,
            subject=cls._get_string(ticket_tree.find('subject')),
            fullname=cls._get_string(ticket_tree.find('fullname')),
            email=cls._get_string(ticket_tree.find('email')),
            departmentid=cls._get_int(ticket_tree.find('departmentid')),
            ticketstatusid=cls._get_int(ticket_tree.find('ticketstatusid'), required=False),
            ticketpriorityid=cls._get_int(ticket_tree.find('priorityid')), # Note the difference, request param is ticketpriorityid, response is priorityid
            tickettypeid=cls._get_int(ticket_tree.find('tickettypeid'), required=False),
            userid=cls._get_int(ticket_tree.find('userid')),
            ownerstaffid=cls._get_int(ticket_tree.find('ownerstaffid')),
            flagtype=cls._parse_int(ticket_tree.get('flagtype'), 'flagtype'),
            displayid=cls._get_string(ticket_tree.find('displayid')),
            statusid=cls._get_int(ticket_tree.find('statusid')),
            typeid=cls._get_int(ticket_tree.find('typeid')),
            userorganization=cls._get_string(ticket_tree.find('userorganization')),
            userorganizationid=cls._get_int(ticket_tree.find('userorganizationid'), required=False),
            ownerstaffname=cls._get_string(ticket_tree.find('ownerstaffname')),
            lastreplier=cls._get_string(ticket_tree.find('lastreplier')),
            creationtime=cls._get_date(ticket_tree.find('creationtime')),
            lastactivity=cls._get_date(ticket_tree.find('lastactivity')),
            laststaffreply=cls._get_date(ticket_tree.find('laststaffreply')),
            lastuserreply=cls._get_date(ticket_tree.find('lastuserreply')),
            slaplanid=cls._get_int(ticket_tree.find('slaplanid')),
            nextreplydue=cls._get_date(ticket_tree.find('nextreplydue')),
            resolutiondue=cls._get_date(ticket_tree.find('resolutiondue')),
            replies=cls._get_int(ticket_tree.find('replies')),
            ipaddress=cls._get_string(ticket_tree.find('ipaddress')),
            creator=cls._get_int(ticket_tree.find('creator')),
            creationmode=cls._get_int(ticket_tree.find('creationmode')),
            creationtype=cls._get_int(ticket_tree.find('creationtype')),
            isescalated=cls._get_boolean(ticket_tree.find('isescalated')),
            escalationruleid=cls._get_int(ticket_tree.find('escalationruleid')),
            tags=cls._get_string(ticket_tree.find('tags')),
            watchers=watchers,
            workflows=workflows,
            notes=notes,
            posts=posts,
            timetracks=timetracks,
        )
        return params

    def _update_from_response(self, ticket_tree):

        ticketid = self._parse_int(ticket_tree.get('id'))
        if ticketid is not None:
            self.id = ticketid

        priority_node = ticket_tree.find('priorityid')
        if priority_node is not None:
            self.ticketpriorityid = self._get_int(priority_node)

        for int_node in ['departmentid', 'userid', 'ownerstaffid', 'flagtype', 'statusid', 'slaplanid', 'replies', 'creator', 'creationmode', 'creationtype', 'escalationruleid', 'ticketstatusid', 'tickettypeid', 'userorganizationid' ]:
            node = ticket_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['subject', 'email', 'displayid', 'userorganization', 'ownerstaffname', 'lastreplier', 'ipaddress', 'tags']:
            node = ticket_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for bool_node in ['isescalated']:
            node = ticket_tree.find(bool_node)
            if node is not None:
                setattr(self, bool_node, self._get_boolean(node, required=False))

        for date_node in ['creationtime', 'lastactivity', 'lastuserreply', 'nextreplydue', 'resolutiondue', ]:
            node = ticket_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, departmentid, ticketstatusid= -1, ownerstaffid= -1, userid= -1):
        '''
        Get all of the tickets filtered by the parameters:
        Lists are converted to comma-separated values.
        Required:
            departmentid     Filter the tickets by the specified department id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
        Optional:
            ticketstatusid   Filter the tickets by the specified ticket status id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
            ownerstaffid     Filter the tickets by the specified owner staff id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3
            userid           Filter the tickets by the specified user id, you can specify multiple id's by separating the values using a comma. Example: 1,2,3 
        '''

        if isinstance(departmentid, (list, tuple)):
            departmentid = ','.join([str(id_item) for id_item in departmentid])
        if isinstance(ticketstatusid, (list, tuple)):
            ticketstatusid = ','.join([str(id_item) for id_item in ticketstatusid])
        if isinstance(ownerstaffid, (list, tuple)):
            ownerstaffid = ','.join([str(id_item) for id_item in ownerstaffid])
        if isinstance(userid, (list, tuple)):
            userid = ','.join([str(id_item) for id_item in userid])

        response = api._request('%s/ListAll/%s/%s/%s/%s/' % (cls.controller, departmentid, ticketstatusid, ownerstaffid, userid), 'GET')
        tree = etree.parse(response)
        return [Ticket(api, **cls._parse_ticket(api, ticket_tree)) for ticket_tree in tree.findall('ticket')]

    @classmethod
    def get(cls, api, id):
        try:
            response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        except KayakoResponseError, error:
            if 'HTTP Error 404' in str(error):
                return None
            else:
                raise
        tree = etree.parse(response)
        node = tree.find('ticket')
        if node is None:
            return None
        params = cls._parse_ticket(api, node)
        return Ticket(api, **params)

    def add(self):
        '''
        Add this Ticket.
        
        Requires:
            subject          The Ticket Subject
            fullname         Full Name of creator
            email            Email Address of creator
            contents         The contents of the first ticket post
            departmentid     The Department ID
            ticketstatusid   The Ticket Status ID
            ticketpriorityid The Ticket Priority ID
            tickettypeid     The Ticket Type ID
        At least one of these must be present:
            userid           The User ID, if the ticket is to be created as a user.
            staffid          The Staff ID, if the ticket is to be created as a staff
        Optional:
            ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
            type             The ticket type: 'default' or 'phone'
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters
        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if 'userid' not in parameters and 'staffid' not in parameters:
            raise KayakoRequestError('To add a Ticket, at least one of the following parameters must be set: userid, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('ticket')
        self._update_from_response(node)

    def save(self):
        '''
        Save this ticket.
        
        Saves only the following:
            subject          The Ticket Subject
            fullname         Full Name of creator
            email            Email Address of creator
            departmentid     The Department ID
            ticketstatusid   The Ticket Status ID
            ticketpriorityid The Ticket Priority ID
            tickettypeid     The Ticket Type ID
            ownerstaffid     The Owner Staff ID, if you want to set an Owner for this ticket
            userid           The User ID, if you want to change the user for this ticket 
        '''
        response = self._save('%s/%s/' % (self.controller, self.id))
        tree = etree.parse(response)
        node = tree.find('ticket')
        self._update_from_response(node)

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<Ticket (%s): %s - %s>' % (self.id, 'UNSUBMITTED' if not self.displayid else self.displayid, self.subject)
