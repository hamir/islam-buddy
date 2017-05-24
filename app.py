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
from start_time_intent_handler import StartTimeIntentHandler

app = Flask(__name__)
prayer_info = PrayerInfo()
token_generator = URandomTokenGenerator(20)
start_time_handler = StartTimeIntentHandler(prayer_info)

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
    post_intent_name = post_params.get('result').get('metadata').get('intentName')
    print 'intent_name = ', post_intent_name

    if post_intent_name in StartTimeIntentHandler.INTENTS_HANDLED:
      server_response = start_time_handler.HandleIntent(device_params, post_params)
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
