"""Masjid Utility functions."""

_MASJID_METADATA = {
    'MCA': {
        'key_name': 'MCA',
        'display_name': 'MCA',
        'id': 8,
    },
    'Noor': {
        'key_name': 'Noor',
        'display_name': 'Masjid Al Noor',
        'id': 9,
    },
    'Waterloo': {
        'key_name': 'Waterloo',
        'display_name': 'Waterloo Masjid',
        'id': 134,
    },
    'MCC': {
        'key_name': 'MCC',
        'display_name': 'MCC East Bay',
        'id': 17,
    },
    'SBIA': {
        'key_name': 'SBIA',
        'display_name': 'SBIA',
        'id': 10,
    },
    'West Valley': {
        'key_name': 'West Valley',
        'display_name': 'West Valley Muslim Association',
        'id': 15,
    },
}


def GetIqamaID(masjid):
  """Gets the masjid id from _MASJID_METADATA obtained from Iqamah.net

  Args:
    masjid: a string representing the masjid of intereset from the
    masjid-entity

  Returns: an integer containing the masjid id
  """

  if _MASJID_METADATA.get(masjid):
    return _MASJID_METADATA.get(masjid).get('id')
  return None


def GetMasjidDisplayName(masjid):
  """Gets the masjid display_name from _MASJID_METADATA

  Args:
    masjid: a string representing the masjid of intereset from the
    masjid-entity

  Returns: a string containing the masjid name to be displayed to the user
  """

  if _MASJID_METADATA.get(masjid):
    return _MASJID_METADATA.get(masjid).get('display_name')
  return None
