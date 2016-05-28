from pymongo import MongoClient
import requests
import json
import pickle
import datetime
from database import users

PACKAGE_LENGTH = 300
token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
kelvin_token = 'EAAak1FpgZAygBAFkr1NOD2DJUwL4r3j74VScIDCMmW4bpBvfnoQi1VmS1KvZCFM0yooJ7Sisg8IUcioQReVAFt25RwberE8olwX8Vsre412IaNdc07fV4GDYIS4bsil4dJmRtp2r6nud8I8SeOGB8R6IO1I8E1td8QljAQNwZDZD'


def send_response(message, user_id):
	""" Constructs the request and sends a message to the user corresponding to the specified user id """

	#=====[ Checks to make sure more bytes to send ]=====
	while len(message) > 0:

		try:			
			#=====[ Checks if message needs to be split before sending ]=====
			if len(message) <= PACKAGE_LENGTH:
				to_send = message 
				message = ''
			else:
				to_send, message = split_message(message)

			#=====[ Data contains facebook specific json format ]=====
			data = json.dumps({"recipient": {"id": user_id}, "message": {"text": to_send}})

			#=====[ URL is to a general facebook messenger bot endpoint + access_token ]=====
			url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + kelvin_token 

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

def split_message(message):
	""" Finds appropriate cutting point for sending message. Returns the message to send and remaining message """

	to_send = message[:PACKAGE_LENGTH]
	message = message[PACKAGE_LENGTH:]

	#=====[ Check if newline character found ]=====
	index = to_send.rfind('\n')
	if index > 0:
		message = to_send[index:] + message
		to_send = to_send[:index]
	else:

		#=====[ If no newline found, check if space found ]=====
		index = to_send.rfind(' ')
		if index > 0:
			message = to_send[index:] + message
			to_send = to_send[:index]

	return (to_send, message)

def remove_user(user_id):
	""" Removes user from the database """

	users.remove({"user_id":user_id})
