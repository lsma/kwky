from eventbrite import Eventbrite

from django.conf import settings

def get_events():
    eventbrite = Eventbrite(settings.EVENTBRITE_KEY)
    
    # Get my own User ID
    my_id = eventbrite.get_user()['id']
    
    # Get a raw list of events (includes pagination details)
    return eventbrite.event_search(**{'user.id': my_id})

