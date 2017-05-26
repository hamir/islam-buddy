"""This is a shim interface for a database until we have a real one set up."""

"""
  "MmtdIf77tCKMRPdYEteAtv8EAWAj830zF5kQY9CB7HE=":
    {
      "city": "Mountain View",
      "lat": 37,
      "lng": -122,
    }
"""
_USER_TABLE = {
}

def GetUserInfo(user_id):
  return _USER_TABLE.get(user_id)

def AddUser(user_id, user_info):
  _USER_TABLE[str(user_id)] = user_info

