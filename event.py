import os, cgi, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class EventPage(webapp.RequestHandler):
    def get(self,ev_id):
        ev_id = int(ev_id)
	event = Event.get_by_id(ev_id)
	event.date_display = event.date.strftime('%-d. %B, %Y')
	event.time_display = event.date.strftime('%R')
        template_values = {'event':event}
	path = os.path.join(os.path.dirname(__file__),'Templates/public-event.html')
        self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication([('/p/(.*)',EventPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

