from pymongo import MongoClient
import requests
import json
import pickle
import datetime
from database import users 

token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'

def send_response(message, user_id):
	""" Constructs the request and sends a message to the user corresponding to the specified user id """

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

def update(user_id, user_obj):
	""" Updates user object in mongodb """

	users.update({"user_id":user_id}, {"user_id":user_id, "user_object":pickle.dumps(user_obj)})


def get_info(user, message):
	""" Returns user information """

	text = message["text"].lower().strip()

	return user.get_id(), text


def extract_obj_info(message_obj):
	""" Extract data from message object """

	#=====[ Extract user_id and timestamp for inserting into db ]=====
	user_id = message_obj['sender']['id']	
	timestamp = datetime.datetime.now()
	
	#=====[ Check if message is a standard message or postback (from template) ]=====
	if 'message' in message_obj:
		message = message_obj['message']
	else:
		message = {'text': message_obj['postback']['payload']}
	
	return (user_id, timestamp, message)
