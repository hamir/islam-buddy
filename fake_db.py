"""This is a shim interface for a database until we have a real one set up."""

_USER_TABLE = {
  "MmtdIf77tCKMRPdYEteAtv8EAWAj830zF5kQY9CB7HE=":
    {
      "name": "Hashim Mir",
      "city": "Mountain View",
      "lat": -122,
      "lng": 37,
    }
}

def GetUserInfo(user_id):
  return _USER_TABLE[user_id]

def AddUser(user_id, user_info):
  _USER_TABLE[user_id] = user_info

