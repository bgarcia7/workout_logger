from pymongo import MongoClient
import requests
import json

db_client = MongoClient()
db = db_client['brandon_workout_db']
users = db['users']

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

def update(to_update, updated_state):
	users.update(to_update, updated_state)

def get_info(user, message):

	user_id = user["user_id"]
	text = message["text"].lower().strip()

	return user_id, text