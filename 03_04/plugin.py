#Import the needed libraries
import requests
import json
from flask import Flask, send_from_directory
from datetime import datetime

#Initialize the Flask app
app = Flask(__name__)

# API used to check for asteroids headed toward Earth
# Documentation: https://api.nasa.gov/
NASA_URL = "https://api.nasa.gov/neo/rest/v1/feed"
NASA_API_KEY = "DEMO_KEY" #replace with your key

# JSON helper function
def stringToJSON(message, count):
    #json string data
    asteroid_string = '{"count":' + count + ', "message": "' + message + '"}'

    return asteroid_string

# Default route populated to show things are working when we deploy and test
@app.route("/")
def index():
    return "Your plugin is working"

# This route contains the core functionality to see if dangerous asteroids are headed toward Earth
# This calls the Asteroids - NeoWs (Near Earth Object Web Service)
# Local test: http://127.0.0.1:5000/danger

@app.route('/danger', methods=['GET'])
def in_danger():
  try:
    today = datetime.today().strftime('%Y-%m-%d')
    params = {"start_date": today, "end_date": today, "api_key": NASA_API_KEY}

    response = requests.get(NASA_URL, params=params)
    api_data = response.json()

    message = "No asteroids headed toward Earth."

    for key in api_data:
      if key == 'is_potentially_hazardous_asteroid' and api_data[key] == True: 
          message = "Dangerous asteroid(s) headed toward Earth. Take cover." 
      else:
          message = "Asteroids headed toward Earth but none of them pose any danger."

    #convert string to  object
    json_object = json.loads(stringToJSON(message, get_asteroid_count()))
  except:
    return "The NASA API, NeoWs (Near Earth Object Web Service), is currently down. Please try your request again later."
  return json_object

# This route returns the count of how many asteroids (dangerous + non-dangerous) are headed toward Earth
# This calls the Asteroids - NeoWs (Near Earth Object Web Service)
# Local test: http://127.0.0.1:5000/count
@app.route('/count', methods=['GET'])
def get_asteroid_count():
  today = datetime.today().strftime('%Y-%m-%d')
  params = {"start_date": today, "end_date": today, "api_key": NASA_API_KEY}

  response = requests.get(NASA_URL, params=params)
  api_data = response.json()

  return str(len(api_data))
