"""Main app file."""

#!/usr/bin/env python
import json
import util

from flask import Flask, request, render_template, redirect
from oauth2.tokengenerator import URandomTokenGenerator

from db import Database
from prayer_info import PrayerInfo
from intent_handler import IntentHandler


# pylint: disable-msg=C0103
app = Flask(__name__)
_prayer_info = PrayerInfo()
_db = Database()
_token_generator = URandomTokenGenerator(20)
_intent_handler = IntentHandler(_prayer_info, _db)


@app.route('/')
def home():
    """GET handler for home page."""
    return 'Welcome to the Islam Buddy API!'


@app.route('/table', methods=['GET'])
def table():
    id = request.args.get('id')
    command = request.args.get('command')
    response = {}
    if command == 'add':
        response = 'add is disabled'
        """
    _db.AddOrUpdateUser(id, {
        'user_info': {'foo': id},
        'city': request.args.get('city')
    })
    response = 'user ', id, ' was added'
    """
    elif command == 'get':
        response = _db.GetUser(id)
    elif command == 'delete':
        _db.DeleteUser(id)
        response = 'user ', id, ' was deleted'
    return util.JsonResponse(response)


@app.route('/salah', methods=['POST', 'GET'])
def salah():
    """GET and POST handler for /salah page."""
    if request.method == 'GET':
        #print 'received GET request'
        params = {
            'lat': request.args.get('lat'),
            'lng': request.args.get('lng'),
            'prayer': request.args.get('prayer'),
        }
        #print 'params = ', params

        if not params.get('lat') or not params.get('lng'):
            return util.JsonError('Please provide a lat and lng.')

        prayer_times = \
            PrayerInfo.GetPrayerTimes(params.get('lat'), params.get('lng'), None)
        if prayer_times == {}:
            return util.JsonResponse(
                "Error, the latitude and longitude entered might be wrong..")

        # convert from map<PrayerTime, string> to map<string, string>
        output_prayer_times = {}
        for key in prayer_times:
            output_prayer_times[util.GetPrayerKeyName(key)] = prayer_times[key]

        return util.JsonResponse(output_prayer_times)

    elif request.method == 'POST':
        post_params = request.get_json(silent=True, force=True)
        #print 'post_params = \n', json.dumps(post_params, indent=2)

        post_intent_name = post_params.get('result').get('metadata').get(
            'intentName')

        if post_intent_name in IntentHandler.INTENTS_HANDLED:
            server_response = _intent_handler.HandleIntent(post_params)
        elif post_intent_name == 'CLEAR_LOCATION':
            user_id = post_params.get('originalRequest').get('data').get('user').get(
                'userId')
            _db.DeleteUser(user_id)
            server_response = {
                "speech": "OK, your location has been cleared.",
            }
        else:
            server_response = {
                "speech": "Sorry, Prayer Pal cannot process this request."
                          " Please try again later.",
            }

        #print 'hi'
        #print 'response = ', server_response
        return util.JsonResponse(server_response)


@app.route('/auth', methods=['GET'])
def authenticate():
    """Authentication handler."""
    redirect_uri = request.args.get('redirect_uri')
    state = request.args.get('state')
    access_token = _token_generator.generate()
    full_redirect_uri = '{}#access_token={}&token_type=bearer&state={}'.format(
        redirect_uri, access_token, state)

    #print 'FULL REDIRECT URI: ', full_redirect_uri

    return redirect(full_redirect_uri)


@app.route('/privacy', methods=['GET'])
def render_privacy():
    """Privacy handler."""
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run()
