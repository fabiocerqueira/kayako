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

__all__ = [
   'CustomFieldTypes',
   'TicketCustomFieldGroup',
   'TicketCustomField',
]

class CustomFieldTypes(object):
    ''' CustomFieldTypes Enum class
    
    Text         1
    Text area    2
    Password     3
    Checkbox     4
    Radio        5
    Select       6
    Multi select 7
    Custom       8
    Linked select fields     9
    Date         10
    File         11 
    '''
    TYPES = {
        1 : 'TEXT',
        2 : 'TEXT_AREA',
        3 : 'PASSWORD',
        4 : 'CHECKBOX',
        5 : 'RADIO',
        6 : 'SELECT',
        7 : 'MULTI_SELECT',
        8 : 'CUSTOM',
        9 : 'LINKED_SELECT_FIELDS',
        10 : 'DATE',
        11 : 'FILE',
    }

    @classmethod
    def id_by_name(cls, name):
        for key, value in cls.TYPES.iteritems():
            if name == value:
                return key

    @classmethod
    def name_by_id(cls, id):
        return cls.TYPES.get(id, None)

class TicketCustomFieldGroup(object):

    def __init__(self, id, title, fields):
        self.id = id
        self.title = title
        self.fields = fields

class TicketCustomField(KayakoObject):
    '''
    Kayako TicketCustomField API Object.
    
    id
    type
    title
    value
    '''

    __parameters__ = [
        'id',
        'title',
        'type',
        'value',
    ]

    __required_add_parameters__ = []
    ''' Add not available for TicketCustomField. '''
    __add_parameters__ = []
    ''' Add not available for TicketCustomField. '''

    __required_save_parameters__ = []
    ''' Save not available for TicketCustomField. '''
    __save_parameters__ = []
    ''' Save not available for TicketCustomField. '''

    controller = '/Tickets/TicketCustomField'

    @classmethod
    def _parse_ticket_custom_field(cls, ticket_custom_field_tree, ticket_id):

        params = dict(
            id=cls._parse_int(ticket_custom_field_tree.get('id')),
            title=ticket_custom_field_tree.get('title'),
            type=CustomFieldTypes.name_by_id(cls._parse_int(ticket_custom_field_tree.get('type'))),
            value=ticket_custom_field_tree.text,
        )

        return params

    @classmethod
    def get_all(cls, api, ticketid):
        '''
        Get all of the TicketPosts for a ticket.
        Required:
            ticketid     The unique numeric identifier of the ticket. 
        '''
        response = api._request('%s/%s' % (cls.controller, ticketid), 'GET')
        tree = etree.parse(response)

        groups = []
        for group_tree in tree.findall('group'):
            fields = [TicketCustomField(api, **cls._parse_ticket_custom_field(custom_field)) for custom_field in group_tree.findall('field')]
            ticket_group = TicketCustomFieldGroup(cls._parse_int(tree.get('id')), tree.get('title'), fields)
            groups.append(ticket_group)
        return groups


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
