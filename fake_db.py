"""This is a shim interface for a database until we have a real one set up.

  Example database entry:
  "MmtdIf77tCKMRPdYEteAtv8EAWAj830zF5kQY9CB7HE=":
    {
      "city": "Mountain View",
      "lat": 37,
      "lng": -122,
    }
"""


class FakeDb(object):
  """In-memory store of user ID to user info."""

  USER_TABLE_ = {}

  def GetUserInfo(self, user_id):
    """Gets info for a user."""
    return self.USER_TABLE_.get(user_id)

  def AddOrUpdateUser(self, user_id, user_info):
    """Adds new user (or updates existing one) in the database."""
    self.USER_TABLE_[user_id] = user_info

  def DeleteUser(self, user_id):
    """Deletes a user from the database."""
    if user_id in self.USER_TABLE_:
      del self.USER_TABLE_[user_id]
