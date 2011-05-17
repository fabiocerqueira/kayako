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
    'User',
    'UserGroup',
    'UserOrganization',
]

class User(KayakoObject):
    '''
    Kayako User API Object.
    
    fullname              The full name of User.
    usergroupid           The User Group ID to assign to this User.
    email                 The Email Address of User, you can send multiple email addresses by using "email[]" as the key
    userorganizationid    The User Organization ID
    salutation            The User Salutation, available options are: Mr., Ms., Mrs., Dr.
    designation           The User Designation/Title
    phone                 The Phone Number
    isenabled             Toggle whether the user is to be enabled/disabled
    userrole              The User Role, available options are: user, manager. Default: user
    timezone              The Time Zone
    enabledst             Enable Daylight Savings?
    slaplanid             The SLA Plan ID to assign to the user
    slaplanexpiry         The SLA Plan Expiry, 0 = never expires
    userexpiry            The User Expiry, 0 = never expires 
    dateline             
    lastvisit
    sendwelcomeemail
    '''

    controller = '/Base/User'

    __parameters__ = [
        'id',
        'fullname',
        'usergroupid',
        'email',
        'password',
        'userorganizationid',
        'salutation',
        'designation',
        'phone',
        'isenabled',
        'userrole',
        'timezone',
        'enabledst',
        'slaplanid',
        'slaplanexpiry',
        'userexpiry',
        'dateline',
        'lastvisit',
        'sendwelcomeemail',
    ]

    __required_add_parameters__ = ['fullname', 'usergroupid', 'password', 'email']
    __add_parameters__ = ['fullname', 'usergroupid', 'password', 'email', 'userorganizationid', 'salutation', 'designation', 'phone', 'isenabled', 'userrole', 'timezone', 'enabledst', 'slaplanid', 'slaplanexpiry', 'userexpiry', 'sendwelcomeemail']

    __required_save_parameters__ = ['fullname']
    __save_parameters__ = ['fullname', 'usergroupid', 'email', 'userorganizationid', 'salutation', 'designation', 'phone', 'isenabled', 'userrole', 'timezone', 'enabledst', 'slaplanid', 'slaplanexpiry', 'userexpiry']

    @classmethod
    def _parse_user(cls, user_tree):
        emails = []
        emails_tree = user_tree.find('emails')
        if emails_tree is not None:
            emails = [cls._get_string(email_node) for email_node in emails_tree.findall('email')]
        else:
            emails = [cls._get_string(email_node) for email_node in user_tree.findall('email')]
        params = dict(
            id=cls._get_int(user_tree.find('id')),
            fullname=cls._get_string(user_tree.find('fullname')),
            usergroupid=cls._get_int(user_tree.find('usergroupid')),
            email=emails,
            userorganizationid=cls._get_int(user_tree.find('userorganizationid'), required=False),
            salutation=cls._get_string(user_tree.find('salutation')),
            designation=cls._get_string(user_tree.find('designation')),
            phone=cls._get_string(user_tree.find('phone')),
            isenabled=cls._get_boolean(user_tree.find('isenabled')),
            userrole=cls._get_string(user_tree.find('userrole')),
            timezone=cls._get_string(user_tree.find('timezone')),
            enabledst=cls._get_boolean(user_tree.find('enabledst')),
            slaplanid=cls._get_int(user_tree.find('slaplanid')),
            slaplanexpiry=cls._get_date(user_tree.find('slaplanexpiry')),
            userexpiry=cls._get_date(user_tree.find('userexpiry')),
            dateline=cls._get_date(user_tree.find('dateline')),
            lastvisit=cls._get_date(user_tree.find('lastvisit')),
        )
        return params

    @classmethod
    def get_all(cls, api, marker=1, maxitems=1000):
        '''
        Returns the users starting at User ID ``marker`` pulling in a maximum
        ``maxitems`` number of Users.
        '''
        response = api._request('%s/%s/%s/' % (cls.controller, marker, maxitems), 'GET')
        tree = etree.parse(response)
        return [User(api, **cls._parse_user(user_tree)) for user_tree in tree.findall('user')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('user')
        if node is None:
            return None
        params = cls._parse_user(node)
        return User(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        self.id = int(tree.find('user').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id))

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<User (%s): %s %s>' % (self.id, self.fullname, self.email)

class UserGroup(KayakoObject):
    '''
    Kayako UserGroup API Object.
    
    title      The title of the user group.
    grouptype  The type of user group ('guest' or 'registered'). 
    ismaster
    '''

    controller = '/Base/UserGroup'

    __parameters__ = [
        'id',
        'title',
        'grouptype',
        'ismaster',
    ]

    __required_add_parameters__ = ['title', 'grouptype']
    __add_parameters__ = ['title', 'grouptype']

    __required_save_parameters__ = ['title']
    __save_parameters__ = ['title']

    @classmethod
    def _parse_user_group(cls, user_group_tree):
        params = dict(
            id=cls._get_int(user_group_tree.find('id')),
            title=cls._get_string(user_group_tree.find('title')),
            grouptype=cls._get_string(user_group_tree.find('grouptype')),
            ismaster=cls._get_boolean(user_group_tree.find('ismaster')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [UserGroup(api, **cls._parse_user_group(user_group_tree)) for user_group_tree in tree.findall('usergroup')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('usergroup')
        if node is None:
            return None
        params = cls._parse_user_group(node)
        return UserGroup(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        self.id = int(tree.find('usergroup').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id))

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<UserGroup (%s): %s (%s)>' % (self.id, self.title, self.grouptype)

class UserOrganization(KayakoObject):
    '''
    Kayako UserOrganization API Object.
    
    name               The name of the user organization.
    organizationtype   The type of user organization ('restricted' or 'shared').
    address      
    city      
    state      
    postalcode      
    country      
    phone      
    fax      
    website      
    slaplanid          The SLA Plan ID to link with this organization
    slaplanexpiry      The UNIX timestamp by which to ignore the SLA Plan, 0 = never expires
    '''

    controller = '/Base/UserOrganization'

    __parameters__ = [
        'id',
        'name',
        'organizationtype',
        'address',
        'city',
        'state',
        'postalcode',
        'country',
        'phone',
        'fax',
        'website',
        'slaplanid',
        'slaplanexpiry',
        'dateline',
        'lastupdate',
    ]

    __required_add_parameters__ = ['name', 'organizationtype']
    __add_parameters__ = ['name', 'organizationtype', 'address', 'city', 'state', 'postalcode', 'country', 'phone', 'fax', 'website', 'slaplanid', 'slaplanexpiry']

    __required_save_parameters__ = ['name']
    __save_parameters__ = ['name', 'organizationtype', 'address', 'city', 'state', 'postalcode', 'country', 'phone', 'fax', 'website', 'slaplanid', 'slaplanexpiry']

    @classmethod
    def _parse_user_organization(cls, user_organization_tree):
        params = dict(
            id=cls._get_int(user_organization_tree.find('id')),
            name=cls._get_string(user_organization_tree.find('name')),
            organizationtype=cls._get_string(user_organization_tree.find('organizationtype')),
            address=cls._get_string(user_organization_tree.find('address')),
            city=cls._get_string(user_organization_tree.find('city')),
            state=cls._get_string(user_organization_tree.find('state')),
            postalcode=cls._get_string(user_organization_tree.find('postalcode')),
            country=cls._get_string(user_organization_tree.find('country')),
            phone=cls._get_string(user_organization_tree.find('phone')),
            fax=cls._get_string(user_organization_tree.find('fax')),
            website=cls._get_string(user_organization_tree.find('website')),
            dateline=cls._get_date(user_organization_tree.find('dateline')),
            lastupdate=cls._get_date(user_organization_tree.find('lastupdate')),
            slaplanid=cls._get_int(user_organization_tree.find('slaplanid')),
            slaplanexpiry=cls._get_date(user_organization_tree.find('slaplanexpiry')),
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [UserOrganization(api, **cls._parse_user_organization(user_organization_tree)) for user_organization_tree in tree.findall('userorganization')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        node = tree.find('userorganization')
        if node is None:
            return node
        params = cls._parse_user_organization(node)
        return UserOrganization(api, **params)

    def add(self):
        response = self._add(self.controller)
        tree = etree.parse(response)
        self.id = int(tree.find('userorganization').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id))

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<UserOrganization (%s): %s>' % (self.id, self.name)






