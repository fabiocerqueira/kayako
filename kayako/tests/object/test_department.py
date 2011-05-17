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
from kayako.tests import KayakoAPITest

class TestDepartment(KayakoAPITest):

    def test_get_nonexistant(self):
        from kayako.objects import Department
        d = self.api.get(Department, '123123')
        assert d is None

    def test_add_get_bare(self):
        from kayako.objects import Department
        d = self.api.create(Department, title='test', module='tickets', type='private')
        d.add()
        obj2 = self.api.get(Department, d.id)
        d.delete()
        assert obj2 is not None

    def test_add_get_full(self):
        from kayako.objects import Department
        parent = self.api.first(Department, parentdepartmentid=0)
        d = self.api.create(Department, title='test', module='tickets', type='private',
                            displayorder=15, parentdepartmentid=parent.id, uservisibilitycustom=0, usergroupid=[1, 2])
        d.add()
        obj2 = self.api.get(Department, d.id)
        d.delete()
        assert obj2 is not None

    def test_get_department(self):
        from kayako.objects import Department
        d = self.api.get(Department, 1)
        assert 'Department' in str(d)
        self.assertEqual(d.id, 1)

    def test_add_department_missing_title(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Department
        department = self.api.create(Department)

        department.module = 'tickets'
        department.type = 'public'

        self.assertRaises(KayakoRequestError, department.add)

    def test_add_department_missing_module(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Department
        department = self.api.create(Department)

        department.title = 'test'
        department.type = 'public'

        self.assertRaises(KayakoRequestError, department.add)

    def test_add_department_missing_type(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Department
        department = self.api.create(Department)

        department.title = 'test'
        department.module = 'tickets'

        self.assertRaises(KayakoRequestError, department.add)


    def test_get_all(self):
        from kayako.objects import Department
        result = self.api.get_all(Department)
        assert len(result)

    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department

        department = self.api.create(Department)
        department.title = 'DELETE_ME'
        department.module = 'tickets'
        department.type = 'private'
        department.add()
        assert department.id is not UnsetParameter
        department.title = 'DELETE_ME2'
        department.save()
        department.delete()

        found_error = False
        all_depts = self.api.get_all(Department)
        for dept in all_depts:
            if dept.title == 'DELETE_ME' or dept.title == 'DELETE_ME2':
                dept.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, Departments did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Department
        department = self.api.create(Department)
        self.assertRaises(KayakoRequestError, department.delete)


