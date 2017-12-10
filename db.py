"""Interface into the database."""

from google.appengine.ext import ndb


class User(ndb.Model):
  user_info = ndb.PickleProperty()


class Database(object):
  def AddOrUpdateUser(self, google_id, user_info):
    """Adds or updates a user with user_info to the user table."""
    # set the primary key as the google ID
    user = User(id=google_id, user_info=user_info)
    user.put()

  def GetUserInfo(self, google_id):
    """Gets user info for the specified google ID."""
    key = ndb.Key(User, google_id).get()
    if key:
      return key.user_info
    else:
      return None

  def DeleteUser(self, google_id):
    """Deletes a user from the database."""
    key = ndb.Key(User, google_id)
    key.delete()

