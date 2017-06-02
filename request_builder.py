"""Builds JSON Requests to pass to our server."""

import json

# For follow-on queries, we get conversation_type "ACTIVE" while original queries are type "NEW".
def BuildJSON(prayer_name, raw_query, resolved_query, intent, masjid_name="", geo_city="", geo_state_us="", geo_country="", conversation_type="NEW", permission="false"):
  data = {}
  data['lang'] = 'en'
  data['status'] = {'error_type': 'success', 'code': 200}
  parameters = {}
  parameters['PrayerName'] = prayer_name
  parameters['MasjidName'] = masjid_name  
  parameters['geo-city'] = geo_city
  parameters['geo-state-us'] = geo_state_us
  parameters['geo-country'] = geo_country

  contexts = {}
  # TODO: Make the PrayerName field capitalized/canonicalized if needed.
  context_parameters = {'PrayerName.original': prayer_name, 'PrayerName': prayer_name, 'geo-city': [geo_city]}

  intent_params = {}
  if (intent == 'WHEN_IS_START_TIME_INTENT'):
    intent_params['name'] = 'google_assistant_welcome'
    intent_params['parameters'] = context_parameters
  elif (intent == 'PERMISSION_INTENT'):
    intent_params['name'] = 'actions_intent_permission'
    intent_params['parameters'] = {'PERMISSION': permission} 


  contexts = [intent_params, \
              {'name': 'requ', 'parameters': context_parameters}, \
              {'name': 'actions_capability_screen_output', 'parameters': context_parameters}, \
              {'name': 'actions_capability_audio_output', 'parameters': context_parameters}, \
              {'name': 'google_assistant_input_type_keyboard', 'parameters': context_parameters}]

  # TODO: Add other arguments as needed.
  inputs = [{'intent': intent, 'raw_inputs': [{'query': raw_query}]}]
  capabilities = [{'name': 'actions.capability.AUDIO_OUTPUT'}, {'name': 'actions.capability.SCREEN_OUTPUT'}]
  original_request_data = {'inputs': inputs, 'isInSandbox': 'true', 'surface': {'capabilities': capabilities}, 'conversation': {'type': conversation_type}}
  data['originalRequest'] = {'source': 'google', 'version':2, 'data': original_request_data}
  metadata = {'intentName': intent}
 
  data['result'] = {'parameters': parameters, 'contexts': contexts, 'resolved_query': resolved_query, 'source': 'agent', 'score': 1, 'metadata': metadata}
  json_data = json.dumps(data)
  print 'json data ', json_data
