import gflags
import httplib2
import logging
import os
import pprint
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run
class Calendar(object):

    service = None

    def __init__(self):
        CLIENT_SECRETS = 'client_secrets.json'
        # Helpful message to display if the CLIENT_SECRETS file is missing.
        MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to download the client_secrets.json file
        and save it at:

           %s

        """ % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)
        FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
          scope=[
              'https://www.googleapis.com/auth/calendar',
              'https://www.googleapis.com/auth/calendar.readonly',
            ],
            message=MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage('sample.dat')
        credentials = storage.get()

        if credentials is None or credentials.invalid:
          credentials = run(FLOW, storage)
    
        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build('calendar', 'v3', http=http)



    def get_events(self, calendar_id, calendar_name):
        events = []
        try:
          page_token = None
          import datetime
          now = datetime.datetime.now()
          time_min = '%s-%s-%sT00:00:00.000-07:00' % (now.year, now.month, now.day)
          while True:
              e = self.service.events().list(
                  calendarId=calendar_id, 
                  pageToken=page_token,
                  timeMin=time_min,
                  singleEvents=True,
                  orderBy='startTime').execute()
              for event in e['items']:
                  pprint.pprint(event)
                  if 'dateTime' in event['start']:
                      dt = event['start'].get('dateTime')
                      sdate = dt[0:10]
                      stime = dt[11:19]
                  else:
                      dt = event['start'].get('date')
                      sdate = dt[0:10]
                      stime = '00:00:00'
                  if 'dateTime' in event['end']:
                      dt = event['end'].get('dateTime')
                      edate = dt[0:10]
                      etime = dt[11:19]
                  else:
                      dt = event['end'].get('date')
                      edate = dt[0:10]
                      etime = '00:00:00'

                  new_event = {
                      'calendar': calendar_name,
                      'name': event['summary'],
                      'description': event.get('description'),
                      'location': event.get('location'),
                      'start': '%s %s' % (sdate, stime),
                      'end': '%s %s' % (edate, etime),
                  }
                  events.append(new_event)

              page_token = e.get('nextPageToken')
              if not page_token:
                  break
        except AccessTokenRefreshError:
          print ("The credentials have been revoked or expired, please re-run"
            "the application to re-authorize")
        return events


    def get_calendars(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print calendar_list_entry['summary']
                print pprint.pprint(calendar_list_entry)
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
