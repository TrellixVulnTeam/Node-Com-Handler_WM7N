#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-01-28 23:21:22
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-02-08 20:29:53

from requests import get

plexBaseURL = "http://10.0.0.41:32400/"

def parsePlexWatching(obj):
	print(obj) 

def getPlexWatching():
	requestType = "status/sessions"
	header = {'Accept': 'application/json'}

	url = plexBaseURL + requestType
	response = get(url, headers=header)

	if response.status_code == 200:
		watchingObj = response.json()
		res = parsePlexWatching(watchingObj)

def plex_watching():
	# Every call saves the info of session.xml to a file named plexPlaying
	system('curl --silent 10.0.0.41:32400/status/sessions > plexPy/plexPlaying.xml')

	# XML parsing, creates a tree and saves the root node as root
	tree = ET.parse('plexPy/plexPlaying.xml')
	root = tree.getroot()

	# The root node named MediaContainer has a size variable that holds number of active processes.
	# If this is '0' then there are none playing, no need to compute.
	if (root.get('size') != '0'):

		# Get load of CPU and I/O
		return_text = '\n\t' + str(popen('cat /proc/loadavg').read())
		return_text += '\tCur: \t' + str(root.get('size')) + '\n'

		# Goes through all the 'video' elements in MediaContainer
		for video in root.findall('Video'):
			if (video.get('type') == 'movie'):
				name = video.get('title')
				return_text += '\n\tTitle: \t' + name

			elif (video.get('type') == 'episode'):
				parentName = video.get('grandparentTitle')
				name = video.get('title')
				return_text += '\n\tTitle: \t' + name + \
					'\n\tSeries: ' + parentName

			progress = "{0:0.1f}".format(float(video.find('TranscodeSession').get('progress')))
			state = video.find('Player').get('state')
			player = video.find('Player').get('platform')
			user = video.find('User').get('title')

			return_text += str('\n\tProg : \t' + str(progress) + '\n\tPlayer: ' + player + \
				'\n\tState: \t' + state + '\n\tUser: \t' + user + '\n')

		try:
			return normalize('NFKD', return_text).encode('ascii', 'ignore')
		except TypeError:
			return return_text
	else: 
		return 'Null playing'

if __name__ == '__main__':
	print(getPlexWatching())
