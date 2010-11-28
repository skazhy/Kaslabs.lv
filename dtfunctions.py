from google.appengine.ext import webapp
import datetime
from dbmodels import *
from datetime import timedelta

def get_events(request):
    error = False
    events = []
    if (len(request) != 17) and (len(request) != 8) and (len(request) != 9):
        error = True

    # Making start date object.
    if not error:
        start_year = int(request[0:4])
        start_month = int(request[4:6])
        start_day = int(request[6:8])
        try:
            start_date = datetime.datetime(start_year,start_month,start_day,0,0)
        except ValueError:
            time_format = False
            error = True
        else:
            if len(request) == 17:
                time_format = 'double'
            if len(request) == 8:
                time_format = 'single'
            if len(request) == 9:
                time_format = 'cont'
    
    # Making end date object.
    if not error:
        if time_format != 'cont':
            try:
                end_year = int(request[9:13])
                end_month = int(request[13:15])
                end_day = int(request[15:17])
            except ValueError:
                end_year = start_year
                end_month = start_month
                end_day = start_day
            try:
                end_date = datetime.datetime(end_year,end_month,end_day,23,59)
            except ValueError:
                error = True
                time_format = False
    
    if not error and time_format:
        if time_format == 'cont':
            evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1", start_date)
            for event in evs:
                events.append(event)
            
            evs = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1",
                               start_date)
            for event in evs:
                events.append(event)
            events = sorted(events, key=lambda Event: Event.date)
        
        else:
            time_diff = end_date - start_date
            length = time_diff.days + 1
            
            # One-day events and multi-day events, that start in the timeframe.
            evs = db.GqlQuery("SELECT * FROM Event WHERE date >= :1 AND date <= :2",
                               start_date, end_date)
            for event in evs:
                events.append(event)
            
            # Multi-day events that end in the timeframe.
            evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1 AND end_date <= :2", 
                               start_date, end_date)
            for event in evs:
                events.append(event)

            # Multi-day events longer than the timeframe.
            evs = db.GqlQuery("SELECT * FROM Event WHERE length > :1 AND length > 1",
                               length)
            for event in evs:
                if event.date < start_date and event.end_date > end_date:
                    events.append(event)

        events = sorted(events, key=lambda Event: Event.date)
        
        for event in events:
            if len(event.title) < 15:
                event.divLen = 240
            else:
                event.divLen = 16*len(event.title)
            event.date_display = event.date.strftime('%R')
    return [events,error]

def parse_timescale(timescale):
    today = datetime.date.today()
    daynumber = int(today.strftime('%u'))
    request = ""
    
    if timescale == "rit":
        tm = today + timedelta(days=1)
        request = tm.strftime('%Y%m%d')
        
    if timescale == "parit":
        atm = today + timedelta(days=2)
        request = atm.strftime('%Y%m%d')
    
    if timescale == "aizparit":
        aatm = today + timedelta(days=3)
        request = aatm.strftime('%Y%m%d')
        
    if timescale == "sonedel":
        week_end = today + timedelta(days=7-daynumber)
        week_start = today - timedelta(days=daynumber-1)
        request = week_start.strftime('%Y%m%d')
        request += '-'
        request += week_end.strftime('%Y%m%d')

    if timescale == "nakamnedel":
        nws = today + timedelta(days=8-daynumber)
        nwe = today + timedelta(days=14-daynumber)
        request = nws.strftime('%Y%m%d')
        request += '-'
        request += nwe.strftime('%Y%m%d')
        
    if timescale == "somenes":
        month_nr = int(today.strftime('%m'))
        year = int(today.strftime('%Y'))
        monthstart = datetime.date(year, month_nr, 1)
        monthend = datetime.date(year, month_nr + 1, 1)
        monthend = monthend - timedelta(days=1)
        request = monthstart.strftime('%Y%m%d')
        request += '-'
        request += monthend.strftime('%Y%m%d')
    return request

def today():
   return datetime.date.today().strftime('%Y%m%d') 
