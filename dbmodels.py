from google.appengine.ext import db

class Venue(db.Model):
    title = db.StringProperty()
    city = db.StringProperty()
    address = db.TextProperty()
    web = db.StringProperty()

class Event(db.Model):
    title = db.StringProperty()
    venue = db.ReferenceProperty(Venue)
    date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
    information = db.TextProperty()
    intro_text = db.TextProperty()
