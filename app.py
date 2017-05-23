#!/usr/bin/env python
import os
import pprint
import json

from flask import Flask, request, make_response
from prayer_info import PrayerInfo
import util
from common import DailyPrayer
import response_builder 


app = Flask(__name__)
prayer_info = PrayerInfo()


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
    print 'post_params = ', pprint.pprint(post_params)

    device_params = post_params.get('originalRequest').get('data').get('device')
    # this needs to be less hacky - @hamdy maybe a request extractor class?
    # we need a request extractor class
    print 'intent_name = ', post_params.get('result').get('metadata').get('intentName') 
    if (post_params.get('result').get('metadata').get('intentName') 
        == 'WHEN_IS_START_TIME_INTENT' and 'location' not in device_params):
      print 'Could not find location in request, so responding with a permission request.'
      server_response = response_builder.RequestLocationPermission()
    else:
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
        }

        all_prayer_times = \
            prayer_info.GetPrayerTimes(
                prayer_params.get('lat'),
                prayer_params.get('lng'))

        prayer_time = \
            all_prayer_times.get(util.StringToDailyPrayer(prayer_params.get('prayer')))
        print 'prayer_times[', prayer_params.get('prayer'), "] = ", prayer_time

        # this also needs to be less hacky - @hamir maybe a json response formater class?
        speech = "The time for %s is %s." % (prayer_params.get('prayer'), prayer_time)
        server_response = {
            "speech": speech,
        }
      else:
        print 'Could not find relevant context..'

    print 'server response = ', server_response
    return util.JsonResponse(server_response)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    # use this for heroku deployments.
    #app.run(debug=False, port=port, host='0.0.0.0')
    app.run()
