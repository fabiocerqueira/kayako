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

from kayako.tests import KayakoAPITest

class TestKayakoAPI(KayakoAPITest):

    def test_init_without_url(self):
        from kayako.api import KayakoAPI
        from kayako.exception import KayakoInitializationError
        self.assertRaises(KayakoInitializationError, KayakoAPI, None, 'key', 'secret')

    def test_init_without_key(self):
        from kayako.api import KayakoAPI
        from kayako.exception import KayakoInitializationError
        self.assertRaises(KayakoInitializationError, KayakoAPI, 'url', None, 'secret')

    def test_init_without_secret(self):
        from kayako.api import KayakoAPI
        from kayako.exception import KayakoInitializationError
        self.assertRaises(KayakoInitializationError, KayakoAPI, 'url', 'key', None)

    def test__sanitize_paramter_list(self):
        api = self.api
        self.assertEqual(api._sanitize_parameter(['a', 'b', '', None, 'c']), ['a', 'b', 'c'])

    def test__sanitize_paramter_number(self):
        api = self.api
        self.assertEqual(api._sanitize_parameter(123), '123')

    def test__sanitize_paramter_none(self):
        api = self.api
        self.assertEqual(api._sanitize_parameter(None), '')

    def test__post_data_none(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=None)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data=')

    def test__post_data_array(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=['abc', '', None, '123'])
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data[]=abc&data[]=123')

    def test__post_data_empty_array(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=['', None])
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data[]=')

    def test__post_data_date(self):
        import time
        from datetime import datetime
        api = self.api

        date = datetime(2011, 5, 11, 12, 42, 46, 977079)
        timestamp = int(time.mktime(date.timetuple()))

        sanitized = api._sanitize_parameters(date=date)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'date=%s' % timestamp)

    def test__post_data_FOREVER(self):
        from kayako.core.lib import FOREVER
        api = self.api
        sanitized = api._sanitize_parameters(date=FOREVER)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'date=0')

    def test__post_data_int(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=123)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data=123')

    def test__post_data_str(self):
        api = self.api
        sanitized = api._sanitize_parameters(data='abc')
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data=abc')

    def test__post_data_true(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=True)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data=1')

    def test__post_data_false(self):
        api = self.api
        sanitized = api._sanitize_parameters(data=False)
        results = api._post_data(**sanitized)
        self.assertEqual(results, 'data=0')

    def test_signature(self):
        ''' Test the signature generation process '''
        import hmac
        import base64
        import urllib
        import hashlib

        secretkey = "secretkey"
        # Generates a random string of ten digits
        salt = '1234567890'
        # Computes the signature by hashing the salt with the secret key as the key
        signature = hmac.new(secretkey, msg=salt, digestmod=hashlib.sha256).digest()
        # base64 encode...
        encoded_signature = base64.b64encode(signature)
        # urlencode...
        url_encoded_signature = urllib.quote(encoded_signature)
        assert url_encoded_signature == 'VKjt8M54liY6xq1UuhUYH5BFp1RUqHekqytgLPrVEA0%3D'

    def test_get(self):
        r = self.api._request('/Core/Test', 'GET')
        assert r.read()
        assert r.getcode() == 200, r.getcode()
        r = self.api._request('/Core/Test', 'GET', test='just a test')
        assert r.read()
        assert r.getcode() == 200, r.getcode()
        r = self.api._request('/Core/Test/1', 'GET')
        assert r.read()
        assert r.getcode() == 200, r.getcode()
        r = self.api._request('/Core/Test/1', 'GET', test='just a test')
        assert r.read()
        assert r.getcode() == 200, r.getcode()

    def test_post(self):
        r = self.api._request('/Core/Test', 'POST')
        assert r.read()
        assert r.getcode() == 200, r.getcode()

    def test_put(self):
        r = self.api._request('/Core/Test/1', 'PUT', x=234)
        assert r.read()
        assert r.getcode() == 200, r.getcode()

    def test_delete(self):
        r = self.api._request('/Core/Test/1', 'DELETE')
        assert r.read()
        assert r.getcode() == 200, r.getcode()

    def test_get_department(self):
        from kayako.objects import Department
        d = self.api.get(Department, 1)
        self.assertEqual(d.id, 1)

    def test_create_department(self):
        from kayako.core.lib import UnsetParameter
        from kayako.objects import Department
        d = self.api.create(Department)
        self.assertEqual(d.id, UnsetParameter)

    def test_creat_with_kwargs(self):
        from kayako.objects import Department
        d = self.api.create(Department, title='test_dept')
        assert d.title == 'test_dept'

    def test_creat_with_bad_kwargs(self):
        from kayako.objects import Department
        self.assertRaises(TypeError, self.api.create, Department, bad_kwarg='bad_kwarg')




