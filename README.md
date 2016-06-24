Address Book
============

**Author:** [John Lindsay Orr](http://johnorr.us)

**License:** [LICENSE.txt](./LICENSE.txt)

This project is a toy address book app which demos use of the
[Django framework](https://www.djangoproject.com/) for object modelling and REST
service, together with Google's [Polymer](https://www.polymer-project.org/1.0/)
for a rich componentized AJAX client.


Quick start
-----------
```
./scripts/setup.sh       # Install dependencies. Only needs to be run once
./scripts/runserver.sh   # Start the server. Connect to `http://localhost:8000/addressbook`
./scripts/test.sh        # (Optional) Run the tests
```

Detailed instructions given below.


Setup
-----

0. Prerequisites: You will need Python 2.7, pip, virtualenv, and npm already
   installed before you begin.

1. Set up a virtualenv sandbox and switch into it:
   ```
   virtualenv venv
   . ./venv/bin/activate
   ```
   Remember to reactivate the virtualenv each time you use the project.

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   npm install
   ```

3. Initialize the database:
   ```
   python manage.py migrate
   ```


Run the app
-----------

Start the app with the command:
```
python manage.py runserver <port_number>
```
Stop the app with a Ctl-C.

Connect to the app with `http://localhost:8000/addressbook`


Tests
-----

Run the server tests with:
```
python manage.py test
```

Run the client tests with:
```
npm test
```

Expect to see a faiurly long list of warnings for unimplemented tests.


Finding your way around
-----------------------

The interesting files in the app are as shown:
```
  + addressbook/             The address book app
    + models.py              The definition of the database ORL
    + tests.py               Tests for the Django service
    + urls.py                URL binding for the REST service
    + views.py               The logic for the REST handlers
    + static/
      + app/
        + addressbook.html   The root Polymer componentfor the app
        + *.html             Other Polymer components used in the client app
        + test.html          The client app tests
    + templates/
      + index.html           The root HTML page of the app
  + project/                 Django boilerplate for the project
  + db.sqlite3               The SQLite3 database for the app
```
