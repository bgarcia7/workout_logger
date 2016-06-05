from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import abort
from flask import make_response
from flask import redirect

import requests
import redis
import pymongo
import json
import jinja2
import os
import sys

#=====[ Sets up directories  ]=====
base_dir = os.path.split(os.path.realpath(__file__))[0]
static_dir = os.path.join(base_dir, 'static')

#=====[ Initializes app  ]=====
app = Flask(__name__)

os.system('curl -ik -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=' + token + '"')
redis_conn = redis.StrictRedis(host='localhost', port=6379)

@app.route("/receive_message",methods=['POST', 'GET'])
def webhook():
	""" Webhook used to receive message from a user messaging the Workout Logger page """

	resp = make_response('OK', 200)

	try:
		#=====[ use for verification ]=====
		# return make_response(request.args['hub.challenge'])
		#=====[ Extract messaging events from json in request ]=====
		if 'entry' in request.json and 'messaging' in request.json['entry'][0]:
				messaging_events = request.json['entry'][0]['messaging']

		else:
			return resp

		#=====[ Iterate through messages and add to queue ]=====
		for message_obj in messaging_events:

			#=====[ Checks to make sure message is not delivery receipt ]=====
			if 'delivery' not in message_obj:
				
				redis_conn.rpush('queue', str(message_obj))

		return resp

	except Exception as e:
		print e


#=====[ Runs app on running server.py ]=====
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80)

