"""Interface into the database."""

from google.appengine.ext import ndb


class User(ndb.Model):
    user_info = ndb.PickleProperty()
    city = ndb.StringProperty()


class Database(object):
    def AddOrUpdateUser(self, google_id, data):
        """Adds or updates a user with user_info to the user table."""
        # set the primary key as the google ID
        user = User(
            id=google_id,
            user_info=data.get('user_info'),
            city=data.get('city'))
        user.put()

    def GetUser(self, google_id):
        """Gets user info for the specified google ID."""
        print 'fetching user for ID = ', google_id
        key = ndb.Key(User, google_id).get()
        return key.to_dict() if key else {}

    def DeleteUser(self, google_id):
        """Deletes a user from the database."""
        key = ndb.Key(User, google_id)
        key.delete()
