"""Tests for aladhan_com_fetcher."""

import aladhan_com_fetcher


def TestFetcher():
  """Tests that the fetcher gets data from salah.com"""
  print aladhan_com_fetcher.GetDailyPrayerTimes(37.3541079, -121.9552355)


TestFetcher()

