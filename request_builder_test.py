import request_builder

def test_request_builder():
  """Tests that the JSON is built with the given inputs."""
  print '\n when is maghrib', request_builder.BuildJSON('maghrib', 'when is maghrib', 'when is maghrib', 'WHEN_IS_START_TIME_INTENT')
  print '\n when is isha in fremont', request_builder.BuildJSON('isha', 'when is isha in fremont', 'when is isha in fremont', 'WHEN_IS_START_TIME_INTENT', geo_city='fremont')
  print '\n yes for permission', request_builder.BuildJSON('maghrib', 'yes', 'actions_intent_PERMISSION', 'PERMISSION_INTENT', conversation_type='ACTIVE', permission='true')
  print '\n no for permission', request_builder.BuildJSON('fajr', 'no', 'actions_intent_PERMISSION', 'PERMISSION_INTENT', conversation_type='ACTIVE', permission='false')
  print '\n what time is fajr today in union city', request_builder.BuildJSON('fajr', 'what time is fajr today in union city', 'what time is fajr today in union city', \
        'WHEN_IS_START_TIME_INTENT', geo_city='union city')

test_request_builder()
