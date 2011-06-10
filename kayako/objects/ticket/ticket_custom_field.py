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

from kayako.core.object import KayakoObject
from kayako.exception import KayakoResponseError

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

class TicketCustomFieldGroup(KayakoObject):
    '''
    Kayako TicketCustomFieldGroup API Object.
    
    id
    title
    fields
    '''

    __parameters__ = ['id', 'title', 'fields']

    def __init__(self, id, title, fields):
        self.id = id
        self.title = title
        self.fields = fields

    def __str__(self):
        return '<TicketCustomFieldGroup (%s): %s (%s field%s)>' % (self.id, self.title, len(self.fields) if self.fields else 0, '' if self.fields and len(self.fields) == 1 else 's')

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
        try:
            response = api._request('%s/%s' % (cls.controller, ticketid), 'GET')
        except KayakoResponseError, error:
            if 'HTTP Error 404' in str(error):
                return None
            else:
                raise

        # Strip possible error text.
        response = response.read()
        if response.startswith('<div'):
            response = '\n'.join(response.split('\n')[1:])

        tree = etree.fromstring(response)

        groups = []
        for group_tree in tree.findall('group'):
            fields = [TicketCustomField(api, **cls._parse_ticket_custom_field(custom_field, ticketid)) for custom_field in group_tree.findall('field')]
            ticket_group = TicketCustomFieldGroup(cls._parse_int(group_tree.get('id')), group_tree.get('title'), fields)
            groups.append(ticket_group)
        return groups

    @property
    def short_value(self):
        value = str(self.value)
        if len(value) > 20:
            return '%s...' % value[:20]
        return value

    def __str__(self):
        return '<TicketCustomField (%s): %s %s>' % (self.id, self.type, self.short_value)
