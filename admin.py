import os
import datetime
import markdown

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from dbmodels import *

# Displaying Event adding form.
class AddEvent(webapp.RequestHandler):
    def get(self):
        venues_query = Venue.all().order('title')
        venues = venues_query.fetch(limit=100)
        template_values = {'venues':venues }
        path = os.path.join(os.path.dirname(__file__),'Templates/admin-addevent.html')
        self.response.out.write(template.render(path,template_values))

# Displaying list of events to edit.
class EditEvent(webapp.RequestHandler):
    def get(self,page=1):
        epp = 10
        page = int(page)
        older = newer = False
        offset = page*epp-epp

        venues_query = Venue.all().order('title')
        venues = venues_query.fetch(limit=100)

        events_query = Event.all().order('-date')
        events = events_query.fetch(offset=offset, limit=epp+1)

        # Event paging
        if len(events) == epp+1:
            older = page+1
            events.pop()
        if offset > 0:
            newer = page-1
        if len(events) == 0:
            older=newer=False
            
        # Event time displaying
        for event in events:
            event.time_display = event.date.strftime('%R')
            event.date_display = event.date.strftime('%-d. %B, %Y')
            event.date_form = event.date.strftime('%Y-%m-%d')
            if event.end_date:
                event.end_time_display = event.end_date.strftime('%R')
                event.end_date_display = event.end_date.strftime('%-d. %B, %Y')
                event.end_date_form = event.end_date.strftime('%Y-%m-%d')

        template_values = {'venues':venues, 
                           'events':events,
                           'older':older,
                           'newer':newer }
        
        path = os.path.join(os.path.dirname(__file__),'Templates/admin-editevent.html')
        self.response.out.write(template.render(path,template_values))

# Displaying list of venues to edit.
class EditVenue(webapp.RequestHandler):
    def get(self):
        venues_query = Venue.all().order('title')
        venues = venues_query.fetch(10)
        template_values = { 'venues':venues }
        
        path = os.path.join(os.path.dirname(__file__),'Templates/admin-editvenue.html')
        self.response.out.write(template.render(path,template_values))

# Saving new / edited venue.
class StoreVenue(webapp.RequestHandler):
    def post(self):
        if self.request.get('venueOc') == 'c':
            venue = Venue() 
        else:
            venue = db.get(self.request.get('venueKey'))
        venue.title = self.request.get('venueTitle')
        venue.city = self.request.get('venueCity')
        venue.address = self.request.get('venueAddress')
        venue.web = self.request.get('venueWeb')
        memcache.delete("main_page") 
        db.put(venue)
        self.redirect('/admin/edit_venue')	
        
# Saving new / edited event.
class StoreEvent(webapp.RequestHandler):
    def post(self,mode):
        if mode == "new" or self.request.get('eventOc') == 'c':
            event = Event()
        else:
            event = db.get(self.request.get('eventKey'))
        
        event.title = self.request.get('eventTitle')
        event.information = self.request.get('eventInfo')
        event.intro_text = self.request.get('eventIntro')
        event.date = self.make_date(self.request.get('eventDate'),self.request.get('eventTime'))
        
        if self.request.get('eventTime_end') and self.request.get('eventDate_end'):
            event.end_date = self.make_date(self.request.get('eventDate_end'),
                                            self.request.get('eventTime_end'))
        else:
            event.end_date = False;
        if not event.end_date:
            event.length = 1
        else:
            length = event.end_date - event.date
            event.length = length.days + 1

        venueKey = self.request.get('venueKey')
        if venueKey == 'createNew':
            venue = Venue()
            venue.title = self.request.get('venueTitle')
            venue.city = self.request.get('venueCity')
            venue.address = self.request.get('venueAddress')
            venue.web = self.request.get('venueWeb')
            venue.put()
        else:
            venue = db.get(venueKey)
        event.venue = venue
        db.put(event)
        memcache.delete("main_page") 
        self.redirect('/admin/edit_event')	
    
    def make_date(self,date,time):
        return datetime.datetime(int(date[0:4]), int(date[5:7]),
                                 int(date[8:10]), int(time[0:2]),
                                 int(time[3:5]))

class DeleteEntry(webapp.RequestHandler):
    def post(self,mode):
        entry = db.get(self.request.get('entry'))
        # db.delete(entry)
        if mode == 'venue':
                events = Event.all().filter('venue = ',entry)
                events = events.fetch(limit=1)
                if len(events) == 0:
                        db.delete(entry)
        if mode == 'event':
                memcache.delete('main_page')
                db.delete(entry)
        self.redirect('/admin/edit_%s' % (mode))	
        
class ChangeLog(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),'Templates/admin-changelog.html')
        self.response.out.write(template.render(path,{}))

application = webapp.WSGIApplication([('/admin', AddEvent),
                                      ('/admin/store_(.*)',StoreEvent),
                                      ('/admin/edit_event',EditEvent),
                                      ('/admin/edit_event/(.*)',EditEvent),
                                      ('/admin/delete_(.*)',DeleteEntry),
                                      ('/admin/edit_venue',EditVenue),
                                      ('/admin/storevenue',StoreVenue),
                                      ('/admin/changelog',ChangeLog)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

