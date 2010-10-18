import os, cgi, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
    def get(self):
		events_query = Event.all().order('-date')
		events = events_query.fetch(10)

		for event in events :
			event.date_display = event.date.strftime('%Y/%m/%d')

		template_values = {'events':events}	
	
		path = os.path.join(os.path.dirname(__file__),'Templates/base_pub.html')
		self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

