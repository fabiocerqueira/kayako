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

import base64
import hashlib
import hmac
import random
import urllib
import urllib2
import time
from datetime import datetime

from kayako.exception import KayakoRequestError, KayakoResponseError, KayakoInitializationError
from kayako.core.lib import FOREVER

class KayakoAPI:
    ''' 
    Python API wrapper for Kayako 4.01.204
    --------------------------------------
        
    **Usage:**
    
    ::
    
        >>> from kayako import KayakoAPI, User, Ticket, Department, UnsetParameter
        >>> api = KayakoAPI('http://kayako.foo.com/api/index.php', 's8v092-2lksd-9cso-c2', 'somesecret')
        >>> departments = api.get_all(Department)
        >>> for department in departments:
        >>>     # Print every ticket in every department
        >>>     tickets = api.get_all(Ticket, department.id)
        >>>     for ticket in tickets:
        >>>         print department, ticket
        <Department...> <Ticket...>
        <Department...> <Ticket...>
        <Department...> <Ticket...>
        
    **Add an object**
    
    ::
    
        department = api.create(Department)
        department.title = 'Food Department' # Department author was hungry
        department.module = 'tickets'
        department.type = 'private'
        assert department.id is UnsetParameter
        department.add()
        assert department.id is not UnsetParameter
        department.title = 'Foo Department' # 'Food' was supposed to be 'Foo'
        department.save()
        department.delete()
    
    **API Factory Methods:**
    
    ``api.create(Object, *args, **kwargs)``
    
        Create and return a new KayakoObject of the type given passing in args and kwargs.
        
    ``api.get_all(Object, *args, **kwargs)``
    
        *Get all Kayako Objects of the given type.*
        *In most cases, all items are returned.*
        
        e.x. ::
        
            >>> api.get_all(Department)
            [<Department....>, ....]
    
        *Special Cases:*
        
            ``api.get_all(User, marker=1, maxitems=1000)``
                Return all Users from userid ``marker`` with up to ``maxitems`` 
                results (max 1000.)
                
            ``api.get_all(Ticket, departmentid, ticketstatusid=-1, ownerstaffid=-1, userid=-1)``
                Return all Tickets filtered by the required argument 
                ``departmentid`` and by the optional keyword arguments.
                
            ``api.get_all(TicketAttachment, ticketid)``
                Return all TicketAttachments for a Ticket with the given ID.
                
            ``api.get_all(TicketPost, ticketid)``
                Return all TicketPosts for a Ticket with the given ID.
    
    ``api.filter(Object, args=(), kwargs={}, **filter)``
    
        Gets all KayakoObjects matching a filter.
            
            e.x.
                >>> api.filter(Department, args=(2), module='tickets')
                [<Department module='tickets'...>, <Department module='tickets'...>, ...]
                
    ``api.first(Object, args=(), kwargs={}, **filter)``
    
        Returns the first KayakoObject found matching a given filter.
            
            e.x.
                >>> api.filter(Department, args=(2), module='tickets')
                <Department module='tickets'>
    
    ``api.get(Object, *args)``
    
        *Get a Kayako Object of the given type by ID.*
        
        e.x. ::
        
            >>> api.get(User, 112359)
            <User (112359)....>
        
        *Special Cases:*
            
            ``api.get(TicketAttachment, ticketid, attachmentid)``
                Return a ``TicketAttachment`` for a ``Ticket`` with the given Ticket
                ID and TicketAttachment ID.  Getting a specific ``TicketAttachment``
                gets a ``TicketAttachment`` with the actual attachment contents.
            
            ``api.get(TicketPost, ticketid, ticketpostid)``
                Return a ``TicketPost`` for a ticket with the given Ticket ID and
                TicketPost ID.
                
    **Object persistence methods**
    
    ``kayakoobject.add()``
        *Adds the instance to Kayako.*
    ``kayakoobject.save()``
        *Saves an existing object the instance to Kayako.*
    ``kayakoobject.delete()``
        *Removes the instance from Kayako*
        
    These methods can raise exceptions:
    
        Raises ``KayakoRequestError`` if one of the following is true:
            - The action is not available for the object
            - A required object parameter is UnsetParameter or None (add/save)
            - The API URL cannot be reached
            
        Raises ``KayakoResponseError`` if one of the following is true:
            - There is an error with the request (not HTTP 200 Ok)
            - The XML is in an unexpected format indicating a possible Kayako version mismatch (expects 4.01.204)
        
    **Quick Reference**
    
    ================= ====================================================================== ========================= ======= ======= =====================
    Object            Get All                                                                Get                       Add     Save    Delete
    ================= ====================================================================== ========================= ======= ======= =====================
    Department        Yes                                                                    Yes                       Yes     Yes     Yes
    Staff             Yes                                                                    Yes                       Yes     Yes     Yes
    StaffGroup        Yes                                                                    Yes                       Yes     Yes     Yes
    Ticket            departmentid, ticketstatusid= -1, ownerstaffid= -1, userid= -1         Yes                       Yes     Yes     Yes
    TicketAttachment  ticketid                                                               ticketid, attachmentid    Yes     No      Yes
    TicketNote        ticketid                                                               No                        Yes     No      No (delete ticket)
    TicketPost        ticketid                                                               ticketid, postid          Yes     No      Yes
    TicketPriority    Yes                                                                    Yes                       No      No      No
    TicketStatus      Yes                                                                    Yes                       No      No      No
    TicketType        Yes                                                                    Yes                       No      No      No
    User              marker=1, maxitems=1000                                                Yes                       Yes     Yes     Yes
    UserGroup         Yes                                                                    Yes                       Yes     Yes     Yes
    UserOrganization  Yes                                                                    Yes                       Yes     Yes     Yes
    ================= ====================================================================== ========================= ======= ======= =====================
    
    '''

    def __init__(self, api_url, api_key, secret_key):
        ''' 
        Creates a new wrapper that will make requests to the given URL using
        the authentication provided.
        '''

        if not api_url:
            raise KayakoInitializationError('API URL not specified.')
        self.api_url = api_url

        if not api_key:
            raise KayakoInitializationError('API Key not specified.')
        self.secret_key = secret_key

        if not secret_key:
            raise KayakoInitializationError('Secret Key not specified.')
        self.api_key = api_key

    ## { Communication Layer

    def _sanitize_parameter(self, parameter):
        '''
        Sanitize a specific object.
        
        - Convert None types to empty strings
        - Convert FOREVER to '0'
        - Convert lists/tuples into sanitized lists
        - Convert objects to strings
        '''

        if parameter is None:
            return ''
        elif parameter is FOREVER:
            return '0'
        elif parameter is True:
            return '1'
        elif parameter is False:
            return '0'
        elif isinstance(parameter, datetime):
            return str(int(time.mktime(parameter.timetuple())))
        elif isinstance(parameter, (list, tuple, set)):
            return [self._sanitize_parameter(item) for item in parameter if item not in ['', None]]
        else:
            return str(parameter)

    def _sanitize_parameters(self, **parameters):
        '''
        Sanitize a dictionary of parameters for a request.
        '''
        result = dict()
        for key, value in parameters.iteritems():
            result[key] = self._sanitize_parameter(value)
        return result

    def _post_data(self, **parameters):
        '''
        Turns parameters into application/x-www-form-urlencoded format.
        '''
        data = None
        first = True
        for key, value in parameters.iteritems():
            if isinstance(value, list):
                if len(value):
                    for sub_value in value:
                        if first:
                            data = '%s[]=%s' % (key, urllib2.quote(sub_value))
                            first = False
                        else:
                            data = '%s&%s[]=%s' % (data, key, urllib2.quote(sub_value))
                else:
                    if first:
                        data = '%s[]=' % key
                        first = False
                    else:
                        data = '%s&%s[]=' % (data, key)
            elif first:
                data = '%s=%s' % (key, urllib2.quote(value))
                first = False
            else:
                data = '%s&%s=%s' % (data, key, urllib2.quote(value))
        return data

    def _generate_signature(self):
        '''
        Generates random salt and an encoded signature using SHA256.
        '''
        # Generate random 10 digit number
        salt = str(random.getrandbits(32))
        # Use HMAC to encrypt the secret key using the salt with SHA256
        encrypted_signature = hmac.new(self.secret_key, msg=salt, digestmod=hashlib.sha256).digest()
        # Encode the bytes into base 64
        b64_encoded_signature = base64.b64encode(encrypted_signature)
        return salt, b64_encoded_signature

    def _request(self, controller, method, **parameters):
        '''
        Get a response from the specified controller using the given parameters.
        '''
        salt, b64signature = self._generate_signature()

        if method == 'GET':
            url = '%s?e=%s&apikey=%s&salt=%s&signature=%s' % (self.api_url, urllib.quote(controller), urllib.quote(self.api_key), salt, urllib.quote(b64signature))
            # Append additional query args if necessary
            data = self._post_data(**self._sanitize_parameters(**parameters)) if parameters else None
            if data:
                url = '%s&%s' % (url, data)
            request = urllib2.Request(url)
        elif method == 'POST' or method == 'PUT':
            url = '%s?e=%s' % (self.api_url, urllib.quote(controller))
            # Auth parameters go in the body for these methods
            parameters['apikey'] = self.api_key
            parameters['salt'] = salt
            parameters['signature'] = b64signature
            data = self._post_data(**self._sanitize_parameters(**parameters))
            request = urllib2.Request(url, data=data, headers={'Content-length' : len(data) if data else 0})
            request.get_method = lambda: method
        elif method == 'DELETE': # DELETE
            url = '%s?e=%s&apikey=%s&salt=%s&signature=%s' % (self.api_url, urllib.quote(controller), urllib.quote(self.api_key), salt, urllib.quote(b64signature))
            data = self._post_data(**self._sanitize_parameters(**parameters))
            request = urllib2.Request(url, data=data, headers={'Content-length' : len(data) if data else 0})
            request.get_method = lambda: method
        else:
            raise KayakoRequestError('Invalid request method: %s not supported.' % method)

#        print 'REQUEST:'
#        print method
#        print 'URL:'
#        print url.replace('&', '\n&') if url else 'None'
#        print 'DATA:'
#        print data.replace('&', '\n&') if data else 'None'
#        print '------'

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
#            print error.read()
            raise KayakoResponseError(error)
        except urllib2.URLError, error:
#            print error.read()
            raise KayakoRequestError(error)
        return response

    ## { Persistence Layer

    def create(self, object, *args, **kwargs):
        '''
        Create a new KayakoObject of the type given, passing in args and kwargs.
        '''
        return object(self, *args, **kwargs)

    def get_all(self, object, *args, **kwargs):
        '''
        Get all Kayako Objects of the given type.
        By default, all items are returned. 
        
        e.x.
            >>> api.get_all(Department)
            [<Department....>, ....]
    
        Special Cases:
        
            api.get_all(User, marker=1, maxitems=1000)
                Return all Users from userid ``marker`` with up to ``maxitems``
                results (max 1000.)
                
            api.get_all(Ticket, departmentid, ticketstatusid= -1, 
              ownerstaffid= -1, userid= -1)
                Return all Tickets filtered by the required argument
                ``departmentid`` and by the optional keyword arguments.
                
            api.get_all(TicketAttachment, ticketid)
                Return all TicketAttachments for a Ticket with the given ID.
                
            api.get_all(TicketPost, ticketid)
                Return all TicketPosts for a Ticket with the given ID.
                
        '''
        return object.get_all(self, *args, **kwargs)

    def _match_filter(self, object, **filter):
        '''
        Returns whether or not every given attribute of an object is equal
        to the given values.
        '''
        for key, value in filter.iteritems():
            attr = getattr(object, key)
            if isinstance(attr, list):
                if value not in attr:
                    return False
            elif attr != value:
                return False
        return True

    def filter(self, object, args=(), kwargs={}, **filter):
        '''
        Gets all KayakoObjects matching a filter.
        
        e.x.
            >>> api.filter(Department, args=(2), module='tickets')
            [<Department module='tickets'...>, <Department module='tickets'...>, ...]
        '''
        objects = self.get_all(object, *args, **kwargs)
        results = []
        for result in objects:
            if self._match_filter(result, **filter):
                results.append(result)
        return results

    def first(self, object, args=(), kwargs={}, **filter):
        '''
        Returns the first KayakoObject found matching a given filter.
        
        e.x.
            >>> api.filter(Department, args=(2), module='tickets')
            <Department module='tickets'>
        '''
        objects = self.get_all(object, *args, **kwargs)
        for result in objects:
            if self._match_filter(result, **filter):
                return result

    def get(self, object, *args):
        '''
        Get a Kayako Object of the given type by ID.
        
        e.x.
            api.get(User, 112359)
            >>> <User....>
        
        Special Cases:
            
            api.get(TicketAttachment, ticketid, attachmentid)
                Return a TicketAttachment for a ticket with the given Ticket ID
                and TicketAttachment ID.  Getting a specific TicketAttachment
                gets a TicketAttachment with the actual attachment contents.
            
            api.get(TicketPost, ticketid, ticketpostid)
                Return a TicketPost for a ticket with the given Ticket ID and
                TicketPost ID.
        
        '''


        return object.get(self, *args)

    def __str__(self):
        return '<KayakoAPI: %s>' % self.api_url

    def __repr__(self):
        return 'KayakoAPI(%s, "some_key", "some_secret")' % (self.api_url)
