# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 9, 2011

@author: evan
'''

from lxml import etree

from kayako.core.object import KayakoObject

__all__ = [
    'Staff',
    'StaffGroup',
]

class Staff(KayakoObject):
    '''
    Kayako Staff API Object.
    
    firstname      The first name
    lastname       The last name
    username       The login username
    password       Will only be updated if its specified with the request
    staffgroupid   The staff group ID
    email          The staff email address
    designation    The Designation/Title of Staff
    mobilenumber   The mobile number of Staff user
    signature      The Signature to append to each reply made by staff
    isenabled      Toggle the enabled/disabled property using this flag
    greeting       The default greeting message when the staff accepts a live chat request
    timezone       The default time zone for Staff
    enabledst      Toggle the enabling/disabling of automatic DST calculation 
    '''

    controller = '/Base/Staff'

    __parameters__ = [
        'id',
        'firstname',
        'lastname',
        'username',
        'password',
        'staffgroupid',
        'email',
        'designation',
        'mobilenumber',
        'signature',
        'isenabled',
        'greeting',
        'timezone',
        'enabledst',
    ]

    __required_add_parameters__ = ['firstname', 'lastname', 'username', 'email', 'password', 'staffgroupid']
    __add_parameters__ = ['firstname', 'lastname', 'username', 'email', 'password', 'staffgroupid', 'designation', 'mobilenumber', 'signature', 'isenabled', 'greeting', 'timezone', 'enabledst']

    __required_save_parameters__ = ['firstname', 'lastname']
    __save_parameters__ = ['firstname', 'lastname', 'username', 'email', 'password', 'staffgroupid', 'designation', 'mobilenumber', 'signature', 'isenabled', 'greeting', 'timezone', 'enabledst']

    @classmethod
    def _parse_staff(cls, staff_tree):
        params = dict(
            id=cls._get_int(staff_tree.find('id')),
            firstname=cls._get_string(staff_tree.find('firstname')),
            lastname=cls._get_string(staff_tree.find('lastname')),
            username=cls._get_string(staff_tree.find('username')),
            #password is never present in the response
            staffgroupid=cls._get_int(staff_tree.find('staffgroupid')),
            email=cls._get_string(staff_tree.find('email')),
            designation=cls._get_string(staff_tree.find('designation')),
            mobilenumber=cls._get_string(staff_tree.find('mobilenumber')),
            signature=cls._get_string(staff_tree.find('signature')),
            isenabled=cls._get_boolean(staff_tree.find('isenabled')),
            greeting=cls._get_string(staff_tree.find('greeting')),
            timezone=cls._get_string(staff_tree.find('timezone')),
            enabledst=cls._get_boolean(staff_tree.find('enabledst')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [Staff(api, **cls._parse_staff(staff_tree)) for staff_tree in tree.findall('staff')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('staff')
        if node is None:
            return None
        params = cls._parse_staff(node)
        return Staff(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        self.id = int(tree.find('staff').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id))

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __repr__(self):
        return '<Staff (%s): %s %s (%s)>' % (self.id, self.firstname, self.lastname, self.username)

class StaffGroup(KayakoObject):
    '''
    Kayako StaffGroup API object.
    
    $id$     The numeric identifier of the staff group.
    title    The title of the staff group.
    isadmin  1 or 0, boolean controlling whether or not staff members assigned to this group are Administrators.
    '''

    controller = '/Base/StaffGroup'


    __parameters__ = ['id', 'title', 'isadmin']

    __required_add_parameters__ = ['title', 'isadmin']
    __add_parameters__ = ['title', 'isadmin']

    __required_save_parameters__ = ['title']
    __save_parameters__ = ['title', 'isadmin']


    @classmethod
    def _parse_staff_group(cls, staff_group_tree):
        params = dict(
            id=cls._get_int(staff_group_tree.find('id')),
            title=cls._get_string(staff_group_tree.find('title')),
            isadmin=cls._get_boolean(staff_group_tree.find('isadmin')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [StaffGroup(api, **cls._parse_staff_group(staff_group_tree)) for staff_group_tree in tree.findall('staffgroup')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('staffgroup')
        if node is None:
            return None
        params = cls._parse_staff_group(node)
        return StaffGroup(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        self.id = int(tree.find('staffgroup').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id))

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<StaffGroup (%s): %s>' % (self.id, self.title)






