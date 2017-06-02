import salah_com_fetcher
import requests

def test_fetcher():
  """Tests that the fetcher gets data from salah.com"""
  print salah_com_fetcher.GetDailyPrayerTimes(37.3541079, -121.9552355)

test_fetcher()
