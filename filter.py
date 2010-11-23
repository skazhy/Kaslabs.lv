import os, cgi, datetime
from dbmodels import *
from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache

class TimeFilter(webapp.RequestHandler):
    def get(self,request=""):
        if request == "":
            page = self.getMain()
        else:
            page = self.renderPage(request)
        self.response.out.write(page)

    def getMain(self):
        main_page = memcache.get("main_page")
        if main_page is not None:
            return main_page
        else:
            todays_date = datetime.date.today().strftime('%Y%m%d-')
            main_page = self.renderPage(todays_date)
            memcache.add("main_page",main_page,300)
            return main_page
    
    def renderPage(self,request):
        error = False
        events = []
        
        if (len(request) != 17) and (len(request) != 8) and (len(request) != 9):
            error = True

        # noparsee requestu un noskaidro laika formaatu
        if (not error):
            start_year = int(request[0:4])
            start_month = int(request[4:6])
            start_day = int(request[6:8])
            try:
                start_date = datetime.date(start_year,start_month,start_day)
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

        if (not error):
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
                        
        # savaac pasaakumus no db
        if (not error) and (time_format):
            # pasaakumi no shodienas liidz db galam
            if time_format == 'cont':
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1", start_date)
                for event in evs:
                    events.append(event)
                    evs = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1", start_date)
                for event in evs:
                    events.append(event)
                events = sorted(events, key=lambda Event: Event.date)
            
            # pasaakumi laika apgabalaa (arii vienaa dienaa)
            else:
                evs = db.GqlQuery("SELECT * FROM Event WHERE date >= :1 AND date <= :2", start_date, end_date)
                for event in evs:
                    events.append(event)
                evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1 AND end_date <= :2", start_date, end_date)
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
        template_values = {'events':events,'error':error } 
        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        page = template.render(path,template_values)
        return page

application = webapp.WSGIApplication([('/',TimeFilter),('/kad/(.*)',TimeFilter)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
