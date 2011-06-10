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
from kayako.exception import KayakoRequestError, KayakoResponseError

class TicketNote(KayakoObject):
    '''
    Kayako TicketNote API Object.
    
    ticketid     The unique numeric identifier of the ticket.
    contents     The ticket note contents
    staffid      The Staff ID, if the ticket is to be created as a staff.
    fullname     The Fullname, if the ticket is to be created without providing a staff user. Example: System messages, Alerts etc.
    forstaffid   The Staff ID, this value can be provided if you wish to restrict the note visibility to a specific staff
    notecolor    The Note Color, for more information see note colors (http://wiki.kayako.com/display/DEV/Mobile+-+Constants)
    '''

    controller = '/Tickets/TicketNote'

    __parameters__ = [
        'id',
        'ticketid',
        'contents',
        'staffid',
        'fullname',
        'forstaffid',
        'notecolor',
        'type',
        'creatorstaffid',
        'creatorstaffname',
        'creationdate',
    ]

    __required_add_parameters__ = ['ticketid', 'contents']
    __add_parameters__ = ['ticketid', 'contents', 'staffid', 'fullname', 'forstaffid', 'notecolor']

    @classmethod
    def _parse_ticket_note(cls, ticket_note_tree, ticketid):
        id = cls._parse_int(ticket_note_tree.get('id'))
        params = dict(
            id=cls._parse_int(ticket_note_tree.get('id')),
            ticketid=ticketid,
            contents=ticket_note_tree.text,
            staffid=cls._parse_int(ticket_note_tree.get('staffid'), required=False),
            forstaffid=cls._parse_int(ticket_note_tree.get('forstaffid')),
            notecolor=cls._parse_int(ticket_note_tree.get('notecolor')),
            type=ticket_note_tree.get('type'),
            creatorstaffid=cls._parse_int(ticket_note_tree.get('creatorstaffid')),
            creatorstaffname=ticket_note_tree.get('creatorstaffname'),
            creationdate=cls._parse_date(ticket_note_tree.get('creationdate')),
        )
        return params

    def _update_from_response(self, ticket_note_tree):

        self.contents = ticket_note_tree.text

        for int_attr in ['id', 'staffid', 'forstaffid', 'notecolor', 'creatorstaffid']:
            attr = ticket_note_tree.get(int_attr)
            if attr is not None:
                setattr(self, int_attr, self._parse_int(attr, required=False))

        for str_attr in ['type', 'creatorstaffname']:
            attr = ticket_note_tree.get(str_attr)
            if attr is not None:
                setattr(self, str_attr, attr)

        for date_attr in ['creationdate']:
            attr = ticket_note_tree.get(date_attr)
            if attr is not None:
                setattr(self, date_attr, self._parse_date(attr, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketNotes for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketNote(api, **cls._parse_ticket_note(ticket_note_tree, ticketid)) for ticket_note_tree in tree.findall('note')]

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
        node = tree.find('note')
        if node is None:
            return None
        params = cls._parse_ticket_note(node, ticketid)
        return TicketNote(api, **params)

    def add(self):
        '''
        Add this TicketNote.
        
        Requires:
            ticketid     The unique numeric identifier of the ticket.
            contents     The ticket note contents
        Requires one:
            staffid      The Staff ID, if the ticket is to be created as a staff.
            fullname     The Fullname, if the ticket is to be created without providing a staff user. Example: System messages, Alerts etc.
        Optional:
            forstaffid   The Staff ID, this value can be provided if you wish to restrict the note visibility to a specific staff
            notecolor    The Note Color, for more information see note colors
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters

        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if ('fullname' not in parameters and 'staffid' not in parameters) or ('fullname' in parameters and 'staffid' in parameters):
            raise KayakoRequestError('To add a TicketNote, just one of the following parameters must be set: fullname, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('note')
        self._update_from_response(node)

    def delete(self):
        if not self.id:
            raise KayakoRequestError('Cannot delete a TicketNote without being attached to a ticket. The ID of the TicketNote (id) has not been specified.')
        if not self.ticketid:
            raise KayakoRequestError('Cannot delete a TicketNote without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def __str__(self):
        return '<TicketNote (%s): %s>' % (self.id, self.contents[:20])
