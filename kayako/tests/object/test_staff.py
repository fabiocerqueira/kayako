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
class TestStaff(KayakoAPITest):

    EMAIL = 'deleteme@example.com'

    def tearDown(self):
        from kayako.objects import Staff
        api = self.api
        test_staff = api.filter(Staff, email=self.EMAIL)
        for staff in test_staff:
            staff.delete()
        super(TestStaff, self).tearDown()

    def test_add_get_nonexistant(self):
        from kayako.objects import Staff
        obj = self.api.get(Staff, '123123')
        assert obj is None

    def test_add_get_bare(self):
        from kayako.objects import Staff
        obj = self.api.create(Staff, firstname='DELETEME', lastname='DELETEME', username='DELETEME', email=self.EMAIL, password='DELETEME', staffgroupid=1)
        obj.add()
        obj2 = self.api.get(Staff, obj.id) # Shouldn't raise errors
        obj.delete()
        assert obj2 is not None

    def test_add_get_full(self):
        from kayako.objects import Staff
        obj = self.api.create(Staff, firstname='DELETEME', lastname='DELETEME', username='DELETEME', email=self.EMAIL, password='DELETEME', staffgroupid=1,
                              designation='TEST', mobilenumber='123-456-7890', signature='TEST', isenabled=False, greeting='Mr.', timezone='MST', enabledst=True)
        obj.add()
        obj2 = self.api.get(Staff, obj.id) # Shouldn't raise errors
        obj.delete()
        assert obj2 is not None

    def test_get_staff(self):
        from kayako.objects import Staff
        d = self.api.get(Staff, 1)
        assert 'Staff ' in str(d)
        self.assertEqual(d.id, 1)

    def test_add_staff_missing_firstname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.lastname = 'test_lastname'
        staff.username = 'test_username'
        staff.password = 'test_password'
        staff.staffgroupid = 1
        staff.email = self.EMAIL

        self.assertRaises(KayakoRequestError, staff.add)

    def test_add_staff_missing_lastname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.firstname = 'test_firstname'
        staff.username = 'test_username'
        staff.password = 'test_password'
        staff.staffgroupid = 1
        staff.email = self.EMAIL

        self.assertRaises(KayakoRequestError, staff.add)

    def test_add_staff_missing_username(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.firstname = 'test_firstname'
        staff.lastname = 'test_lastname'
        staff.password = 'test_password'
        staff.staffgroupid = 1
        staff.email = self.EMAIL

        self.assertRaises(KayakoRequestError, staff.add)

    def test_add_staff_missing_password(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.firstname = 'test_firstname'
        staff.lastname = 'test_lastname'
        staff.username = 'test_username'
        staff.staffgroupid = 1
        staff.email = self.EMAIL

        self.assertRaises(KayakoRequestError, staff.add)

    def test_add_staff_missing_staffgroupid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.firstname = 'test_firstname'
        staff.lastname = 'test_lastname'
        staff.username = 'test_username'
        staff.password = 'test_password'
        staff.email = self.EMAIL

        self.assertRaises(KayakoRequestError, staff.add)

    def test_add_staff_missing_email(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)

        staff.firstname = 'test_firstname'
        staff.lastname = 'test_lastname'
        staff.username = 'test_username'
        staff.password = 'test_password'
        staff.staffgroupid = 1

        self.assertRaises(KayakoRequestError, staff.add)


    def test_get_all(self):
        from kayako.objects import Staff
        result = self.api.get_all(Staff)
        assert len(result)

    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Staff

        staff = self.api.create(Staff)
        staff.firstname = 'DELETEME'
        staff.lastname = 'test_lastname'
        staff.username = 'test_username'
        staff.password = 'test_password'
        staff.staffgroupid = 1
        staff.email = self.EMAIL
        staff.add()
        assert staff.id is not UnsetParameter
        staff.firstname = 'DELETEME2'
        staff.save()
        staff.delete()

        found_error = False
        all_staff = self.api.get_all(Staff)
        for staff in all_staff:
            if staff.email == self.EMAIL:
                staff.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, Staff did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import Staff
        staff = self.api.create(Staff)
        self.assertRaises(KayakoRequestError, staff.delete)

class TestStaffGroup(KayakoAPITest):

    def tearDown(self):
        from kayako.objects import StaffGroup
        all_groups = self.api.get_all(StaffGroup)
        for group in all_groups:
            if group.title == 'DELETEME' or group.title == 'DELETEME2':
                group.delete()
        super(TestStaffGroup, self).tearDown()

    def test_add_get_nonexistant(self):
        from kayako.objects import StaffGroup
        obj = self.api.get(StaffGroup, 123123123)
        assert obj is None

    def test_add_get_bare(self):
        from kayako.objects import StaffGroup
        obj = self.api.create(StaffGroup, title='DELETEME', isadmin=False)
        obj.add()
        obj2 = self.api.get(StaffGroup, obj.id) # Shouldn't raise errors
        obj.delete()
        assert obj2 is not None

    def test_add_get_full(self):
        from kayako.objects import StaffGroup
        obj = self.api.create(StaffGroup, title='DELETEME', isadmin=False)
        obj.add()
        obj2 = self.api.get(StaffGroup, obj.id) # Shouldn't raise errors
        obj.delete()
        assert obj2 is not None

    def test_get_staffgroup(self):
        from kayako.objects import StaffGroup
        d = self.api.get(StaffGroup, 1)
        self.assertEqual(d.id, 1)

    def test_add_staff_missing_title(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import StaffGroup
        staffgroup = self.api.create(StaffGroup)

        staffgroup.isadmin = 0

        self.assertRaises(KayakoRequestError, staffgroup.add)

    def test_add_staff_missing_isadmin(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import StaffGroup
        staffgroup = self.api.create(StaffGroup)

        staffgroup.title = 'test_title'

        self.assertRaises(KayakoRequestError, staffgroup.add)

    def test_get_all(self):
        from kayako.objects import StaffGroup
        result = self.api.get_all(StaffGroup)
        assert len(result)

    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import StaffGroup

        staffgroup = self.api.create(StaffGroup)
        staffgroup.title = 'DELETEME'
        staffgroup.isadmin = 0
        staffgroup.add()
        assert staffgroup.id is not UnsetParameter
        staffgroup.title = 'DELETEME2'
        staffgroup.save()
        staffgroup.delete()

        found_error = False
        all_staff_groups = self.api.get_all(StaffGroup)
        for staffgroup in all_staff_groups:
            if staffgroup.title == 'DELETEME' or staffgroup.title == 'DELETEME2':
                staffgroup.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, StaffGroup did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import StaffGroup
        staffgroup = self.api.create(StaffGroup)
        self.assertRaises(KayakoRequestError, staffgroup.delete)

