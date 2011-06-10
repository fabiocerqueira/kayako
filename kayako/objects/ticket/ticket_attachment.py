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

from kayako.core.lib import UnsetParameter
from kayako.core.object import KayakoObject
from kayako.exception import KayakoRequestError, KayakoResponseError
from lxml import etree
import base64

class TicketAttachment(KayakoObject):
    '''
    Kayako TicketAttachment API Object.
    
    ticketid     The unique numeric identifier of the ticket.
    ticketpostid The unique numeric identifier of the ticket post.
    filename     The file name for the attachment
    contents     The BASE64 encoded attachment contents 
    filesize
    filetype
    dateline
    '''

    controller = '/Tickets/TicketAttachment'

    __parameters__ = [
        'id',
        'ticketid',
        'ticketpostid',
        'filename',
        'filesize',
        'filetype',
        'contents',
        'dateline',
    ]

    __required_add_parameters__ = ['ticketid', 'ticketpostid', 'filename', 'contents']
    __add_parameters__ = ['ticketid', 'ticketpostid', 'filename', 'contents']

    @classmethod
    def _parse_ticket_attachment(cls, ticket_attachment_tree):

        params = dict(
            id=cls._get_int(ticket_attachment_tree.find('id')),
            ticketid=cls._get_int(ticket_attachment_tree.find('ticketid')),
            ticketpostid=cls._get_int(ticket_attachment_tree.find('ticketpostid')),
            filename=cls._get_string(ticket_attachment_tree.find('filename')),
            filesize=cls._get_int(ticket_attachment_tree.find('filesize')),
            filetype=cls._get_string(ticket_attachment_tree.find('filetype')),
            contents=cls._get_string(ticket_attachment_tree.find('contents')),
            dateline=cls._get_date(ticket_attachment_tree.find('dateline')),
        )
        return params

    def _update_from_response(self, ticket_attachment_tree):
        for int_node in ['id', 'ticketid', 'ticketpostid', 'filesize']:
            node = ticket_attachment_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['filename', 'filetype', 'contents']:
            node = ticket_attachment_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for date_node in ['dateline']:
            node = ticket_attachment_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketAttachments for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketAttachment(api, **cls._parse_ticket_attachment(ticket_attachment_tree)) for ticket_attachment_tree in tree.findall('attachment')]

    @classmethod
    def get(cls, api, ticketid, attachmentid):
        try:
            response = api._request('%s/%s/%s/' % (cls.controller, ticketid, attachmentid), 'GET')
        except KayakoResponseError, error:
            if 'HTTP Error 404' in str(error):
                return None
            else:
                raise
        tree = etree.parse(response)
        node = tree.find('attachment')
        if node is None:
            return None
        params = cls._parse_ticket_attachment(node)
        return TicketAttachment(api, **params)

    def add(self):
        '''
        Add this TicketAttachment.
        
        Requires:
            ticketid     The unique numeric identifier of the ticket.
            ticketpostid The unique numeric identifier of the ticket post.
            filename     The file name for the attachment
            contents     The BASE64 encoded attachment contents 
        '''
        response = self._add(self.controller)
        tree = etree.parse(response)
        node = tree.find('attachment')
        self._update_from_response(node)

    def delete(self):
        if self.ticketid is None or self.ticketid is UnsetParameter:
            raise KayakoRequestError('Cannot delete a TicketAttachment without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def get_contents(self):
        ''' Return the unencoded contents of this TicketAttachment. '''
        if self.contents:
            return base64.b64decode(self.contents)

    def set_contents(self, contents):
        ''' 
        Set this TicketAttachment's contents to Base 64 encoded data, or set the
        contents to nothing.
        '''
        if contents:
            self.contents = base64.b64encode(contents)
        else:
            self.contents = None

    def __str__(self):
        return '<TicketAttachment (%s): %s>' % (self.id, self.filename)
