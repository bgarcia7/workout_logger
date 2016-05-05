from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import abort
from flask import make_response
from flask import redirect

import re
import math
import time 
import requests
import redis
import json
import jinja2
import os
import sys
import ast
import datetime
import sys

from pymongo import MongoClient
from nltk.corpus import stopwords

sys.path.append('modules/')
import intro
import idle
import workout
import command 

#=====[ Access token ]=====
token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
os.system('curl -ik -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=' + token + '"')

#=====[ Set up Redis server ]=====
redis_conn = redis.StrictRedis(host='localhost', port=6379)

#=====[ Set up Mongo DB ]=====
db_client = MongoClient()

db = db_client['brandon_workout_db']
users = db['users']
users.remove()
users = db['users']

def run():
	""" Continually pings redis to process any and all queued messages """

	while(True):

		try:
			q_len = redis_conn.llen('queue')
			if q_len >= 1:

				#=====[ Rehydrate dictionary of information from redis ]=====
				message_obj = ast.literal_eval(redis_conn.rpop('queue'))

				#=====[ Process message (store info) and formulate appropriate response ]=====
				process_message(message_obj)

			else:
				#=====[ If no messages to process, sleep ]=====
				time.sleep(1)

		except Exception as e:
			print "Error in Messenger.py/run:", str(e)



def process_message(message_obj):
	
	""" Processes a message:
		
		Step 1: Finds user in database or creates new user
		Step 2: Store raw message object in database
		Step 3: Formulate response 

	"""
	#=====[ Extract user_id and timestamp for inserting into db ]=====
	user_id = message_obj['sender']['id']	
	timestamp = datetime.datetime.now()
	
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
		user = {"user_id":user_id, "messages":[{"timestamp":timestamp, "message":message}],"workouts":[],
		        "current_workout":None, "status": "intro"}
		users.insert_one(user)
	else:
		user['messages'].append({"timestamp":timestamp, "message":message})
		users.update({"user_id":user_id}, user)

	#=====[ Formulates and sends response ]=====
	respond(message, user)



def respond(message, user):
	""" 
		Step 1: Extracts relevant info from user message 
		Step 2: Evaluate user status
		Step 3: send appropriate response 
	"""

	status = user["status"]

	if command.process(user, message):
		return

	if status == "intro":
		intro.process(user, message)

	elif status == "idle":
		idle.process(user, message)

	elif status == "workout":
		workout.process(user, message)



#=====[ Runs app on running server.py ]=====
if __name__ == "__main__":
	run()

