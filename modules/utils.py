import sys
sys.path.append('../classes')

from pymongo import MongoClient
import requests
import json
import pickle
import datetime
import re
from database import users
from xset import xSet


PACKAGE_LENGTH = 300
token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
kelvin_token = 'EAAak1FpgZAygBAFkr1NOD2DJUwL4r3j74VScIDCMmW4bpBvfnoQi1VmS1KvZCFM0yooJ7Sisg8IUcioQReVAFt25RwberE8olwX8Vsre412IaNdc07fV4GDYIS4bsil4dJmRtp2r6nud8I8SeOGB8R6IO1I8E1td8QljAQNwZDZD'
test_token = 'EAAYjxWLX4AUBAG8W5qtCZBhmaNulNn2CtlsFP4ppNZCgiygOrafREWsLFDWZChDQ27fUMs7jpKyt5I56n8Q76ESlORNnOjYYZCIOAZCp5sHhZBIBkZCDeZBi5Yr1uiLNVlZB1WxfYx1vz8ZC9x9WYAelh4vQnz2rZCZAB9EkX5eBoFoRpAZDZD'


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
			url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + token 

			#=====[ Construct headers ]=====
			headers = {"Content-Type": "application/json"}

			#=====[ Make request and get response ]=====
			response = requests.post(url=url.strip(), data=data, headers=headers)

		except Exception as e:
			print e

def send_button_confirm_response(message, user_id):

	try:
	
		buttons = [
					{'type':'postback','title':'no','payload':'no'}, \
					{'type':'postback','title':'yes','payload':'yes'}
					]

		#=====[ Data contains facebook specific json format ]=====
		data = {"recipient":{ "id": user_id}, "message":{ "attachment":{ "type":"template", "payload":{ "template_type":"button", "text": message, "buttons":buttons  }}}}

		data = json.dumps(data)

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


def get_info(user, message, state=False):
	""" Returns user information """

	text = message["text"].lower().strip()

	if state:
		return user.id, text, user.status_state
	else:
		return user.id, text


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

def extract_exercise(text):
	""" Extracts reps, exercise and weight from text """
	
	regexes = [
			#=====[ rep regex ]=====
			[{'reg_str':r'(\d+) ?(reps)?(at ?|@ ?)?(of)?', 'match':1}], 
			#=====[ exercise regex ]=====
			[{'reg_str':r'(\d+) ?reps( of )?([^\d]+)( at ?| ?@ ?)(\d+)', 'match': 3}, 
			 {'reg_str':r'(\d+) ?reps (of|at|@) ([^\d]+)', 'match': 3},
			 {'reg_str':r'(\d+) ?((min(ute)?s?)|(sec(ond)?s?)|(h(ou)?rs?))( of )?([^\d]+)( at ?| ?@ ?)(\d+)', 'match':10},
			 {'reg_str':r'(\d+) ?((min(ute)?s?)|(sec(ond)?s?)|(h(ou)?rs?)) ?(of|at|@) ?([^\d]+)', 'match':10}], 
			#=====[ weight regex ]=====
			[{'reg_str': r'(at ?|@ ?|of ?)(\d+)', 'match': 2}],
			#=====[ note regex ]=====
			[{'reg_str': r'note:(.+)', 'match':1}]]

	values = []

	#=====[ Search for each exercise parameters (weight, reps, exercise) ]=====
	for idx, reg_array in enumerate(regexes):

		value_found = False

		#=====[ Iterate through each regex for a particular parameter ]=====
		for reg in reg_array:

			reg_str = reg['reg_str']

			#=====[ Search for regext in string ]=====
			if re.search(reg_str, text):

				value_found = True
				values.append(re.search(reg_str, text).group(reg['match']))
				break

		#=====[ Return None if no reps extracted ]=====
		if not value_found:
			if idx == 0:
				return None

			values.append(None)

	#=====[ Returns xSet object constructed from extracted reps, exercise, and weight ]=====
	return xSet(values[1], values[2], values[0], values[3])

def extract_int(text):
	
	number = None

	#=====[ regex to extract weight ]=====
	regex = r"\d+"

	if re.search(regex,text):

		match = re.search(regex, text)

		#=====[ Store weight ]=====
		number = int(match.group(0))
		
	return number
