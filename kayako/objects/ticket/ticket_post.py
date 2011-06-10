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

class TicketPost(KayakoObject):
    '''
    Kayako TicketPost API Object.
    
    ticketid   The unique numeric identifier of the ticket.
    subject    The ticket post subject
    contents   The ticket post contents
    userid     The User ID, if the ticket post is to be created as a user.
    staffid    The Staff ID, if the ticket post is to be created as a staff
    dateline
    fullname
    email
    emailto
    ipaddress
    hasattachments
    creator
    isthirdparty
    ishtml
    isemailed
    issurveycomment
    '''

    __parameters__ = [
        'id',
        'ticketid',
        'subject',
        'contents',
        'userid',
        'staffid',
        'dateline',
        'fullname',
        'email',
        'emailto',
        'ipaddress',
        'hasattachments',
        'creator',
        'isthirdparty',
        'ishtml',
        'isemailed',
        'issurveycomment',
    ]

    __required_add_parameters__ = ['ticketid', 'subject', 'contents']
    __add_parameters__ = ['ticketid', 'subject', 'contents', 'userid', 'staffid']

    controller = '/Tickets/TicketPost'

    @classmethod
    def _parse_ticket_post(cls, ticket_post_tree, ticket_id):

        params = dict(
            id=cls._get_int(ticket_post_tree.find('id')),
            ticketid=ticket_id,
            subject=cls._get_string(ticket_post_tree.find('subject')),
            contents=cls._get_string(ticket_post_tree.find('contents')),
            userid=cls._get_int(ticket_post_tree.find('userid')),
            staffid=cls._get_int(ticket_post_tree.find('staffid')),
            dateline=cls._get_date(ticket_post_tree.find('dateline')),
            fullname=cls._get_string(ticket_post_tree.find('fullname')),
            email=cls._get_string(ticket_post_tree.find('email')),
            emailto=cls._get_string(ticket_post_tree.find('emailto')),
            ipaddress=cls._get_string(ticket_post_tree.find('ipaddress')),
            hasattachments=cls._get_boolean(ticket_post_tree.find('hasattachments')),
            creator=cls._get_int(ticket_post_tree.find('creator')),
            isthirdparty=cls._get_boolean(ticket_post_tree.find('isthirdparty')),
            ishtml=cls._get_boolean(ticket_post_tree.find('ishtml')),
            isemailed=cls._get_boolean(ticket_post_tree.find('isemailed')),
            issurveycomment=cls._get_boolean(ticket_post_tree.find('issurveycomment')),
        )
        return params

    def _update_from_response(self, ticket_post_tree):

        ticketpostid_node = ticket_post_tree.find('id')
        if ticketpostid_node is not None:
            self.id = self._get_int(ticketpostid_node)

        for int_node in ['userid', 'staffid', 'creator']:
            node = ticket_post_tree.find(int_node)
            if node is not None:
                setattr(self, int_node, self._get_int(node, required=False))

        for str_node in ['subject', 'contents', 'fullname', 'email', 'emailto', 'ipaddress']:
            node = ticket_post_tree.find(str_node)
            if node is not None:
                setattr(self, str_node, self._get_string(node))

        for bool_node in ['hasattachments', 'isthirdparty', 'ishtml', 'isemailed', 'issurveycomment']:
            node = ticket_post_tree.find(bool_node)
            if node is not None:
                setattr(self, bool_node, self._get_boolean(node, required=False))

        for date_node in ['dateline']:
            node = ticket_post_tree.find(date_node)
            if node is not None:
                setattr(self, date_node, self._get_date(node, required=False))

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketPosts for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/ListAll/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)
        return [TicketPost(api, **cls._parse_ticket_post(ticket_post_tree, ticketid)) for ticket_post_tree in tree.findall('post')]

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
        node = tree.find('post')
        if node is None:
            return None
        params = cls._parse_ticket_post(node, ticketid)
        return TicketPost(api, **params)

    def add(self):
        '''
        Add this TicketPost.
        
        Requires:
            ticketid  The unique numeric identifier of the ticket.
            subject   The ticket post subject
            contents  The ticket post contents
        Requires one of:
            userid    The User ID, if the ticket post is to be created as a user.
            staffid   The Staff ID, if the ticket post is to be created as a staff 
        '''
        if self.id is not UnsetParameter:
            raise KayakoRequestError('Cannot add a pre-existing %s. Use save instead. (id: %s)' % (self.__class__.__name__, self.id))

        parameters = self.add_parameters

        for required_parameter in self.__required_add_parameters__:
            if required_parameter not in parameters:
                raise KayakoRequestError('Cannot add %s: Missing required field: %s.' % (self.__class__.__name__, required_parameter))

        if ('userid' not in parameters and 'staffid' not in parameters) or ('userid' in parameters and 'staffid' in parameters):
            raise KayakoRequestError('To add a TicketPost, just one of the following parameters must be set: userid, staffid. (id: %s)' % self.id)

        response = self.api._request(self.controller, 'POST', **parameters)
        tree = etree.parse(response)
        node = tree.find('post')
        self._update_from_response(node)

    def delete(self):
        if self.ticketid is None or self.ticketid is UnsetParameter:
            raise KayakoRequestError('Cannot delete a TicketPost without being attached to a ticket. The ID of the Ticket (ticketid) has not been specified.')
        self._delete('%s/%s/%s/' % (self.controller, self.ticketid, self.id))

    def __str__(self):
        return '<TicketPost (%s): %s>' % (self.id, self.subject)
