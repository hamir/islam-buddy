#!/usr/bin/env python
import os
import json
import util

from flask import Flask, request, make_response, render_template, redirect
from flask_assistant import Assistant, tell
from oauth2.tokengenerator import URandomTokenGenerator
from daily_prayer import PrayerInfo
from common import DailyPrayer
import response_builder 
import gmaps_API

app = Flask(__name__)
prayer_info = PrayerInfo()
token_generator = URandomTokenGenerator(20)

@app.route('/')
def hello_world():
  return 'Welcome to the Islam Buddy API!'

@app.route('/salah', methods=['POST', 'GET'])
def GetSalah():
  if request.method == 'GET':
    print 'received GET request'
    params = {
      'lat': request.args.get('lat'),
      'lng': request.args.get('lng'),
      'prayer': request.args.get('prayer'),
    }
    print 'params = ', params

    if not params.get('lat') or not params.get('lng'):
      return util.JsonError('Please provide a lat and lng.')

    prayer_times = \
      prayer_info.GetPrayerTimes(params.get('lat'), params.get('lng'))

    # convert from map<PrayerTime, string> to map<string, string>
    output_prayer_times = {}
    for key in prayer_times:
      output_prayer_times[util.GetPrayerKeyName(key)] = prayer_times[key]

    return util.JsonResponse(output_prayer_times)

  elif request.method == 'POST':
    print 'received POST request'

    post_params = request.get_json(silent=True, force=True)
    print 'post_params = \n', json.dumps(post_params, indent=2)

    device_params = post_params.get('originalRequest').get('data').get('device')
    # this needs to be less hacky - @hamdy maybe a request extractor class?
    # we need a request extractor class
    print 'intent_name = ', post_params.get('result').get('metadata').get('intentName') 
    
    post_intent_name = post_params.get('result').get('metadata').get('intentName')
    post_prayer = post_params.get('result').get('parameters').get('PrayerName')
    post_geo_city = (post_params.get('result').get('parameters').get('geo-city'))

    if (post_intent_name == 'WHEN_IS_START_TIME_INTENT' 
        and 'location' not in device_params
        and not post_geo_city):
      print 'Could not find location in request, so responding with a permission request.'
      server_response = response_builder.RequestLocationPermission()
    elif (post_geo_city and 'location' not in device_params):
      post_geo_city = ' '.join(post_geo_city).encode('utf-8')
      post_geo_country = ' '.join(post_params.get('result').get('parameters')\
        .get('geo-country')).encode('utf-8')
      post_geo_state_us = ' '.join(post_params.get('result').get('parameters')\
        .get('geo-state-us')).encode('utf-8')
      print 'city:', post_geo_city
      print 'country:', post_geo_country
      print 'state:', post_geo_state_us
      location_coordinates = gmaps_API.GetGeocode(
          post_geo_city,
          post_geo_country,
          post_geo_state_us) 

      all_prayer_times = \
          prayer_info.GetPrayerTimes(
              location_coordinates.get('lat'),
              location_coordinates.get('lng'))

      prayer_time = \
         all_prayer_times.get(util.StringToDailyPrayer(post_prayer))
      print 'prayer_times[', post_prayer, "] = ", prayer_time
      speech = "The time for %s is %s in %s." % \
          (post_prayer, prayer_time,post_geo_city)
      server_response = {
          "speech": speech,
      }

    elif ('location' in device_params):
      print 'trying to get contexts index'
      relevant_context = {}
      for candidate in post_params.get('result').get('contexts'):
        if 'requ' in candidate['name']:
          relevant_context = candidate
      
      if relevant_context:
        print 'relevant_context = ', relevant_context
        prayer_params = {
         'prayer': \
             relevant_context.get('parameters').get('PrayerName'),
         'lat': \
             post_params.get('originalRequest') \
                 .get('data') \
                 .get('device') \
                 .get('location') \
                 .get('coordinates') \
                 .get('latitude'),
         'lng': \
             post_params \
                .get('originalRequest') \
                .get('data') \
                .get('device') \
                .get('location') \
                .get('coordinates') \
                .get('longitude'),
        'city': \
             post_params \
                .get('originalRequest') \
                .get('data') \
                .get('device') \
                .get('location') \
                .get('city'),
        }

        all_prayer_times = \
            prayer_info.GetPrayerTimes(
                prayer_params.get('lat'),
                prayer_params.get('lng'))

        prayer_time = \
            all_prayer_times.get(util.StringToDailyPrayer(prayer_params.get('prayer')))
        print 'prayer_times[', prayer_params.get('prayer'), "] = ", prayer_time

        # this also needs to be less hacky - @hamir maybe a json response formater class?
        speech = "The time for %s is %s in %s." % \
            (prayer_params.get('prayer'), prayer_time,prayer_params.get('city'))
        server_response = {
            "speech": speech,
        }
      else:
        print 'Could not find relevant context..'
    else:
      server_response = {
          "speech": "Sorry, Prayer Pal cannot process this request." \
          " Please try again later.",
      }

    print 'server response = ', server_response
    return util.JsonResponse(server_response)


@app.route('/auth', methods=['GET'])
def authenticate():
  redirect_uri = request.args.get('redirect_uri')
  state = request.args.get('state')
  access_token = token_generator.generate()
  full_redirect_uri = '{}#access_token={}&token_type=bearer&state={}'.format(redirect_uri, access_token, state)

  print 'FULL REDIRECT URI: ', full_redirect_uri

  return redirect(full_redirect_uri)

@app.route('/privacy', methods=['GET'])
def render_privacy():
  return render_template('privacy.html')


if __name__ == '__main__':
    #port = int(os.getenv('PORT', 5000))

    #print("Starting app on port %d" % port)

    # use this for heroku deployments.
    #app.run(debug=True, port=port, host='0.0.0.0')
    app.run()
