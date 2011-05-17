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

class TestUser(KayakoAPITest):

    def test_get_nonexistant(self):
        from kayako.objects import User
        obj = self.api.get(User, 'abc123')
        assert obj is None

    def test_add_get_bare(self):
        from kayako.objects import User
        user = self.api.create(User, fullname='DELETE ME', usergroupid=2, password='deleteme', email='deleteme@example.com')
        user.add()
        user2 = self.api.get(User, user.id)
        user.delete()
        assert user2 is not None

    def test_add_get_full(self):
        from datetime import datetime
        from kayako.objects import User
        user = self.api.create(User, fullname='DELETE ME', usergroupid=2, password='deleteme', email='deleteme@example.com',
                               userorganizationid=1, salutation='Mr.', designation='CEO', phone='123-456-7890', isenabled=False, userrole='user', timezone='MST', enabledst=True, slaplanid=1, slaplanexpiry=datetime.now(), sendwelcomeemail=False)
        user.add()
        user2 = self.api.get(User, user.id)
        user.delete()
        assert user2 is not None

    def test_get_all(self):
        from kayako.objects import User
        result = self.api.get_all(User)
        assert len(result)

    def test_get_all_with_kwargs(self):
        from kayako.objects import User
        result = self.api.get_all(User, marker=200, maxitems=50)
        assert isinstance(result, list)

    def test_get_user(self):
        from kayako.objects import User
        user = self.api.get(User, 1)

        assert 'User ' in str(user)

        self.assertEqual(user.id, 1)

    def test_add_user_missing_fullname(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import User
        user = self.api.create(User)

        user.usergroupid = -1
        user.password = 'test_password'
        user.email = 'test_email@example.com'
        user.dateline = 4234
        user.phone = '56465464'

        self.assertRaises(KayakoRequestError, user.add)

    def test_add_user_missing_usergroupid(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import User
        user = self.api.create(User)

        user.fullname = 'test_user'
        user.password = 'test_password'
        user.email = 'test_email@example.com'
        user.dateline = 4234
        user.phone = '56465464'

        self.assertRaises(KayakoRequestError, user.add)

    def test_add_user_missing_password(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import User
        user = self.api.create(User)

        user.fullname = 'test_user'
        user.usergroupid = -1
        user.email = 'test_email@example.com'
        user.dateline = 4234
        user.phone = '56465464'

        self.assertRaises(KayakoRequestError, user.add)

    def test_add_user_missing_email(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import User
        user = self.api.create(User)

        user.fullname = 'test_user'
        user.usergroupid = -1
        user.password = 'test_password'
        user.dateline = 4234
        user.phone = '56465464'

        self.assertRaises(KayakoRequestError, user.add)

    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import User

        user = self.api.create(User)
        user.fullname = 'DELETE_ME'
        user.usergroupid = 2
        user.password = 'test_password'
        user.email = 'test@example.com'
        user.add()
        assert user.id is not UnsetParameter
        user.fullname = 'DELETE_ME2'
        user.save()
        user.delete()

        found_error = False
        all = self.api.get_all(User)
        for obj in all:
            if obj.fullname == 'DELETE_ME' or obj.fullname == 'DELETE_ME2':
                obj.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, Users did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import User
        user = self.api.create(User)
        self.assertRaises(KayakoRequestError, user.delete)

class TestUserGroup(KayakoAPITest):

    def test_get_nonexistant(self):
        from kayako.objects import UserGroup
        obj = self.api.get(UserGroup, '12345')
        print obj
        assert obj is None

    def test_add_get(self):
        from kayako.objects import UserGroup
        obj = self.api.create(UserGroup, title='DELETE ME', grouptype='registered')
        obj.add()
        obj2 = self.api.get(UserGroup, obj.id)
        obj.delete()
        assert obj2 is not None

    def test_get_all(self):
        from kayako.objects import UserGroup
        result = self.api.get_all(UserGroup)
        assert len(result)

    def test_get(self):
        from kayako.objects import UserGroup
        usergroup = self.api.get(UserGroup, 1)
        self.assertEqual(usergroup.id, 1)

    def test_add_missing_title(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserGroup
        usergroup = self.api.create(UserGroup)

        usergroup.grouptype = 'registered'

        self.assertRaises(KayakoRequestError, usergroup.add)

    def test_add_missing_grouptype(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserGroup
        usergroup = self.api.create(UserGroup)

        usergroup.title = 'test_usergroup'

        self.assertRaises(KayakoRequestError, usergroup.add)


    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import UserGroup

        usergroup = self.api.create(UserGroup)
        usergroup.title = 'DELETE_ME'
        usergroup.grouptype = 'registered'
        usergroup.add()
        assert usergroup.id is not UnsetParameter
        usergroup.title = 'DELETE_ME2'
        usergroup.save()
        usergroup.delete()

        found_error = False
        all = self.api.get_all(UserGroup)
        for obj in all:
            if obj.title == 'DELETE_ME' or obj.title == 'DELETE_ME2':
                obj.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, UserGroups did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserGroup
        usergroup = self.api.create(UserGroup)
        self.assertRaises(KayakoRequestError, usergroup.delete)

class TestUserOrganization(KayakoAPITest):

    def test_get_nonexistant(self):
        from kayako.objects import UserOrganization
        obj = self.api.get(UserOrganization, '123123')
        assert obj is None

    def test_add_get_bare(self):
        from kayako.objects import UserOrganization
        obj = self.api.create(UserOrganization, name='DELETE ME', organizationtype='restricted')
        obj.add()
        obj2 = self.api.get(UserOrganization, obj.id)
        obj.delete()
        assert obj2 is not None

    def test_add_get_full(self):
        from datetime import datetime
        from kayako.objects import UserOrganization
        obj = self.api.create(UserOrganization, name='DELETE ME', organizationtype='restricted',
                              address='23423 E', city='Salt Lake City', state='Utah', postalcode=84121, country='USA', phone='123-456-7890', fax='098-765-4321', website='http://example.com', slaplanid=1, slaplanexpiry=datetime.now())
        obj.add()
        obj2 = self.api.get(UserOrganization, obj.id)
        obj.delete()
        assert obj2 is not None

    def test_get_all(self):
        from kayako.objects import UserOrganization
        result = self.api.get_all(UserOrganization)
        assert len(result)

    def test_get(self):
        from kayako.objects import UserOrganization
        userorg = self.api.get(UserOrganization, 1)
        self.assertEqual(userorg.id, 1)

    def test_add_missing_name(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserOrganization
        userorg = self.api.create(UserOrganization)

        userorg.organizationtype = 'restricted'

        self.assertRaises(KayakoRequestError, userorg.add)

    def test_add_missing_organizationtype(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserOrganization
        userorg = self.api.create(UserOrganization)

        userorg.name = 'test_user_org'

        self.assertRaises(KayakoRequestError, userorg.add)

    def test_add_save_delete(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import UserOrganization

        userorg = self.api.create(UserOrganization)
        userorg.name = 'DELETE_ME'
        userorg.organizationtype = 'restricted'
        userorg.add()
        assert userorg.id is not UnsetParameter
        userorg.name = 'DELETE_ME2'
        userorg.save()
        userorg.delete()

        found_error = False
        all = self.api.get_all(UserOrganization)
        for obj in all:
            if obj.name == 'DELETE_ME' or obj.name == 'DELETE_ME2':
                obj.delete()
                found_error = True
        if found_error:
            assert False, 'Found an error, UserOrganizations did not delete correctly.'

    def test_delete_unadded(self):
        from kayako.exception import KayakoRequestError
        from kayako.objects import UserOrganization
        userorg = self.api.create(UserOrganization)
        self.assertRaises(KayakoRequestError, userorg.delete)

