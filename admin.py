import os, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class AddEvent(webapp.RequestHandler):
    def get(self):
		venues_query = Venue.all().order('title')
		venues = venues_query.fetch(limit=10) 
		template_values = {'venues':venues}
		path = os.path.join(os.path.dirname(__file__),'Templates/admin-addevent.html')
		self.response.out.write(template.render(path,template_values))

class EditEvent(webapp.RequestHandler):
	def get(self):
		venues_query = Venue.all().order('title')
		venues = venues_query.fetch(10)
		events_query = Event.all().order('-date') 
		events = events_query.fetch(10)
		template_values = {'venues':venues, 'events':events}

class EditVenue(webapp.RequestHandler):
    def get(self):
        venues_query = Venue.all().order('title')
        venues = venues_query.fetch(10)
        template_values = {'venues':venues}
        path = os.path.join(os.path.dirname(__file__),'Templates/admin-editvenue.html')
        self.response.out.write(template.render(path,template_values))

class StoreVenue(webapp.RequestHandler):
    def post(self):
        venue = db.get(self.request.get('venueKey'))
        venue.title = self.request.get('venueTitle')
        db.put(venue)
        self.redirect('/admin')	
        
class StoreEvent(webapp.RequestHandler):
    def post(self,mode):
        if mode == "new":
            event = Event()
        if mode == "edit":
            event = db.get(self.request.get('eventKey'))

        event.title = self.request.get('eventTitle')
        event.information = self.request.get('eventInfo')
        venueKey = self.request.get('venueKey')
        year = int(self.request.get('eventY'))
        month = int(self.request.get('eventM'))
        day = int(self.request.get('eventD'))
        event.date = datetime.datetime(year,month,day)
		
        if (venueKey == 'createNew'):
			venue = Venue()
			venue.title = self.request.get('venueTitle')
			venue.put()
        else:
            venue = db.get(venueKey)
        event.venue = venue
        db.put(event)

        self.redirect('/admin')	

application = webapp.WSGIApplication(
                                     [('/admin', AddEvent),('/admin/store_(.*)',StoreEvent),('/admin/edit_event',EditEvent),('/admin/edit_venue',EditVenue),('/admin/storevenue',StoreVenue)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

