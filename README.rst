Python API wrapper for Kayako 4.01.240
--------------------------------------
    
**Usage:**

Set up the API::

	>>> from kayako import KayakoAPI, 
	>>> API_URL = 'http://example.com/api/index.php'
	>>> API_KEY = 'abc3r4f-alskcv3-kvj4'
	>>> SECRET_KEY = 'vkl239vLKMNvlik42fv9IsflkFJlkckfjs'
	>>> api = KayakoAPI(API_URL, API_KEY, SECRET_KEY)

Add a department::
	
	>>> from kayako import Department
	>>>
	>>> # The following is equivalent to: department = api.create(Department, title='Customer Support Department', type='public', module='tickets'); department.add()
	>>> department = api.create(Department)
	>>> department.title = 'Customer Support Department'
	>>> department.type = 'public'
	>>> department.module = 'tickets'
	>>> department.add()
	>>> department.id
	84
	>>>
	>>> # Cool, we now have a ticket department.
	>>> # Lets say we want to make it private now
	>>>
	>>> department.type = 'private'
	>>> department.save()
	>>>
	>>> # Ok, great.  Lets delete this test object.
	>>>
	>>> department.delete()
	>>> department.id
	UnsetParameter()
	>>>
	>>> # We can re-add it if we want to...
	>>>
	>>> department.save()
	>>> department.id
	85
	>>>
	>>> # Lets see all of our Departments (yours will vary.)
	>>> for dept in api.get_all(Department):
	...     print dept
	... 
	<Department (1): General/tickets>
	<Department (2): Suggest A Store/tickets>
	<Department (3): Report A Bug/tickets>
	<Department (4): Sales/livechat>
	<Department (5): Commissions/livechat>
	<Department (6): Missing Order/livechat>
	<Department (7): Suggest A Feature/tickets>
	<Department (8): Other/livechat>
	<Department (49): Offers/tickets>
	<Department (85): Customer Support Department/tickets>
	>>>
	>>> # Lets see all of our ticket Departments
	>>>
	>>> for dept in api.filter(Department, module='tickets')
	>>>    print dept
	<Department (1): General/tickets>
	<Department (2): Suggest A Store/tickets>
	<Department (3): Report A Bug/tickets>
	<Department (7): Suggest A Feature/tickets>
	<Department (49): Offers/tickets>
	<Department (85): Customer Support Department/tickets>
	>>>
	>>> # We will use this Department in the next example so lets wait to clean up the test data...
	>>> #department.delete()

Add a Staff member::

	>>> from kayako import Staff, StaffGroup
	>>>
	>>> # You can set parameters in the create method.
	>>> staff = api.create(Staff, firstname='John', lastname='Doe', email='foo@example.com', username='explodes', password='easypass332') 
	>>>
	>>> # We need to add a Staff member to a staff group.
	>>> # Lets get the first StaffGroup titled "Administrator"
	>>>
	>>> admin_group = api.first(StaffGroup, title="Administrator")
	>>> staff.staffgroupid = admin_group.id
	>>>
	>>> # And save the new Staff
	>>>
	>>> staff.add()
	>>>
	>>> # We will use this Staff in the next example so lets wait to clean up the test data...
	>>> #staff.delete()
	
Add a User::

	>>> from kayako import User, UserGroup, FOREVER
	>>>
	>>> # What fields can we add to this User?
	>>> User.__add_parameters__
	['fullname', 'usergroupid', 'password', 'email', 'userorganizationid', 'salutation', 'designation', 'phone', 'isenabled', 'userrole', 'timezone', 'enabledst', 'slaplanid', 'slaplanexpiry', 'userexpiry', 'sendwelcomeemail']
	>>>
	>>> # Lets make a new User, but not send out a welcome email.
	>>> # Lets add the User to the "Registered" user group.
	>>> registered = api.first(UserGroup, title='Registered')
	>>> user = api.create(User, fullname="Ang Gary", password="easypass332", email="bar@example.com", usergroupid=registered.id, sendwelcomeemail=False, phone='1-800-555-5555', userexpiry=FOREVER)
	>>> user.add()
	>>>
	>>> # Its that easy.  We will use this user in the next example so lets wait to clean up the test data...
	>>> # user.delete()
	
Add a Ticket and a TicketNote::

	>>> from kayako import TicketStatus, TicketPriority, TicketType, TicketNote, TicketAttachment
	>>>
	>>> # Lets add a "Bug" Ticket to any Ticket Department, with "Open" status and "High" priority for a user. Lets use the user and department from above.
	>>>
	>>> bug = api.first(TicketType, title="Bug")
	>>> open = api.first(TicketStatus, title="Open")
	>>> high = api.first(TicketPriority, title="High")
	>>>
	>>> ticket = api.create(Ticket, tickettypeid=bug.id, ticketstatusid=open.id, ticketpriorityid=high.id, departmentid=department.id, userid=user.id)
	>>> ticket.subject = 'I found a bug and its making me very angry.'
	>>> ticket.fullname = 'Ang Gary'
	>>> ticket.email = 'bar@example.com'
	>>> ticket.contents = 'I am an angry customer you need to make me happy.'
	>>> ticket.add()
	>>>
	>>> # The ticket was added, lets let the customer know that everything will be fine.
	>>>
	>>> print 'Thanks, %s, your inquiry with reference number %s will be answered shortly.' % (ticket.fullname, ticket.displayid)
	Thanks, Ang Gary, your inquiry with reference number TOJ-838-99722 will be answered shortly.'
	>>>
	>>> # Lets add a note to this Ticket, using the Staff member we created above.
	>>>
	>>> note = api.create(TicketNote, ticketid=ticket.id, contents='Customer was hostile. Will pursue anyway as this bug is serious.')
	>>> note.staffid = staff.id # Alternatively, we could do: staff.fullname = 'John Doe'
	>>> note.add()
	>>>
	>>> # Lets say the bug is fixed, we want to let the User know.
	>>>
	>>> post = api.create(TicketPost, ticketid=ticket.id, subject="We fixed it.", contents="We have a patch that will fix the bug.")
	>>> post.add()
	>>>
	>>> # Now lets add an attachment to this TicketPost.
	>>>
	>>> with open('/var/patches/foo.diff', 'rb') as patch:
	...    binary_data = patch.read()
	>>>
	>>> attachment = api.create(TicketAttachment, ticketid=ticket.id, ticketpostid=post.id, filename='foo.diff', filetype='application/octet-stream')
	>>> attachment.set_contents(binary_data) # set_contents encodes data into base 64. get_contents decodes base64 contents into the original data.
	>>> attachment.add()
	>>>
	>>> # Lets clean up finally.
	>>> ticket.delete() # This deletes the attachment, post, and note.
	>>> user.delete()
	>>> staff.delete()
	>>> department.delete()

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
        - The XML is in an unexpected format indicating a possible Kayako version mismatch
        
**Misc API Calls**

``api.ticket_search(query, ticketid=False, contents=False, author=False, email=False, creatoremail=False, fullname=False, notes=False, usergroup=False, userorganization=False, user=False, tags=False)``
	*Search tickets with a query in the specified fields*
        
``api.ticket_search_full(query)``
    *Shorthand for ``api.ticket_search.`` Searches all fields.
        
**Changes**

	*1.1.6*
		- Added ``api.ticket_search_full`` shorthand function for searching all fields in ``api.ticket_search``

    *1.1.5*
    
		- Fix ``Staff.__str__``.
		- ``Ticket.__str__`` includes ``displayid``.
		- ``TicketPost.subject`` is not returned in any responses, so it is not always available, removed it from ``TicketPost.__str__``.

    *1.1.4*
	
		- Requires Kayako 4.01.240, use 1.1.3 for Kayako 4.01.204
		- ``TicketNote`` now supports get and delete
		- Added ``api.ticket_search``, see Misc API Calls for details.
		- Refactored ticket module into ticket package. This could cause problems
		  if things were not imported like ``from kayako.objects import X``
		- Added ``TicketCount`` object. Use ``api.get_all(TicketCount)`` to
		  retrieve.
		- Added ``TicketTimeTrack`` object. ``api.get_all(TicketTimeTrack, ticket.id)`` or
		  ``api.get(TicketTimeTrack, ticket.id, ticket_time_track_id)``
		- Added ``Ticket.timetracks``

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
TicketTimeTrack   ticketid                                                               ticketid, id              Yes     No      Yes
TicketType        Yes                                                                    Yes                       No      No      No
User              marker=1, maxitems=1000                                                Yes                       Yes     Yes     Yes
UserGroup         Yes                                                                    Yes                       Yes     Yes     Yes
UserOrganization  Yes                                                                    Yes                       Yes     Yes     Yes
================= ====================================================================== ========================= ======= ======= =====================