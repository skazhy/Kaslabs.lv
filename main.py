import os, cgi, datetime
from dbmodels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
    def get(self,page=1):
        epp = 10 # events per page
        page = int(page)
        older = newer = False
        offset = page*epp-epp
        
        events_query = Event.all().order('-date')
        events = events_query.fetch(limit = epp+1, offset = offset)
        if len(events) == epp+1:
            older = page+1
            events.pop() 
        if offset > 0:
            newer = page-1
        for event in events :
			event.date_display = event.date.strftime('%Y/%m/%d')
        template_values = {'events':events, 'newer':newer, 'older':older}

        path = os.path.join(os.path.dirname(__file__),'Templates/base_pub.html')
        self.response.out.write(template.render(path,template_values))

application = webapp.WSGIApplication([('/', MainPage),('/page/(.*)',MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

