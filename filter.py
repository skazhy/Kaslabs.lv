import os, cgi, datetime
from dbmodels import *
from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class TimeFilter(webapp.RequestHandler):
    def get(self,request):
        error = False
        events = []
        if len(request) == 8:
            year = int(request[0:4])
            month = int(request[4:6])
            day = int(request[6:8])
            try:
                 date = datetime.date(year,month,day)
            except ValueError:
                 time_format = False
                 error = True
            else:
                 time_format = 'single'

        if len(request) == 17:
            time_format = 'double'
            start_year = int(request[0:4])
            start_month = int(request[4:6])
            start_day = int(request[6:8])
            end_year = int(request[9:13])
            end_month = int(request[13:15])
            end_day = int(request[15:17])
            try:
                 start_date = datetime.date(start_year,start_month,start_day)
                 end_date = datetime.datetime(end_year,end_month,end_day,23,59)
            except ValueError:
                 error = True
                 time_format = False
            else:
                 time_format = 'double'
        if time_format:
            if time_format == 'single':
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1", 
                                   date)
                for event in evs:
                    events.append(event)
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1",
                                   date)
                for event in evs:
                    events.append(event)
                events = sorted(events, key=lambda Event: Event.date)
            
            if time_format == 'double':  
                evs = db.GqlQuery("SELECT * FROM Event WHERE date >= :1 AND date <= :2", 
                                   start_date, end_date)
                for event in evs:
                    events.append(event)
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1 AND end_date <= :2", 
                                   start_date, end_date)
                for event in evs:
                    events.append(event)
                evs = db.GqlQuery("SELECT * FROM Event WHERE date >= :1 AND date >= :2", start_date, end_date)
            events = sorted(events, key=lambda Event: Event.date)
            for event in events:
                if len(event.title) < 15:
                    event.divLen = 240
                else:
                    event.divLen = 16*len(event.title)
                event.date_display = event.date.strftime('%R')
        template_values = {'events':events,'error':error}

        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        self.response.out.write(template.render(path,template_values))
application = webapp.WSGIApplication([('/kad/(.*)',TimeFilter)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
