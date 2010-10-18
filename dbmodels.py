from google.appengine.ext import db
class Venue(db.Model):
	title = db.StringProperty()

class Event(db.Model):
	title = db.StringProperty()
	venue = db.ReferenceProperty(Venue) 
	date = db.DateTimeProperty()
	information = db.StringProperty(multiline=True)
