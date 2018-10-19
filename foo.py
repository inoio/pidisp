import urllib2
import json

from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC # timezone
import pytz
from dateutil.tz import tzlocal
import dateutil.rrule as rrule
utc=pytz.UTC
import caldav
from caldav.elements import dav, cdav

def newClient():
    client = caldav.DAVClient("https://sogo.inoio.de/SOGo/dav/public/loesungsraum/Calendar/personal/")
    principal = client.principal()
    calendars = principal.calendars()
    if len(calendars) > 0:
        calendar = calendars[0]
        print "Using calendar", calendar

        print "Renaming"
        calendar.set_properties([dav.DisplayName("Test calendar"),])
        print calendar.get_properties([dav.DisplayName(),])

        event = calendar.add_event(vcal)
        print "Event", event, "created"

        print "Looking for events in 2010-05"
        results = calendar.date_search(
            datetime(2010, 5, 1), datetime(2010, 6, 1))

        for event in results:
            print "Found", event


def getAll():
    request = urllib2.Request("https://sogo.inoio.de/SOGo/dav/public/loesungsraum/Calendar/personal.ics", headers={"Accept" : "text/txt", "user-agent": "curl"})
    contents = urllib2.urlopen(request).read().decode('utf-8')
    gcal = Calendar.from_ical(contents)
    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            events.append(component)
    events = sorted(events, key=lambda event: event.get('dtstart').dt)
    for event in events:
        print event.get('dtstart').dt.strftime('%m-%d %H:%M')
        #rule = rrule.rrulestr(event.get('rrule'), dtstart=event.get('dtstart'))
        #print rule.after(event.get('dtstart'))
    events = filter(lambda event: event.get('dtstart').dt>utc.localize(datetime.utcnow()), events) 
    result = ""
    for event in events:
        result = result + event.get('dtstart').dt.strftime('%m-%d %H:%M') + " " + event.get('summary') + "\n" + event.get('organizer') + "\n"
    result = result.replace("mailto:", "")
    print result
    return result
    
if __name__ == '__main__':
    print newClient()
