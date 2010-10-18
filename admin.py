import os, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
			venues_query = Venue.all().order('title')
			venues = venues_query.fetch(10) 
			template_values = {'venues':venues}
			path = os.path.join(os.path.dirname(__file__),'Templates/base_admin.html')
			self.response.out.write(template.render(path,template_values))

class StoreEvent(webapp.RequestHandler):
	def post(self):
		event = Event()
		event.title = self.request.get('eventTitle')
		event.information = self.request.get('eventInfo')
		
		year = int(self.request.get('eventY'))
		month = int(self.request.get('eventM'))
		day = int(self.request.get('eventD'))
		event.date = datetime.datetime(year,month,day)
		
		if(self.request.get("eventVenue") == "createnew"):
			venue = Venue()
			venue.title = self.request.get('venueTitle')
			venue.put()
		else:
			venue = Venue.get_by_id(int(self.request.get('eventVenue')))
		event.venue = venue
		event.put()
		
		self.redirect('/admin')	

application = webapp.WSGIApplication(
                                     [('/admin', MainHandler),('/admin/save',StoreEvent)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

