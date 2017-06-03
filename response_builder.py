"""Helps build reponses in a format API.AI understands."""


def RequestLocationPermission():
  """Asks the usee permission to use their location."""
  return {
      "data": {
          "google": {
              "expectUserResponse": 1,
              "systemIntent": {
                  "intent": "actions.intent.PERMISSION",
                  "data": {
                      "@type":
                      "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                      "optContext":
                      "To get you accurate timings",
                      "permissions": ["DEVICE_PRECISE_LOCATION"]
                  }
              }
          }
      }
  }
