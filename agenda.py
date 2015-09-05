import datetime

import json


from apiclient import discovery

from bottle import response, route, run

import click

import httplib2

from oauth2client.client import SignedJwtAssertionCredentials


settings = {
    'PORT': 8080
}

# Endpoint this APi will touch
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def _read_pem_file(file_path):
    """
    Read PEM file and return its private key.
    """
    try:
        with open(file_path) as pem_file:
            private_key = pem_file.read()
    except IOError:
        private_key = None
    return private_key


def _do_auth(private_key):
    """
    Do auth using the private key from the PEM file.

    Return auth object ready to make HTTP requests.
    """
    credentials = SignedJwtAssertionCredentials(
        settings['CLIENT_EMAIL'],
        private_key,
        SCOPES
    )
    auth = credentials.authorize(httplib2.Http())
    return auth


def _make_service(auth):
    """
    Create and return a service that uses Google Calendar API calls.
    """
    return discovery.build('calendar', 'v3', auth)


def _get_events(service, calendar_id):
    """
    Get a list of events in JSON format.
    MaxResults is 10 because this code is just for demonstration.
    Ordered by startTime.
    """
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events.get('items', [])
    return events


@route('/calendar/<calendar_id>')
def index(calendar_id, method='GET'):
    private_key = _read_pem_file(settings['FILE_PATH'])
    auth = _do_auth(private_key)
    service = _make_service(auth)
    events = _get_events(service, calendar_id)
    response.content_type = 'application/json'
    return json.dumps(events)


@click.command()
@click.argument('client_email')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--port', default=settings['PORT'],
              help='Port this service will listen to.')
def main(client_email, file_path, port):
    """
    Microservice to return Google Calendar events in JSON format.

    To run this microservice you need to pass:
        * Google Client Email.
        * PEM File Path.
        * Port the service listens on.

    You can use your PEM file and its private key.
    If you have a p12 file you can export it to a PEM file:

        $ openssl pkcs12 -passin pass:notasecret -in private_key.p12 -nocerts -passout pass:notasecret -out key.pem
        $ openssl pkcs8 -nocrypt -in key.pem -passin pass:notasecret -topk8 -out private_key.pem

    """
    settings.update({'CLIENT_EMAIL': client_email,
                     'FILE_PATH': file_path})
    run(host='localhost', port=port)


if __name__ == '__main__':
    main()
