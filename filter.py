import os
import cgi
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from dbmodels import *
from datetime import timedelta

class TimeFilter(webapp.RequestHandler):
    def get(self,request=""):
        if request:
            page = self.render_page(request)
        else:
            page = self.get_main()
        self.response.out.write(page)

    def get_main(self):
        main_page = memcache.get("main_page")
        if main_page is not None:
            return main_page
        else:
            today = datetime.date.today().strftime('%Y%m%d')
            main_page = self.render_page(today)
            memcache.add("main_page",main_page,300)
            return main_page
    
    def render_page(self,request):
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
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1 AND date <= :2",
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
        template_values = {'events':events,'error':error } 
        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        page = template.render(path,template_values)
        return page

application = webapp.WSGIApplication([('/',TimeFilter),('/kad/(.*)',TimeFilter)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
