from urllib import request
import json
import os
from datetime import datetime, timezone
from untested_helpers import from_datetime_to_string

class EventBriteAPIHelper:
    '''Methods that send/receive data to the eventbrite.com api'''
    def __init__(self):
        self.token = get_api_key()
        print(self.token)

    # This is a helper method used when creating an event
    # You will not need to modify it
    def get_organization_id(self):
        # (gets the "organization id" of our eventbrite.com account)
        url = f'https://www.eventbriteapi.com/v3/users/me/organizations/?token={self.token}'

        request_object = request.Request(url, method="GET")
        request_object.add_header('Content-Type', 'application/json')

        opened_request = request.urlopen(request_object, data=None)
        result = opened_request.read().decode('utf-8')
        parsed = json.loads(result)
       
        print(f"{parsed['organizations'][0]['id']=}")
        return parsed['organizations'][0]['id']

    # This is a working implementation of create event.
    # The title, description, start_time, and end_time should come from your game objects eventually
    def create_event(self, title, description, start_time, end_time):
        organization_id = self.get_organization_id()
        
        # the reason we place the data in a dictionary that looks like this is that
        # the eventbrite api documents the structure here,
        # https://www.eventbrite.com/platform/api#/reference/event/create/create-an-event
        data = {
            "event": {
                "currency": "USD",
                "name": {
                    "html": title
                },
                "description": {
                    "html": description
                },
                "start": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(start_time)
                },
                "end": {
                    "timezone": "UTC",
                    "utc": datetime_to_eventbrite_format(end_time)
                },
            }
        }

        # You will need to do this for any data you send to eventbrite
        data = json.dumps(data)
        data = data.encode()
        
        # This is the url that we will interact with to create an event
        url = f'https://www.eventbriteapi.com/v3/organizations/{organization_id}/events/?token={self.token}'

        # You should prepare your request as follows whenever you send data to eventbrite
        req = request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/json')
        
        # This line is what actually sends data over.
        opened_request = request.urlopen(req, data=data)

        # We check the data sent back to us, so that we can recover the id of the event
        content = opened_request.read().decode('utf-8')
        parsed = json.loads(content)

        # Returns the ID of the event created
        return parsed.get('id')

    # Milestone 4
    def update_event(self, event_id, title, description, start_time, end_time):
        # This method does not need to return anything. It can end as you send the request
        pass

    ########### HELPERS ###############

def get_api_key():
    '''Read the api key from the apikey.txt file'''
    if not os.path.exists('apikey.txt'):
        raise Exception("Please create a file named apikey.txt and paste the Private Token there")
   
    with open('apikey.txt') as f:
        return f.read().strip()


def datetime_to_eventbrite_format(datetime_string):   
    dt = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
    # convert from current timezone to utc
    dt_utc = dt.astimezone(timezone.utc)
    return from_datetime_to_string(dt_utc)

if __name__ == '__main__':
    client = EventBriteAPIHelper()
    result = client.create_event("Test Event", "something", "2024-05-12T02:00:00Z", "2024-05-12T04:00:00Z" )

    print(result)

    # By the end of milestone 4, you should be able to run this and see a new event in your eventbrite page
    # Using the event id stored in result, you should be able to use update_event to modify that same event
    