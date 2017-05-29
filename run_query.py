import requests


_LOCALHOST = 'http://127.0.0.1:5000/salah'


# queries based on a predefined city, country or state
_PLACE_QUERY_SET = {
  'when_is_fajr_in_city': ['sample_requests/fajr_waterloo_ontario.json'],
  'when_is_fajr_in_state': ['sample_requests/fajr_ontario.json'],
  'when_is_fajr_in_country': ['sample_requests/fajr_zimbabwe.json'],
}


# queries based on the user's current location
_LOCATION_QUERY_SET = {
  'when_is_maghrib_no_location': [
      'sample_requests/when_is_maghrib.json', 
      'sample_requests/deny_location_permission.json'],
  'when_is_maghrib_yes_location': [
      'sample_requests/when_is_maghrib.json', 
      'sample_requests/allow_location_permission.json'],
  'when_is_fajr': ['sample_requests/fajr.json'],
  'when_is_zuhr': ['sample_requests/zuhr.json'],
  'when_is_asr': ['sample_requests/asr.json'],
  'when_is_maghrib': ['sample_requests/maghrib.json'],
  'when_is_isha': ['sample_requests/isha.json'],
  'when_is_iftar': ['sample_requests/iftar.json'],
  'when_is_suhur': ['sample_requests/suhur.json'],
}


for query_name, query_files in _LOCATION_QUERY_SET:
  for query_file in query_files:
    f = open(query_file)
    print '[QUERY = ', query_name, ']\n'
    r = requests.post(_LOCALHOST, json=f.read())
    print r.json(), '\n\n'

