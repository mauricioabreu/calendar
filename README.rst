Calendar
--------

Example of Google Calendar API usage.

It works like a microservice by serving JSON responses containing information about next events.


Pre-requisites
**************

You need the following tools

	* virtualenv
	* pip


Installing
**********

Create a fresh virtualenv::

	$ virtualenv env

Activate your virtualenv::

	$ source env/bin/activate

Run pip to install all Python dependencies::

	$(env) pip install -r requirements.txt


Running
*******

In your preferred console::

	$(env) python agenda.py my_service_account_email@gmail.com my_pem_file_location 8080


Now you can make requests to this endpoint in order to return events related to the Calendar id passed as parameter.
For example::

	http://localhost:8080/calendar/calendar_id@group.calendar.google.com
