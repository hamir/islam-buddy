"""Intent handler for WHEN_IS_START_TIME_INTENT, HOW_LONG_PRAYER_TIME_INTENT, and NEXT_PRAYER."""

#import json
import util
import response_builder
import gmaps_client
from iqama_fetcher import GetIqamaTime
from common import Locality
from masjid_util import GetMasjidDisplayName


def _GetContext(post_params, context_name):
  for candidate in post_params.get('result').get('contexts'):
    if candidate['name'] == context_name:
      return candidate
  return None


def _MakeSpeechResponse(canonical_prayer, desired_prayer, prayer_time, prayer_time_prop,
                        locality):
  # prayer_time contains [0] desired prayer time diff, [1] next prayer, [2] next prayer time,
  # [3] next prayer time diff if prayer_time_prop is set; otherwise it is desired prayer time

  speech = ''
  if prayer_time and locality:
    preposition = "in" if locality[0] == Locality.CITY else "at"
    location = locality[1] if locality[0] == Locality.CITY else GetMasjidDisplayName(locality[1])

    try:
      location = location.decode('utf-8')
    except:
      location = 'your location'

    if prayer_time_prop and prayer_time_prop.lower() == 'time until':
      if (not canonical_prayer or canonical_prayer == 'NA' or not desired_prayer or
          not locality[0] == Locality.CITY):
        return _DefaultErrorResponse()

      pronunciation_prayer = util.GetPronunciation(canonical_prayer)
      display_prayer = util.GetDisplayText(canonical_prayer)

      # get the hours and minutes if there are more than or equal to an hour;
      # otherwise just return the minutes
      if not isinstance(prayer_time[0], dict):
        return _DefaultErrorResponse()

      hour_string = 'Hours'
      minute_string = 'Minutes'

      if prayer_time[0]['HOURS'] == 1:
        hour_string = 'Hour'
      if prayer_time[0]['MINUTES'] == 1:
        minute_string = 'Minute'

      if prayer_time[0]['HOURS'] > 0:
        time_str = '%s %s and %s %s' % (prayer_time[0]['HOURS'], hour_string, prayer_time[0]['MINUTES'], minute_string)
      elif prayer_time[0]['MINUTES'] > 1:
        time_str = '%s %s' % (prayer_time[0]['MINUTES'], minute_string)

      if desired_prayer.lower() == 'suhur':
        pronunciation_prayer = 'Suhur'
        display_prayer = 'Suhur'
      elif desired_prayer.lower() == 'iftar':
        pronunciation_prayer = 'Iftar'
        display_prayer = 'Iftar'

      # if the indices of the desired prayer and the next prayer are one apart
      # or at a difference of -5 (Isha's index is 6 and Fajr's index is 1) 
      # or the time difference is 0 Hours and 0 Minutes then
      # it is currently time for the desired prayer;
      # otherwise return the time left for the desired prayer
      if not prayer_time[1]:
        return _DefaultErrorResponse()

      if ((prayer_time[1] - canonical_prayer == 1) or (prayer_time[1] - canonical_prayer == -5)
          or (prayer_time[0]['HOURS'] == 0 and prayer_time[0]['MINUTES'] == 0)):
        if desired_prayer.lower() == 'suhur':
          speech = 'The time for %s %s %s has ended.' % (
              pronunciation_prayer, preposition, location)
          display_text = 'The time for %s %s %s has ended.' % (
              display_prayer, preposition, location)
        else:
          next_prayer = prayer_time[1]
          next_prayer_time = prayer_time[2]

          pronunciation_next_prayer = util.GetPronunciation(next_prayer)
          display_next_prayer = util.GetDisplayText(next_prayer)
          speech = 'It is currently time for %s %s %s. %s is coming up at %s.' % (
              pronunciation_prayer, preposition, location,
              pronunciation_next_prayer, next_prayer_time)
          display_text = 'It is currently time for %s %s %s. %s is coming up at %s.' % (
              display_prayer, preposition, location,
              display_next_prayer, next_prayer_time)
      else:
        speech = 'There is %s left before the time for %s %s %s.' % (
            time_str, pronunciation_prayer, preposition, location)
        display_text = 'There is %s left before the time for %s %s %s.' % (
            time_str, display_prayer, preposition, location)
    elif prayer_time_prop and prayer_time_prop.lower() == 'next prayer':
      if not prayer_time[1] or not prayer_time[2] or not locality[0] == Locality.CITY:
        return _DefaultErrorResponse()

      time_str = '%s %s %s' % (prayer_time[2], preposition, location)

      next_prayer = prayer_time[1]

      pronunciation_prayer = util.GetPronunciation(next_prayer)
      display_prayer = util.GetDisplayText(next_prayer)

      speech = '%s is coming up at %s.' % (
          pronunciation_prayer, time_str)
      display_text = '%s is coming up at %s.' % (
          display_prayer, time_str)
    elif prayer_time_prop and prayer_time_prop.lower() == 'fasting times':
      if not prayer_time[0] or not prayer_time[1] or not locality[0] == Locality.CITY:
        return _DefaultErrorResponse()

      speech = 'Fasting starts from %s and ends at %s in %s.'  % (
          prayer_time[0], prayer_time[1], location)
      display_text = 'Fasting starts from %s and ends at %s in %s.'  % (
          prayer_time[0], prayer_time[1], location)
    elif canonical_prayer and not canonical_prayer == 'NA':
      time_str = '%s %s %s' % (prayer_time, preposition, location)

      pronunciation_prayer = util.GetPronunciation(canonical_prayer)
      display_prayer = util.GetDisplayText(canonical_prayer)

      if desired_prayer.lower() == 'suhur':
        return {'speech': 'Suhur ends at %s.' % time_str}
      elif desired_prayer.lower() == 'iftar':
        return {'speech': 'Today, Iftar is at %s.' % time_str}

      speech = 'The time for %s is %s.' % (
          pronunciation_prayer, time_str)
      display_text = 'The time for %s is %s.' % (
          display_prayer, time_str)
    else:
      return _DefaultErrorResponse()
  else:
    return _DefaultErrorResponse()

  return {'speech': speech, 'displayText': display_text}


def _DefaultErrorResponse():
  speech = 'Sorry. Prayer Pal is unable to process your request at the moment.'\
      'Please try again later.'
  display_text = 'Sorry. Prayer Pal is unable to process your request at'\
      ' the moment. Please try again later.'

  return {'speech': speech, 'displayText': display_text}


def _RespondWithIqamaTime(masjid, desired_prayer):
  #print 'masjid: ', masjid
  if not desired_prayer or not masjid:
    return _MakeSpeechResponse(None, None, None, None,
                               (None, None))
  canonical_prayer = util.StringToDailyPrayer(desired_prayer)
  if desired_prayer and not desired_prayer.lower() == 'suhur':
    iqama_time = GetIqamaTime(canonical_prayer, masjid)
    #print 'iqama_time[', desired_prayer, "] = ", iqama_time
    return _MakeSpeechResponse(canonical_prayer, desired_prayer, iqama_time, None,
                               (Locality.MASJID, masjid))
  return {'speech': 'Sorry, suhur time is not supported for masjids.'}


# pylint: disable=too-few-public-methods
class IntentHandler(object):
  """Handles the core intents WHEN_IS_START_TIME_INTENT,
  HOW_LONG_PRAYER_TIME_INTENT, FASTING_TIMES_INTENT, and NEXT_PRAYER_INTENT."""

  INTENTS_HANDLED = [
      'WHEN_IS_START_TIME_INTENT',
      'HOW_LONG_PRAYER_TIME_INTENT',
      'NEXT_PRAYER_INTENT',
      'FASTING_TIMES_INTENT',
      'PERMISSION_INTENT',
  ]

  def __init__(self, prayer_info, fake_db, db):
    self.prayer_info_ = prayer_info
    self.fake_db_ = fake_db
    self.db_ = db

  def HandleIntent(self, post_params):
    """Returns a server response as a dictionary."""

    # filled if we have the user's city, country and/or state
    params = post_params.get('result').get('parameters')
    city = params.get('geo-city')

    # filled if the user calls for a masjid
    masjid = params.get('MasjidName')

    # filled if we have the user's lat/lng
    device_params = {}
    if 'originalRequest' in post_params:
      device_params = post_params.get('originalRequest').get('data').get(
          'device')
    has_location = device_params and 'location' in device_params
    # this will only be populated if the intent type is PERMISSION_REQUEST
    permission_context = None

    # filled if the user would like to know the time before a prayer or the time for
    # the next prayer
    prayer_time_prop = params.get('prayer-time-prop')

    if not has_location:
      # this should always be filled since its a required parameter to the intent
      # the only time it won't be filled is on PERMISSION_REQUEST intents
      desired_prayer = params.get('PrayerName')
    else:
      # this should be filled on PERMISSION_REQUEST intents in the relevant context
      permission_context = _GetContext(post_params, 'requ')
      #print 'permission context = ', permission_context
      desired_prayer = permission_context.get('parameters').get('PrayerName')
      prayer_time_prop = permission_context.get('parameters').get('prayer-time-prop')

    # this should also always be available
    user_id = post_params.get('originalRequest').get('data').get('user').get(
        'userId')

    # if we have a masjid name then call GetIqamaTime to obtain it from scraper
    if masjid:
      return _RespondWithIqamaTime(masjid, desired_prayer)

    # if there is no city or location, we won't be able to do anything
    # so request the user for permissions to use their location
    if not (city or has_location):
      return self._LookupOrRequestInformation(post_params, params,
                                              desired_prayer, user_id, prayer_time_prop)

    # if we have a city, then use this
    if city:
      return self._RespondToCityRequest(params, desired_prayer, prayer_time_prop)

    # if we have a device location, then use it
    elif has_location:
      return self._RespondToLocationRequest(device_params, permission_context,
                                            user_id, desired_prayer, prayer_time_prop)

  def _LookupOrRequestInformation(self, post_params, params, desired_prayer,
                                  user_id, prayer_time_prop):
    # do not ask for permission if we've already asked for it before
    permission_context = _GetContext(post_params, 'actions_intent_permission')
    if (permission_context and
        permission_context.get('parameters').get('PERMISSION') == 'false'):
      # if we are here it means the user rejected our request to use location
      return {
          'speech':
          ('Sorry, I\'ll need a location in order to get a prayer time.'
           ' You can also try asking prayer times for a city next time.')
      }

    # the user has specified a state or country but not a city, then we should
    # instruct them to tell us a city name.
    if params.get('geo-state-us') or params.get('geo-country'):
      return {
          'speech': ('Sorry, I don\'t have enough information. Please try '
                     'again with a city next time.')
      }

    # at this stage, we don't know anything about the user's location - try
    # checking our db for a cached location

    # however, do not use the user's cached location if user has explicitly requested
    # that their current location be used
    explicit_location_requested = params.get('user-current-location')

    #print 'prayer time prop', prayer_time_prop

    user = self.db_.GetUser(user_id)
    #print 'user info for ', user_id, ' is ', user
    user_info = user.get('user_info')
    if (not explicit_location_requested and user_info and
        user_info.get('lat') and user_info.get('lng') and
        user_info.get('city')):
      #print 'found user ', user_id, ' in database, so location request is not necessary'
      lat = user_info.get('lat')
      lng = user_info.get('lng')
      city = user_info.get('city')
      return self._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, prayer_time_prop)

    #print('Could not find location in request, '
    #      'so responding with a permission request.')
    return response_builder.RequestLocationPermission()

  def _RespondToLocationRequest(self, device_params, permission_context,
                                user_id, desired_prayer, prayer_time_prop):
    if permission_context:
      #print 'permission context'
      location = device_params.get('location')
      lat = location.get('coordinates').get('latitude')
      lng = location.get('coordinates').get('longitude')
      city = location.get('city')
      if not city:
        city = gmaps_client.ReverseGeocodeCity(lat, lng)
      user = {
          'user_info': {'city': city, 'lat': lat, 'lng': lng},
          'city': city
      }
      #print 'caching user location for ', user_id, ' as ', json.dumps(user)
      self.db_.AddOrUpdateUser(user_id, user)
    #else:
    #  print 'Could not find relevant context!'

    return self._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, prayer_time_prop)

  def _RespondToCityRequest(self, params, desired_prayer, prayer_time_prop):
    city = util.EncodeParameter(params.get('geo-city'), True)
    country = util.EncodeParameter(params.get('geo-country'), True)
    state = util.EncodeParameter(params.get('geo-state-us'), True)

    location_coordinates = gmaps_client.GetGeocode(city, country, state)
    if not location_coordinates:
      return _MakeSpeechResponse(None, None, None, None,
                               (None, None))
    lat = location_coordinates.get('lat')
    lng = location_coordinates.get('lng')

    return self._ComputePrayerTimeAndRespond(desired_prayer, lat, lng, city, prayer_time_prop)

  def _ComputePrayerTimeProperty(self, canonical_prayer, all_prayer_times, lat, lng):
    """Computes the desired prayer's time difference as well as the
    next prayer, next prayer's time, and next prayer's time difference"""
    current_user_time = util.GetCurrentUserTime(lat, lng)

    if current_user_time:
      next_prayer_time_diff = {}
      # loop through all the prayer times to obtain the next prayer,
      # next prayer's time, and next prayer's time difference
      for prayer in all_prayer_times:
        # skip prayer if it is [0] unspecified, [7] qiyam, or [2] sunrise
        if not prayer or prayer == 7 or prayer == 0 or prayer == 2:
          continue
        prayer_time = all_prayer_times.get(prayer)
        if not prayer_time:
          return None
        # get the time difference between the current user time and the loop prayer time
        time_until_params = util.GetTimeDifference(current_user_time, prayer_time)
        if next_prayer_time_diff:
          if (time_until_params['HOURS'] < next_prayer_time_diff['HOURS'] or
              (time_until_params['HOURS'] == next_prayer_time_diff['HOURS']
               and time_until_params['MINUTES'] < next_prayer_time_diff['MINUTES'])):
            next_prayer_time_diff = time_until_params
            next_prayer = prayer
            next_prayer_time = prayer_time
        else:
          next_prayer_time_diff = time_until_params
          next_prayer = prayer
          next_prayer_time = prayer_time
      # obtain the desired prayer's time difference
      desired_prayer_time_diff = 0
      if canonical_prayer and not canonical_prayer == 'NA':
        desired_prayer_time = all_prayer_times.get(canonical_prayer)
        desired_prayer_time_diff = util.GetTimeDifference(current_user_time, desired_prayer_time)
      return (desired_prayer_time_diff, next_prayer, next_prayer_time, next_prayer_time_diff)
    else:
      return None

  def _ComputePrayerTimeAndRespond(self, desired_prayer, lat, lng, city, prayer_time_prop):
    if not city:
      city = 'your location'
    all_prayer_times = self.prayer_info_.GetPrayerTimes(lat, lng)
    canonical_prayer = 'NA'
    if desired_prayer:
      canonical_prayer = util.StringToDailyPrayer(desired_prayer)
    if prayer_time_prop and prayer_time_prop.lower() != 'fasting times':
      computed_prayer_time_property = self._ComputePrayerTimeProperty(canonical_prayer,
                                                                      all_prayer_times, lat, lng)
      return _MakeSpeechResponse(canonical_prayer, desired_prayer, computed_prayer_time_property,
                                 prayer_time_prop, (Locality.CITY, city))
    if prayer_time_prop and prayer_time_prop.lower() == 'fasting times':
      fasting_times = []
      suhur_canonical_prayer = util.StringToDailyPrayer('suhur')
      iftar_canonical_prayer = util.StringToDailyPrayer('iftar')
      fasting_times.append(all_prayer_times.get(suhur_canonical_prayer))
      fasting_times.append(all_prayer_times.get(iftar_canonical_prayer))
      return _MakeSpeechResponse(canonical_prayer, desired_prayer, fasting_times, prayer_time_prop,
                               (Locality.CITY, city))  
    prayer_time = all_prayer_times.get(canonical_prayer)
    #print 'prayer_times[', desired_prayer, "] = ", prayer_time
    return _MakeSpeechResponse(canonical_prayer, desired_prayer, prayer_time, prayer_time_prop,
                               (Locality.CITY, city))

