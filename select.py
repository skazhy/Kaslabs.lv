import os, cgi, datetime
from dbmodels import *
from datetime import timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class TimeMain(webapp.RequestHandler):
    def get(self):
        today = datetime.date.today()
        
        # Tomorrow
        tomorrow_obj = today + timedelta(days=1);
        tomorrow=tomorrow_obj.strftime('%Y%m%d')
        
        # After 2 days
        atm = tomorrow_obj + timedelta(days=1);
        atomorrow=atm.strftime('%Y%m%d')
        
        # After 3 days
        aatm = atm + timedelta(days=1);
        aatomorrow=aatm.strftime('%Y%m%d')
        
        # This week
        daynumber = int(today.strftime('%u'))
        week_end = today + timedelta(days=7-daynumber)
        week_start = today - timedelta(days=daynumber-1)
        week = week_start.strftime('%Y%m%d')
        week += '-'
        week += week_end.strftime('%Y%m%d')

        # Next week
        nws = week_end + timedelta(days=1)
        nwe = week_end + timedelta(days=7)
        nextweek = nws.strftime('%Y%m%d')
        nextweek += '-'
        nextweek += nwe.strftime('%Y%m%d')

        # This month
        month_nr = int(today.strftime('%m'))
        year = int(today.strftime('%Y'))
        monthstart = datetime.date(year, month_nr, 1)
        monthend = datetime.date(year, month_nr + 1, 1)
        monthend = monthend - timedelta(days=1)
        month = monthstart.strftime('%Y%m%d')
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

application = webapp.WSGIApplication([('/kad',TimeMain)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
