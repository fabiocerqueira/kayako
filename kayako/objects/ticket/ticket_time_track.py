# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on Jun 10, 2011

@author: evan
'''

from lxml import etree

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError

class TicketTimeTrack(KayakoObject):
    '''
    Kayako TicketTimeTrack API Object.
    
    ticketid      The unique numeric identifier of the ticket.
    id            The unique numeric identifier of the ticket time tracking note.
    contents      The ticket time tracking note contents
    staffid       The ticket time tracking creator staff identifier - synonym for creatorstaffid
    creatorstaffname
    worktimeline  The datetime which specifies when the work was executed - synonym for workdate
    billtimeline  The datetime which specifies when to bill the user - synonym for billdate
    timespent     The time spent (in seconds).  - synonym for timeworked
    timebillable  The time billable (in seconds).
    workerstaffid The staff identifier of the worker. If not specified, the staff user creating this entry will be considered as the worker.
    workerstaffname
    notecolor     The Note Color, for more information see note colors
    '''

    __parameters__ = [
        'id',
        'ticketid',
        'contents',
        'staffid',
        'worktimeline',
        'billtimeline',
        'timespent',
        'timebillable',
        'workerstaffid',
        'notecolor',
        'creatorstaffid',
        'creatorstaffname',
        'workerstaffname',
    ]

    __required_add_parameters__ = ['ticketid', 'contents', 'staffid', 'worktimeline', 'billtimeline', 'timespent', 'timebillable']
    __add_parameters__ = ['ticketid', 'contents', 'staffid', 'worktimeline', 'billtimeline', 'timespent', 'timebillable', 'workerstaffid', 'notecolor']

    controller = '/Tickets/TicketTimeTrack'

    @classmethod
    def _parse_ticket_time_track(cls, ticket_time_track_tree, ticket_id):

        params = dict(
            id=cls._parse_int(ticket_time_track_tree.get('id')), #
            ticketid=ticket_id, #
            contents=ticket_time_track_tree.text,
            staffid=cls._parse_int(ticket_time_track_tree.get('creatorstaffid')), #
            creatorstaffname=ticket_time_track_tree.get('creatorstaffname'), #
            worktimeline=cls._parse_date(ticket_time_track_tree.get('workdate')),
            billtimeline=cls._parse_date(ticket_time_track_tree.get('billdate')),
            timespent=cls._parse_int(ticket_time_track_tree.get('timeworked')), #
            timebillable=cls._parse_int(ticket_time_track_tree.get('timebillable')), #
            workerstaffid=cls._parse_int(ticket_time_track_tree.get('workerstaffid')), #
            workerstaffname=ticket_time_track_tree.get('workerstaffname'), #
            notecolor=cls._parse_int(ticket_time_track_tree.get('notecolor')), #
        )
        return params

    def _update_from_response(self, ticket_time_track_tree):
        self.id = self._parse_int(ticket_time_track_tree.get('id'))
        self.ticketid = self._parse_int(ticket_time_track_tree.get('ticketid'))
        self.contents = ticket_time_track_tree.text
        self.staffid = self._parse_int(ticket_time_track_tree.get('creatorstaffid'))
        self.creatorstaffname = ticket_time_track_tree.get('creatorstaffname')
        self.worktimeline = self._parse_date(ticket_time_track_tree.get('workdate'))
        self.billtimeline = self._parse_date(ticket_time_track_tree.get('billdate'))
        self.timespent = self._parse_int(ticket_time_track_tree.get('timeworked'))
        self.timebillable = self._parse_int(ticket_time_track_tree.get('timebillable'))
        self.workerstaffid = self._parse_int(ticket_time_track_tree.get('workerstaffid'))
        self.workerstaffname = ticket_time_track_tree.get('workerstaffname')
        self.notecolor = self._parse_int(ticket_time_track_tree.get('notecolor'))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketTimeTracks for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketTimeTrack(api, **cls._parse_ticket_time_track(ticket_time_track_tree, ticketid)) for ticket_time_track_tree in tree.findall('timetrack')]

    @classmethod
    def get(cls, api, ticketid, id):
        try:
            response = api._request('%s/%s/%s/' % (cls.controller, ticketid, id), 'GET')
        except KayakoResponseError, error:
            if 'HTTP Error 404' in str(error):
                return None
            else:
                raise
        tree = etree.parse(response)

        print etree.tostring(tree, pretty_print=True)

        node = tree.find('timetrack')
        if node is None:
            return None
        params = cls._parse_ticket_time_track(node, ticketid)
        return TicketTimeTrack(api, **params)

    def add(self):
        '''
        Add this TicketTimeTrack.
        
        Requires:
            ticketid     The unique numeric identifier of the ticket.
            contents     The ticket time tracking note contents
            staffid      The ticket time tracking creator staff identifier
            worktimeline The UNIX timestamp which specifies when the work was executed
            billtimeline The UNIX timestamp which specifies when to bill the user
            timespent    The time spent (in seconds).
            timebillable The time billable (in seconds). 
        Optional:
            workerstaffid The staff identifier of the worker. If not specified, the staff user creating this entry will be considered as the worker.
            notecolor     The Note Color
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters

        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('timetrack')
        self._update_from_response(node)

    def delete(self):
        if self.ticketid is None or self.ticketid is UnsetParameter:
            raise KayakoRequestError('Cannot delete a TicketTimeTrack without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def __str__(self):
        return '<TicketTimeTrack (%s): %s>' % (self.id, self.workerstaffname)
