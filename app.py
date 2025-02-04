#!/usr/bin/env python3
# Flask auth with HTTP '$ pip install flask_httpauth'
# For https '$ pip install Flask-SSLify'

from flask import Flask, jsonify, make_response, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
from json import loads, dumps
import requests

from werkzeug.security import generate_password_hash, \
    check_password_hash

from status.diskusage import diskUsage
from status.uptime import timeSinceBoot
from status.load import load
from status.cpuTemp import getCpuTemp

from plex.tmdb import tmdbSearch
from plex.plexSearch import plexSearch

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

# Hardcoded users, the password is hashed with salt used by wekzeug
users = {
    "kevin": "9f6c79bbb3b8bbc4e6aab32314afaf3c812df66b",
    "apollo": "BerryTree",
    "test": "test"
}

tmdbBaseURL = "https://api.themoviedb.org/3/"

# Flask function for checking password sent with http request
# @auth.verify_password
# def verify_password(email, password):
#     return verifyHash(password)

# # Costum function for hashing and verifying the sent password.
# # TODO Read if ok to send in cleartext like this if use https
# def verifyHash(pw):
#   pw_hash = generate_password_hash(pw)
#   return check_password_hash(pw_hash, pw)

# Flask function for getting password matching username sent by http request
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# Flasks own error handler that makes and returns error 401 if creds
# to not match.
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'errors': 'Unauthorized access'}), 401)

# This would be replaced with a database, but single process and thread
# can use local data like this for simplicity.


# Want all return data to be JSON so create custom error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'errors': 'Not found'}), 404)
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'errors': 'Bad request'}), 400)


# --- Apollo Activity --- #
@app.route('/api/v1/load', methods=['GET'])
def get_load():
    return jsonify(load())


@app.route('/api/v1/disks', methods=['GET'])
def get_diskUsage():
    return jsonify(diskUsage(request.args.get('dir')))


@app.route('/api/v1/uptimes', methods=['GET'])
def get_uptimes():
    return jsonify({ 'uptime': timeSinceBoot() })

@app.route('/api/v1/temps', methods=['GET'])
def get_temps():
    return  jsonify(getCpuTemp())


# TODO PLEX
# Search, watching, +photo
@app.route('/api/v1/plex/request', methods=['GET'])
def get_movieRequest():
	query = request.args.get("query")
	if (query != None):
		# TODO if list is empty
		return jsonify(tmdbSearch(query))

	else: return jsonify({ "errors": "Query not defined." })

@app.route('/api/v1/plex/movies', methods=['GET'])
def getPlexMovies():
    title = request.args.get('title')

    movieInfo = plexSearch(title)
    if movieInfo != None:
        print(movieInfo)
        return jsonify(movieInfo)

    abort(500)

@app.route('/api/v1/plex/watchings', methods=['GET'])
@auth.login_required
def getPlexWatchings():
    r = requests.get('http://10.0.0.41:32400/status/sessions')

    return r.text
    movieInfo = getSpecificMovieInfo(title)
    if movieInfo != None:
        return jsonify(movieInfo)



if __name__ == '__main__':
		app.run(host="0.0.0.0",port=63590, debug=True)

