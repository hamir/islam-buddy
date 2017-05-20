import json
from flask import make_response


def json_response(response_dict):
  """Constructs a JSON response object."""
  response = make_response(json.dumps(response_dict, indent=4))
  response.headers['Content-Type'] = 'application/json'
  return response


def json_error(error_text):
  """Constcuts a JSON response from an error."""
  response = make_response(json.dumps({'error': error_text}, indent=4))
  response.headers['Content-Type'] = 'application/json'
  return response
