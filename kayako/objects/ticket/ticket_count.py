# -*- coding: utf-8 -*-
'''
Created on Jun 10, 2011

@author: evan
'''

from lxml import etree

from kayako.core.object import KayakoObject

__all__ = [
    'TicketCountTicketStatus',
    'TicketCountTicketType',
    'TicketCountOwnerStaff',
    'TicketCountUnassignedDepartment',
    'TicketCountDepartment',
    'TicketCount',
]

class TicketCountItem(KayakoObject):
    '''
    Kayako TicketCountItem API Object.
    
    id
    lastactivity
    totalitems
    totalunresolveditems
    '''

    __parameters__ = ['id', 'lastactivity', 'totalitems', 'totalunresolveditems']

    def __init__(self, id, lastactivity, totalitems, totalunresolveditems=None):
        self.id = id
        self.lastactivity = lastactivity
        self.totalitems = totalitems
        self.totalunresolveditems = totalunresolveditems

    @classmethod
    def _from_node(cls, node):
        return cls(cls._parse_int(node.get('id')), cls._parse_date(node.get('lastactivity')), cls._parse_int(node.get('totalitems')), totalunresolveditems=cls._parse_int(node.get('totalunresolveditems'), required=False))

    def __str__(self):
        return '<%s (%s): totalitems=%s lastactivity=%s%s>' % (self.__class__.__name__, self.id, self.totalitems, self.lastactivity, ' totalunresolveditems=%s' % self.totalunresolveditems if self.totalunresolveditems is not None else '')

class TicketCountTicketStatus(TicketCountItem):
    pass

class TicketCountTicketType(TicketCountItem):
    pass

class TicketCountOwnerStaff(TicketCountItem):
    pass

class TicketCountUnassignedDepartment(TicketCountItem):
    pass

class TicketCountDepartment(KayakoObject):
    '''
    Kayako TicketCountDepartment API Object.
    
    id
    totalitems
    lastactivity
    totalunresolveditems
    statuses - A list of TicketCountTicketStatus
    types - A list of TicketCountTicketType
    staff - A list of TicketCountOwnerStaff
    '''

    __parameters__ = ['id', 'totalitems', 'lastactivity', 'totalunresolveditems', 'statuses', 'types', 'staff']

    @classmethod
    def _from_node(cls, node):

        ticketstatus_nodes = node.findall('ticketstatus')
        tickettype_nodes = node.findall('tickettype')
        ownerstaff_nodes = node.findall('ownerstaff')

        params = dict(
            id=cls._parse_int(node.get('id')),
            totalitems=cls._get_int(node.find('totalitems')),
            lastactivity=cls._get_date(node.find('lastactivity')),
            totalunresolveditems=cls._get_int(node.find('totalunresolveditems')),
            statuses=tuple(TicketCountTicketStatus._from_node(ticketstatus_node) for ticketstatus_node in ticketstatus_nodes),
            types=tuple(TicketCountTicketType._from_node(tickettype_node) for tickettype_node in tickettype_nodes),
            staff=tuple(TicketCountOwnerStaff._from_node(ownerstaff_node) for ownerstaff_node in ownerstaff_nodes),
        )

        return TicketCountDepartment(None, **params)

    def __str__(self):
        return '<TicketCountDepartment (%s): totalitems:%s, lastactivity:%s, totalunresolveditems:%s, statuses:%s, types:%s, staff:%s>' % (self.id, self.totalitems, self.lastactivity, self.totalunresolveditems, len(self.statuses), len(self.types), len(self.staff))

class TicketCount(KayakoObject):
    '''
    Kayako TicketCount API Object.
    
    departments - A list of TicketCountDepartment
    statuses - A list of TicketCountTicketStatus
    staff - A list of TicketCountOwnerStaff
    unassigned - A list of TicketCountUnassigned
    '''

    controller = '/Tickets/TicketCount'

    __parameters__ = ['departments', 'statuses', 'staff', 'unassigned']

    def __init__(self, departments, statuses, staff, unassigned):
        self.departments = departments
        self.statuses = statuses
        self.staff = staff
        self.unassigned = unassigned

    @classmethod
    def _parse_ticket_count(cls, tree):

        departments = tuple()
        parent = tree.find('departments')
        if parent is not None:
            nodes = parent.findall('department')
            departments = tuple(TicketCountDepartment._from_node(node) for node in nodes)

        statuses = tuple()
        parent = tree.find('statuses')
        if parent is not None:
            nodes = parent.findall('ticketstatus')
            statuses = tuple(TicketCountTicketStatus._from_node(node) for node in nodes)

        staff = tuple()
        parent = tree.find('owners')
        if parent is not None:
            nodes = parent.findall('ownerstaff')
            staff = tuple(TicketCountOwnerStaff._from_node(node) for node in nodes)

        unassigned = tuple()
        parent = tree.find('unassigned')
        if parent is not None:
            nodes = parent.findall('department')
            unassigned = tuple(TicketCountUnassignedDepartment._from_node(node) for node in nodes)

        params = dict(
            departments=departments,
            statuses=statuses,
            staff=staff,
            unassigned=unassigned,
        )

        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return TicketCount(**cls._parse_ticket_count(tree))

    def __str__(self):
        return '<TicketCount: departments:%s, statuses:%s, staff:%s, unassigned:%s>' % (len(self.departments), len(self.statuses), len(self.staff), len(self.unassigned))

