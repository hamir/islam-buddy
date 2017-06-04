"""Utility functions."""
import json
from flask import make_response
from common import DailyPrayer

def EncodeParameter(param, spaced=None):
  """Returns param encoded to utf-8"""
  if spaced:
    return ' '.join(param).encode('utf-8')
  return ''.join(param).encode('utf-8')


def JsonResponse(response_dict):
  """Constructs a JSON response object."""
  print 'JsonResponse'
  response = make_response(json.dumps(response_dict, indent=4))
  print 'JsonResponse'
  response.headers['Content-Type'] = 'application/json'
  print 'JsonResponse'
  return response


def JsonError(error_text):
  """Constructs a JSON response from an error."""
  response = make_response(json.dumps({'error': error_text}, indent=4))
  response.headers['Content-Type'] = 'application/json'
  return response


_PRAYER_METADATA = {
    DailyPrayer.FAJR: {
        'key_name': 'fajr',
        'display_name': 'Fajr',
        'pronunciation': 'Fajer',
    },
    DailyPrayer.DHUHR: {
        'key_name': 'dhuhr',
        'display_name': 'Dhuhr',
        'pronunciation': 'Dhuhr',
    },
    DailyPrayer.ASR: {
        'key_name': 'asr',
        'display_name': 'Asr',
        'pronunciation': 'Usser',
    },
    DailyPrayer.MAGHRIB: {
        'key_name': 'maghrib',
        'display_name': 'Maghrib',
        'pronunciation': 'Mugreb',
    },
    DailyPrayer.ISHA: {
        'key_name': 'isha',
        'display_name': 'Isha',
        'pronunciation': 'Isha',
    },
    DailyPrayer.QIYAM: {
        'key_name': 'qiyam',
        'display_name': 'Qiyam',
        'pronunciation': 'Qiyam',
    },
    DailyPrayer.UNSPECIFIED: {
        'key_name': 'unpsecified',
        'display_name': 'unspecified',
        'pronunciation': 'unspecified',
    },
}

_KEY_NAME_TO_PRAYER = {
    'suhur': DailyPrayer.FAJR,
    'fajr': DailyPrayer.FAJR,
    'dhuhr': DailyPrayer.DHUHR,
    'asr': DailyPrayer.ASR,
    'maghrib': DailyPrayer.MAGHRIB,
    'iftar': DailyPrayer.MAGHRIB,
    'isha': DailyPrayer.ISHA,
    'qiyam': DailyPrayer.QIYAM,
    'unspecified': DailyPrayer.UNSPECIFIED,
}


def GetPrayerKeyName(daily_prayer):
  """Gets the name of a daily prayer (ex: "fajr")."""
  return _PRAYER_METADATA.get(daily_prayer).get('key_name')


def _StringToEnum(str_value, str_to_enum, default):
  """Converts a string to an enum based on provided dict."""
  str_value = str(str_value).lower()
  if str_value in str_to_enum:
    return str_to_enum[str_value]
  return default


def StringToDailyPrayer(prayer_str):
  """Infers a DailyPrayer out of a string."""
  prayer_str = str(prayer_str).lower()
  if prayer_str in _KEY_NAME_TO_PRAYER:
    return _KEY_NAME_TO_PRAYER[prayer_str]
  return ''


def GetPronunciation(daily_prayer):
  """Gets TTS for a daily prayer."""
  print 'GetPronunciation: ', _PRAYER_METADATA[daily_prayer]
  return _PRAYER_METADATA[daily_prayer].get('pronunciation')


def GetDisplayText(daily_prayer):
  """Gets display text for a daily prayer."""
  return _PRAYER_METADATA[daily_prayer].get('display_name')
