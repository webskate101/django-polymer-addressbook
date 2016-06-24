Technologies
------------

1. SQLite db
2. Django webserver, service layer, and ORM
3. Polymer client app


TODO
----

- P0: [DONE] User login, actor in session etc
- P0: [DONE] Tie the model entities to the actor in session id
- P1: Factor individual ajax calls into a service object
  + Current design is very chatty - does many more ajax calls than necessary.
  + Needs a client-side data cachelayer like Relay.
- P1: Client-side form validation
- P1: Server-side form validation
- P1: [DONE] XSRF protection
- P1: [DONE] Deleting people needs confirm step
- P1: Paging list views
- P2: [DONE] Empty list cases
- P2: Ajax spinner
- P2: Amimated transitions
- P2: Refactor person-list.html and organization-list.html into single component
- P2: [DONE] Factor display of contact details into single component
- P2: Factor editor of contact details into single component
- P2: Add tooltips to buttons
- P2: Flow to members at the time an org is created
- P2: Introduce facade layer between the handlers and the data model
- P2: Server-side memcache layer


USEFUL COMMANDS
---------------

```shell
python manage.py makemigrations  # Makes new migrations files
python manage.py migrate  # Set up SQLite database
python manage.py createsuperuser
python manage.py runserver
python manage.py test  # Run service tests
npm test  # Run client tests
```


REST Service
------------

```
/person              POST
/person/<id>         GET, PUT, DELETE
/person/all          GET
/organization        POST
/organization/<id>   GET, PUT, DELETE
/organization/all    GET
/organization/<organization_id>/member/<person_id>    DELETE, PUT
```
