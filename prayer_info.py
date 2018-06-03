"""Computes daily salah times based on location."""
import praytime_fetcher
import util


# pylint: disable-msg=r0903
class PrayerInfo(object):
    """Gets and packages prayer information."""

    @classmethod
    def GetPrayerTimes(cls, lat, lng, date_str):
        """Gets the daily prayer times for a given lat/lng.

        Args:
          lat: a double representing the latitude
          lng: a double representing the longitude
          date_str: a string representing the requested date in YYYY-MM-DD

        Returns: a dict containing (DailyPrayer -> string) of daily
            prayer times
        """

        (prayer_times, day_difference) = praytime_fetcher.GetDailyPrayerTimes(lat, lng, date_str)
        if not prayer_times or prayer_times == {}:
            return (None, None)

        result = {}

        for key in prayer_times:
            prayer = util.StringToDailyPrayer(key)
            if prayer:
                result[prayer] = util.ConvertTimeToAMPM(prayer_times[key])

        return (result, day_difference)

