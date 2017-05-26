"""This is a shim interface for a database until we have a real one set up."""

"""
  "MmtdIf77tCKMRPdYEteAtv8EAWAj830zF5kQY9CB7HE=":
    {
      "city": "Mountain View",
      "lat": 37,
      "lng": -122,
    }
"""

_USER_TABLE = {}

def GetUserInfo(user_id):
  return _USER_TABLE.get(user_id, {})

def AddOrUpdateUser(user_id, user_info):
  _USER_TABLE[user_id] = user_info

def DeleteUser(user_id):
  if user_id in _USER_TABLE:
    del _USER_TABLE[user_id]
