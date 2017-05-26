"""This is a shim interface for a database until we have a real one set up."""

"""
  "MmtdIf77tCKMRPdYEteAtv8EAWAj830zF5kQY9CB7HE=":
    {
      "city": "Mountain View",
      "lat": 37,
      "lng": -122,
    }
"""

class FakeDb(object):

  USER_TABLE_ = {
  }

  def GetUserInfo(self, user_id):
    return self.USER_TABLE_.get(user_id)

  def AddOrUpdateUser(self, user_id, user_info):
    self.USER_TABLE_[user_id] = user_info

  def DeleteUser(self, user_id):
    if user_id in self.USER_TABLE_:
      del self.USER_TABLE_[user_id]
