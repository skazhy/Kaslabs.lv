import os, cgi, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
    def get(self,page=1):
        today = datetime.date.today()
        events = []
        m_ev = db.GqlQuery("SELECT * FROM Event WHERE end_date >= :1", today)
        for event in m_ev:
            events.append(event)
        s_ev = db.GqlQuery("SELECT * FROM Event WHERE end_date = NULL AND date >= :1", today)
        for event in s_ev:
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
        self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication([('/', MainPage),('/page/(.*)',MainPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
