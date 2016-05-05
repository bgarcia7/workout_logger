from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import abort
from flask import make_response
from flask import redirect
from flask import g 

import requests
import redis
from pymongo import MongoClient
import json
import jinja2
import os
import sys

#=====[ Sets up directories  ]=====
base_dir = os.path.split(os.path.realpath(__file__))[0]
static_dir = os.path.join(base_dir, 'static')

#=====[ Initializes app  ]=====
app = Flask(__name__)
	# , static_folder=static_dir)

#=====[ Access token ]=====
token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
os.system('curl -ik -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=' + token + '"')

#=====[ Connect to REdis ]=====
# redis_conn = redis.StrictRedis(host='localhost', port=6379)

#=====[ Instantiate DB Client ]=====
db_client = MongoClient()
# db = db_client['health_db_dogfood']
db = db_client['workout_db']
users = db['users']
users.remove()
users = db['users']

@app.route("/receive_message",methods=['POST', 'GET'])
def webhook():
	""" Webhook used to receive message from a user messaging the Health Advisor FB page """

	resp = make_response('OK', 200)

	try:
		#=====[ user for verification ]=====
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

				user_id = message_obj['sender']['id']
				send_response('Andale, guey!',user_id)

		return resp

	except Exception as e:
		print e

def process_message(message_obj):
	""" 
	1. figure out the user
	2. states: in workout / idle / intro
	    a. intro -> say 'start workout' / 'end workout'
	    b. in workout -> time of exercise, exercise, reps, weight
	    c. idle -> waiting for 'start workout' respond to everything to tell me to start tracking.
	"""

	user_id = message_obj['sender']['id']

	#=====[ Check if message is a standard message or postback (from template) ]=====
	if 'message' in message_obj:
		message = message_obj['message']
	else:
		message = {'text': message_obj['postback']['payload']}

	
	#=====[ Find user in db ]=====
	user = users.find_one({"user_id": user_id})
	
	#=====[ Add message to existing user database or add new user ]=====
	if not user:
		#=====[ Create new user ]=====
		users.insert_one({"user_id":user_id, "messages":[{"timestamp":timestamp, "message":message}],"profile":{}, "status": ("name",1), "food_collection":{}, "last_food_collection":0})		
		# user = users.find_one({"user_id":user_id})
		# goals.ask(user, user_id)
		ut.send_response(responses.welcome_message, user_id)
		return
	else:
		user['messages'].append({"timestamp":timestamp, "message":message})
		users.update({"user_id":user_id}, user)

	#=====[ Formulates and sends response ]=====
	respond(message, user)

def send_response(message, F):
		
	try:

		#=====[ Data contains facebook specific json format ]=====
		data = json.dumps({"recipient": {"id": user_id}, "message": {"text": message}})

		#=====[ URL is to a general facebook messenger bot endpoint + access_token ]=====
		url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + token 

		#=====[ Construct headers ]=====
		headers = {"Content-Type": "application/json"}

		#=====[ Make request and get response ]=====
		response = requests.post(url=url.strip(), data=data, headers=headers)


	except Exception as e:
		print e


#=====[ Runs app on running server.py ]=====
if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80)

