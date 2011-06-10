Python API wrapper for Kayako 4.01.240
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

    Create and return a new ``KayakoObject`` of the type given passing in args and kwargs.
    
``api.get_all(Object, *args, **kwargs)``

    *Get all ``KayakoObjects`` of the given type.*
    *In most cases, all items are returned.*
    
    e.x. ::
    
        >>> api.get_all(Department)
        [<Department....>, ....]

    *Special Cases:*
    
        ``api.get_all(User, marker=1, maxitems=1000)``
            Return all ``Users`` from userid ``marker`` with up to ``maxitems`` 
            results (max 1000.)
            
        ``api.get_all(Ticket, departmentid, ticketstatusid=-1, ownerstaffid=-1, userid=-1)``
            Return all ``Tickets`` filtered by the required argument 
            ``departmentid`` and by the optional keyword arguments.
            
        ``api.get_all(TicketAttachment, ticketid)``
            Return all ``TicketAttachments`` for a ``Ticket`` with the given ID.
            
        ``api.get_all(TicketPost, ticketid)``
            Return all ``TicketPosts`` for a ``Ticket`` with the given ID.
            
        ``api.get_all(TicketCustomField, ticketid)``
        	Return all ``TicketCustomFieldGroups`` for a ``Ticket`` with the given ID.
        	Returns a ``list`` of ``TicketCustomFieldGroups``.
        	
        ``api.get_all(TicketCount)``
        	Returns only one object: ``TicketCount`` not a ``list`` of objects.

``api.filter(Object, args=(), kwargs={}, **filter)``

	Gets all ``KayakoObjects`` matching a filter.
        
        e.x. ::

            >>> api.filter(Department, args=(2), module='tickets')
            [<Department module='tickets'...>, <Department module='tickets'...>, ...]
            
``api.first(Object, args=(), kwargs={}, **filter)``

	Returns the first ``KayakoObject`` found matching a given filter.
        
        e.x. ::

            >>> api.filter(Department, args=(2), module='tickets')
            <Department module='tickets'>

``api.get(Object, *args)``

    *Get a ``KayakoObject`` of the given type by ID.*
    
    e.x. ::

        >>> api.get(User, 112359)
        <User (112359)....>
    
    *Special Cases:*
        
        ``api.get(TicketAttachment, ticketid, attachmentid)``
            Return a ``TicketAttachment`` for a ``Ticket`` with the given ``Ticket``
            ID and ``TicketAttachment`` ID.  Getting a specific ``TicketAttachment``
            gets a ``TicketAttachment`` with the actual attachment contents.
        
        ``api.get(TicketPost, ticketid, ticketpostid)``
            Return a ``TicketPost`` for a ticket with the given ``Ticket`` ID and
            ``TicketPost`` ID.
                
        ``api.get(TicketNote, ticketid, ticketnoteid)``
            Return a ``TicketNote`` for a ticket with the given ``Ticket`` ID and
            ``TicketNote`` ID.
            
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
        
**Misc API Calls**

``api.ticket_search(query, ticketid=False, contents=False, author=False, email=False, creatoremail=False, fullname=False, notes=False, usergroup=False, userorganization=False, user=False, tags=False)``
	*Search tickets with a query in the specified fields*
        
**Changes**

	*1.1.4*
	
		- Requires Kayako 4.01.240, use 1.1.3 for Kayako 4.01.204
		- ``TicketNote`` now supports get and delete
		- Added ``api.ticket_search``, see Misc API Calls for details.
		- Refactored ticket module into ticket package. This could cause problems
		  if things were not imported like ``from kayako.objects import X``
		- Added ``TicketCount`` object. Use ``api.get_all(TicketCount)`` to
		  retrieve.

**Quick Reference**

================= ====================================================================== ========================= ======= ======= =====================
Object            Get All                                                                Get                       Add     Save    Delete
================= ====================================================================== ========================= ======= ======= =====================
Department        Yes                                                                    Yes                       Yes     Yes     Yes
Staff             Yes                                                                    Yes                       Yes     Yes     Yes
StaffGroup        Yes                                                                    Yes                       Yes     Yes     Yes
Ticket            departmentid, ticketstatusid= -1, ownerstaffid= -1, userid= -1         Yes                       Yes     Yes     Yes
TicketAttachment  ticketid                                                               ticketid, attachmentid    Yes     No      Yes
TicketCustomField ticketid                                                               No                        No      No      No
TicketCount       Yes                                                                    No                        No      No      No
TicketNote        ticketid                                                               Yes                       Yes     No      Yes
TicketPost        ticketid                                                               ticketid, postid          Yes     No      Yes
TicketPriority    Yes                                                                    Yes                       No      No      No
TicketStatus      Yes                                                                    Yes                       No      No      No
TicketType        Yes                                                                    Yes                       No      No      No
User              marker=1, maxitems=1000                                                Yes                       Yes     Yes     Yes
UserGroup         Yes                                                                    Yes                       Yes     Yes     Yes
UserOrganization  Yes                                                                    Yes                       Yes     Yes     Yes
================= ====================================================================== ========================= ======= ======= =====================