# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------
'''
Created on May 5, 2011

@author: evan
'''

from lxml import etree

from kayako.core.object import KayakoObject

__all__ = [
    'Department',
]

class Department(KayakoObject):
    '''
    Kayako Department API Object.
    
    title                 The title of the department.
    module                The module the department should be associated with ('tickets' or 'livechat').
    type                  The accessibility level of the department ('public' or 'private').
    displayorder          A positive integer that the helpdesk will use to sort departments when displaying them (ascending).
    parentdepartmentid    A positive integer of the parent department for this department.
    uservisibilitycustom  1 or 0 boolean that controls whether or not to restrict visibility of this department to particular user groups (see usergroupid[]).
    usergroupid[]         An array of positive integers identifying the user groups to be assigned to this department. 
    '''

    __request_parameters__ = ['id', 'title', 'type', 'module', 'displayorder', 'parentdepartmentid', 'uservisibilitycustom', 'usergroups']

    controller = '/Base/Department'

    @classmethod
    def _parse_department(cls, department_tree):
        usergroups = []
        usergroups_node = department_tree.find('usergroups')
        if usergroups_node is not None:
            for id_node in usergroups_node.findall('id'):
                id = cls._get_int(id_node)
                usergroups.append(id)

        params = dict(
            id=cls._get_int(department_tree.find('id')),
            title=cls._get_string(department_tree.find('title')),
            type=cls._get_string(department_tree.find('type')),
            module=cls._get_string(department_tree.find('module')),
            displayorder=cls._get_int(department_tree.find('displayorder')),
            parentdepartmentid=cls._get_int(department_tree.find('parentdepartmentid'), required=False),
            uservisibilitycustom=cls._get_boolean(department_tree.find('uservisibilitycustom')),
            usergroups=usergroups,
        )
        return params

    @classmethod
    def get_all(cls, api):
        response = api._request(cls.controller, 'GET')
        tree = etree.parse(response)
        return [Department(api, **cls._parse_department(department_tree)) for department_tree in tree.findall('department')]

    @classmethod
    def get(cls, api, id):
        response = api._request('%s/%s/' % (cls.controller, id), 'GET')
        tree = etree.parse(response)
        params = cls._parse_department(tree.find('department'))
        return Department(api, **params)

    def add(self):
        response = self._add(self.controller, 'title', 'module', 'type')
        tree = etree.parse(response)
        self.id = int(tree.find('department').find('id').text)

    def save(self):
        self._save('%s/%s/' % (self.controller, self.id), 'title')

    def delete(self):
        self._delete('%s/%s/' % (self.controller, self.id))

    def __str__(self):
        return '<Department (%s): %s/%s>' % (self.id, self.title, self.module)






