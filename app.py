#!/usr/bin/env python
import os
import pprint
import json

from flask import Flask, request, make_response, render_template, redirect
from flask_assistant import Assistant, tell
from oauth2.tokengenerator import URandomTokenGenerator
from daily_prayer import PrayerInfo
import util
from common import DailyPrayer
import response_builder 


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
    if (post_params.get('result').get('metadata').get('intentName') 
        == 'prayer-times' and 'location' not in device_params):
      print 'Could not find location in request, so responding with a permission request.'
      server_response = {
        'data': response_builder.RequestLocationPermission(),
      }

    else:
      contexts_index = \
          next(
            index for (index, d) in \
                enumerate(post_params.get('result').get('contexts')) \
                if d["name"] == "request_permission"
          )
      try:
        contexts_index
      except NameError:
        print "Cannot fine request_permission in result.contexts in post parameters."
      else:
        prayer_params = {
         'prayer': \
             post_params.get('result') \
                 .get('contexts')[contexts_index] \
                 .get('parameters') \
                 .get('PrayerName'),
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
            "data": response_builder.RequestLocationPermission()
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
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
