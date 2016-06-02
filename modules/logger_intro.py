import utils as ut
from resources import *
import re
import sys

def start(user, user_id):
	""" Begins teaching a user how to log a workout """

	#=====[ Send instructions for starting workout, logging sets, and ask if they want to learn about logging circuits ]=====
	ut.send_response(WORKOUT_START_INSTRUCTIONS, user_id)
	ut.send_response(WORKOUT_SET_INITIALIZATION, user_id)
	ut.send_response(WORKOUT_SET_CONTINUATION, user_id)
	ut.send_response(WORKOUT_TIMER, user_id)
	ut.send_response(LEARN_ABOUT_CIRCUITS, user_id)

	user.status = "logger_intro"
	ut.update(user_id, user)

def process(user, message):
	""" Processes message when user is learning about logging workouts. Currently, just checks to see if user wants to learn 
		about logging circuits. """

	#=====[ Update user into idle mode regardless of whether they wish to learn about circuits or not ]=====
	user.status = "idle"
	ut.update(user_id, user)

	user_id, text = ut.get_info(user, message)

	#=====[ Check if user gave a 'yes' word. If so gives information about logging circuits ]=====
	for word in yes_words:
		
		if word in text:
		
			#=====[ Teach user how to log circuits ]=====
			ut.send_response(WORKOUT_CIRCUIT_INITIALIZATION, user_id)
			ut.send_response(WORKOUT_CIRCUIT_CONTINUATION, user_id)
			return

	#=====[ Checks if user gave a 'no' word ]=====
	for word in no_words:

		if word in text:

			ut.send_response(DONE_INSTRUCTIONS, user_id)
			return

	#=====[ If no 'yes' or 'no' word found, then just assume user doesn't want to learn about logging circuits ]=====
	ut.send_response(ASSUME_DONE_INSTRUCTIONS, user_id)
