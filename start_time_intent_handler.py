# Intent handler for 'WHEN_IS_START_TIME_INTENT'

class StartTimeIntentHandler(object):

  INTENT_NAME = 'WHEN_IS_START_TIME_INTENT'

  def _EncodeParameter(self, param):
    return ' '.join(param).encode('utf-8')

  def HandleIntent(self, device_params, params):
    """Returns a server response as a dictionary."""
    
    # we have the user's city
    city = params.get('geo-city')
    # we have the user's lat/lng
    has_location = 'location' in device_params

    # if there is no city or location, we won't be able to do anything
    # so request the user for permissions to use their location
    if not (city or has_location):
      print ('Could not find location in request, '
             'so responding with a permission request.')
      return response_builder.RequestLocationPermission()

    # we must fill these parameters in order to make a query to salah.com
    lat = None
    lng = None
    desired_prayer = post_params.get('result').get('parameters').get('PrayerName')

    # if we have a city, then use this
    if city:
      city = _EncodeParameter(params.get('geo-city'))
      country = _EncodeParameter(params.get('geo-country'))
      state = _EncodeParameter(params.get('geo-state-us'))

      print 'city:', city 
      print 'country:', country 
      print 'state:', state 

      location_coordinates = gmaps_API.GetGeocode(city, country, state)
      lat = location_coordinates.get('lat')
      lat = location_coordinates.get('lng')

    # if we have a device location, then use it
    elif has_location:
      print 'trying to get contexts index'
      relevant_context = {}
      for candidate in post_params.get('result').get('contexts'):
        if 'requ' in candidate['name']:
          relevant_context = candidate
      
      if relevant_context:
        print 'relevant_context = ', relevant_context

        location = \
            post_params \
                .get('originalRequest') \
                .get('data') \
                .get('location')

        lat = location.get('lat')
        lat = location.get('lng')

        # Since this is a follow-on query, we won't actually have the
        # prayer name in the 'result.parameters.PrayerName'. Instead
        # we must pull it from the context.
        desired_prayer = relevant_context.get('parameters').get('PrayerName')
      else:
        print 'Could not find relevant context!'

    all_prayer_times = prayer_info.GetPrayerTimes(lat, lng)
    prayer_time = \
       all_prayer_times.get(util.StringToDailyPrayer(desired_prayer))
    print 'prayer_times[', desired_prayer, "] = ", prayer_time 

    return _MakeSpeechResponse(desired_prayer, prayer_time, city)


  def _MakeSpeechResponse(self, desired_prayer, prayer_time, city):
    return {
      'speech': 
          ('The time for %s is %s in %s.' % 
           (desired_prayer, prayer_time, post_geo_city))
    }

