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

class TicketPriority(KayakoObject):
    '''
    Kayako TicketPriority API Object.
    
    id
    title
    displayorder
    frcolorcode
    bgcolorcode
    displayicon
    type
    uservisibilitycustom
    usergroupid

    '''

    controller = '/Tickets/TicketPriority'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'frcolorcode',
        'bgcolorcode',
        'displayicon',
        'type',
        'uservisibilitycustom',
        'usergroupid',
    ]

    @classmethod
    def _parse_ticket_priority(cls, ticket_priority_tree):

        params = dict(
            id=cls._get_int(ticket_priority_tree.find('id')),
            title=cls._get_string(ticket_priority_tree.find('title')),
            displayorder=cls._get_int(ticket_priority_tree.find('displayorder')),
            frcolorcode=cls._get_string(ticket_priority_tree.find('frcolorcode')),
            bgcolorcode=cls._get_string(ticket_priority_tree.find('bgcolorcode')),
            displayicon=cls._get_string(ticket_priority_tree.find('displayicon')),
            type=cls._get_string(ticket_priority_tree.find('type')),
            uservisibilitycustom=cls._get_boolean(ticket_priority_tree.find('uservisibilitycustom')),
            usergroupid=cls._get_int(ticket_priority_tree.find('usergroupid'), required=False),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketPriority(api, **cls._parse_ticket_priority(ticket_priority_tree)) for ticket_priority_tree in tree.findall('ticketpriority')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('ticketpriority')
        if node is None:
            return None
        params = cls._parse_ticket_priority(tree.find('ticketpriority'))
        return TicketPriority(api, **params)

    def __str__(self):
        return '<TicketPriority (%s): %s>' % (self.id, self.title)

class TicketStatus(KayakoObject):
    '''
    Kayako TicketStatus API Object.
    
    id
    title
    displayorder
    departmentid
    displayicon
    type
    displayinmainlist
    markasresolved
    displaycount
    statuscolor
    statusbgcolor
    resetduetime
    triggersurvey
    staffvisibilitycustom

    '''

    controller = '/Tickets/TicketStatus'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'departmentid',
        'displayicon',
        'type',
        'displayinmainlist',
        'markasresolved',
        'displaycount',
        'statuscolor',
        'statusbgcolor',
        'resetduetime',
        'triggersurvey',
        'staffvisibilitycustom',
    ]

    @classmethod
    def _parse_ticket_status(cls, ticket_status_tree):

        params = dict(
            id=cls._get_int(ticket_status_tree.find('id')),
            title=cls._get_string(ticket_status_tree.find('title')),
            displayorder=cls._get_int(ticket_status_tree.find('displayorder')),
            departmentid=cls._get_int(ticket_status_tree.find('departmentid')),
            displayicon=cls._get_string(ticket_status_tree.find('displayicon')),
            type=cls._get_string(ticket_status_tree.find('type')),
            displayinmainlist=cls._get_boolean(ticket_status_tree.find('displayinmainlist')),
            markasresolved=cls._get_boolean(ticket_status_tree.find('markasresolved')),
            displaycount=cls._get_int(ticket_status_tree.find('displaycount')),
            statuscolor=cls._get_string(ticket_status_tree.find('statuscolor')),
            statusbgcolor=cls._get_string(ticket_status_tree.find('statusbgcolor')),
            resetduetime=cls._get_boolean(ticket_status_tree.find('resetduetime')),
            triggersurvey=cls._get_boolean(ticket_status_tree.find('triggersurvey')),
            staffvisibilitycustom=cls._get_boolean(ticket_status_tree.find('staffvisibilitycustom')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketStatus(api, **cls._parse_ticket_status(ticket_status_tree)) for ticket_status_tree in tree.findall('ticketstatus')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('ticketstatus')
        if node is None:
            return None
        params = cls._parse_ticket_status(node)
        return TicketStatus(api, **params)

    def __str__(self):
        return '<TicketStatus (%s): %s>' % (self.id, self.title)

class TicketType(KayakoObject):
    '''
    Kayako TicketType API Object.
    
    id
    title
    displayorder
    departmentid
    displayicon
    type
    uservisibilitycustom

    '''

    controller = '/Tickets/TicketType'

    __parameters__ = [
        'id',
        'title',
        'displayorder',
        'departmentid',
        'displayicon',
        'type',
        'uservisibilitycustom',
    ]

    @classmethod
    def _parse_ticket_type(cls, ticket_type_tree):

        params = dict(
            id=cls._get_int(ticket_type_tree.find('id')),
            title=cls._get_string(ticket_type_tree.find('title')),
            displayorder=cls._get_int(ticket_type_tree.find('displayorder')),
            departmentid=cls._get_int(ticket_type_tree.find('departmentid')),
            displayicon=cls._get_string(ticket_type_tree.find('displayicon')),
            type=cls._get_string(ticket_type_tree.find('type')),
            uservisibilitycustom=cls._get_boolean(ticket_type_tree.find('uservisibilitycustom')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [TicketType(api, **cls._parse_ticket_type(ticket_type_tree)) for ticket_type_tree in tree.findall('tickettype')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('tickettype')
        if node is None:
            return None
        params = cls._parse_ticket_type(node)
        return TicketType(api, **params)

    def __str__(self):
        return '<TicketType (%s): %s>' % (self.id, self.title)
