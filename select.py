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

application = webapp.WSGIApplication([('/kad',TimeMain)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
