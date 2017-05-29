import salah_com_fetcher
import requests

def test_fetcher():
  """Tests that the fetcher gets data from salah.com"""
  print salah_com_fetcher.GetDailyPrayerTimes(37.3541079, -121.9552355)

def test_JSON_builder():
  """Tests that the JSON is built with the given inputs."""
  print '\n when is maghrib', salah_com_fetcher.BuildJSON('maghrib', 'when is maghrib', 'when is maghrib', 'WHEN_IS_START_TIME_INTENT')
  print '\n when is isha in fremont', salah_com_fetcher.BuildJSON('isha', 'when is isha in fremont', 'when is isha in fremont', 'WHEN_IS_START_TIME_INTENT', geo_city='fremont')
  print '\n yes for permission', salah_com_fetcher.BuildJSON('maghrib', 'yes', 'actions_intent_PERMISSION', 'PERMISSION_INTENT', conversation_type='ACTIVE', permission='true')
  print '\n no for permission', salah_com_fetcher.BuildJSON('fajr', 'no', 'actions_intent_PERMISSION', 'PERMISSION_INTENT', conversation_type='ACTIVE', permission='false')

test_fetcher()
test_JSON_builder()
