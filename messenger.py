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
import pickle

from pymongo import MongoClient
from nltk.corpus import stopwords

sys.path.append('classes')
from user_class import User

sys.path.append('modules/')
import intro
import idle
import workout_log
import feedback
import command 
import logger_intro
import utils as ut
from database import users
from resources import *


#=====[ Access token ]=====
token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
kelvin_token = 'EAAak1FpgZAygBAFkr1NOD2DJUwL4r3j74VScIDCMmW4bpBvfnoQi1VmS1KvZCFM0yooJ7Sisg8IUcioQReVAFt25RwberE8olwX8Vsre412IaNdc07fV4GDYIS4bsil4dJmRtp2r6nud8I8SeOGB8R6IO1I8E1td8QljAQNwZDZD'

os.system('curl -ik -X POST "https://graph.facebook.com/v2.6/me/subscribed_apps?access_token=' + token + '"')

#=====[ Set up Redis server ]=====
redis_conn = redis.StrictRedis(host='localhost', port=6379)

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
	user_id, timestamp, message = ut.extract_obj_info(message_obj)

	#=====[ Find user in db ]=====
	user = users.find_one({"user_id": user_id})

	#=====[ Add message to existing user database or add new user ]=====
	if not user:

		#=====[ Create new user ]=====
		user = User(user_id)
		users.insert_one({"user_id":user_id, "user_object": pickle.dumps(user)})
	
	else:
		user = pickle.loads(user["user_object"])
		
	#=====[ Store message in user object ]=====
	user.add_message(message)

	#=====[ Formulates and sends response ]=====
	respond(message, user)


def respond(message, user):
	""" 
		Step 1: Extracts relevant info from user message 
		Step 2: Evaluate user status
		Step 3: send appropriate response 
	"""

	try:

		status = user.status

		if command.process(user, message):
			return

		if status == "intro":
			intro.process(user, message)

		elif status == "idle":
			idle.process(user, message)

		elif status == "workout":
			workout_log.process(user, message)

		elif status == "feedback":
			feedback.process(user, message)
		
		elif status == "logger_intro":
			logger_intro.process(user, message)

	#=====[ If error caught, send user an error message and keep in same state ]=====
	except Exception as e:
		print e
		ut.send_response(ERROR_MESSAGE, user_id)


#=====[ Runs app on running server.py ]=====
if __name__ == "__main__":
	run()

