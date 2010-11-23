import os, cgi, datetime
from dbmodels import *
from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache

class MainPage(webapp.RequestHandler):
    def get(self):
        main_page = self.getMain()
        self.response.out.write(main_page)
	
    def getMain(self):
        main_page = memcache.get("main_page")
        if main_page is not None:
            return main_page
        else:
            main_page = self.renderMain()
            memcache.add("main_page",main_page,300)
            return main_page
    
    def renderMain(self):
        today = datetime.date.today()
        events = []
        evs = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1", today)
        for event in evs:
            events.append(event)
        evs = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1", today)
        for event in evs:
            events.append(event)
        events = sorted(events, key=lambda Event: Event.date) 
        for event in events:
            if len(event.title) < 15:
                event.divLen = 240
            else:
                event.divLen = 16*len(event.title)
            event.date_display = event.date.strftime('%R')
        template_values = {'events':events}
        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        main_page = template.render(path,template_values)
        return main_page

class TimeMain(webapp.RequestHandler):
    def get(self):
        today = datetime.date.today()
        
        # riit
        tm = today + timedelta(days=1);
        tomorrow=tm.strftime('%Y%m%d')
        
        # pariit
        atm = tm + timedelta(days=1);
        atomorrow=atm.strftime('%Y%m%d')
        
        # aizpariit
        aatm = atm + timedelta(days=1);
        aatomorrow=aatm.strftime('%Y%m%d')
        
        # shonedeelj
        dayn = 7 - int(today.strftime('%u'))
        wn = today + timedelta(days=dayn)
        week = today.strftime('%Y%m%d')
        week += '-'
        week += wn.strftime('%Y%m%d')

        # naakoshnedeelj
        nws = wn + timedelta(days=1)
        nwe = wn + timedelta(days=7)
        nextweek = nws.strftime('%Y%m%d')
        nextweek += '-'
        nextweek += nwe.strftime('%Y%m%d')

        # shomeenes
        calnr = int(today.strftime('%m'))
        calnr += 1
        year = int(today.strftime('%Y'))
        monthend = datetime.date(year,calnr,1)
        monthend = monthend - timedelta(days=1)
        month = today.strftime('%Y%m%d')
        month += '-'
        month += monthend.strftime('%Y%m%d')
        template_values = {
            'tomorrow':tomorrow,
            'atomorrow':atomorrow,
            'aatomorrow':aatomorrow,
            'week':week,
            'nextweek':nextweek,
            'month':month
        }
        path = os.path.join(os.path.dirname(__file__),'Templates/public-timeselect.html')
        self.response.out.write(template.render(path,template_values))



application = webapp.WSGIApplication([('/', MainPage),('/kad',TimeMain)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
