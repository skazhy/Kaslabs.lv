import os
import cgi
import dtfunctions
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from dbmodels import *
from datetime import timedelta

# Requests containing text
class DefaultFilter(webapp.RequestHandler):
    def get(self,timescale):
        error = False
        request = dtfunctions.parse_timescale(timescale)
        events = dtfunctions.get_events(request)
        if events[1]:
            error = True
        template_values = {'events':events[0],'error':error, 'logo':timescale } 
        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        page = template.render(path,template_values)
        self.response.out.write(page)

# Requests containing dates
class TimeFilter(webapp.RequestHandler):
    def get(self,request=""):
        # Renders page with a custom timescale.
        if request:
            page = self.render_page(request,'default')
        # Returns the main page
        else:
            page = self.get_main()
        self.response.out.write(page)

    def get_main(self):
        main_page = memcache.get("main_page")
        if main_page is not None:
            return main_page
        else:
            today = dtfunctions.today()
            main_page = self.render_page(today,'sodien')
            memcache.add("main_page",main_page,300)
            return main_page
    
    def render_page(self,request,logo):
        error = False
        events = dtfunctions.get_events(request)
        if events[1]:
            error = True
        template_values = {'events':events[0],'error':error, 'logo':logo } 
        path = os.path.join(os.path.dirname(__file__),'Templates/base-pub.html')
        page = template.render(path,template_values)
        return page

class FilterMain(webapp.RequestHandler):
     def get(self):
        path = os.path.join(os.path.dirname(__file__),'Templates/public-timeselect.html')
        self.response.out.write(template.render(path,{}))

application = webapp.WSGIApplication([('/',TimeFilter),
                                      ('/kad/(.*)',DefaultFilter),
                                      ('/d/(.*)',TimeFilter),
                                      ('/kad',FilterMain)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
