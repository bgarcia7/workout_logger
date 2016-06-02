import utils as ut
import datetime 
from resources import *

def process(user, message, instructions=False):
	""" Introduces a user to the workout chatbot and to logging workouts """

	user_id, text, status_state = ut.get_info(user, message, True)

	if status_state == 0:

		#=====[ Send introduction messages to user ]=====
		ut.send_response(WELCOME_MESSAGE, user_id)
		ut.send_response(COMMAND_INTRO, user_id)
		ut.send_response(WORKOUT_INTRO, user_id)

		user.status_state == 1

	#=====[ Begins teaching a user how to log a workout ]=====	
	elif status_state == 1:

		#=====[ Check if user said yes to learning about working out ]=====
		for word in yes_words:			
			if word in text:
				instructions = True
				break

		if instructions:
			#=====[ Send instructions for starting workout, logging sets, and ask if they want to learn about logging circuits ]=====
			ut.send_response(WORKOUT_START_INSTRUCTIONS, user_id)
			ut.send_response(WORKOUT_SET_INITIALIZATION, user_id)
			ut.send_response(WORKOUT_SET_CONTINUATION, user_id)
			ut.send_response(WORKOUT_TIMER, user_id)
			ut.send_response(LEARN_ABOUT_CIRCUITS, user_id)

			user.status_state == 2

		else:
			
			user.status = "idle"
			user.status_state = 0
			ut.send_response(DONE_INSTRUCTIONS, user_id)

	#=====[ Processes message when user is learning about logging workouts. Currently, just checks to see if user wants to learn 
	#=====[ about logging circuits ]=====
	elif status_state == 2:

		#=====[ Update user into idle mode regardless of whether they wish to learn about circuits or not ]=====
		user.status = "idle"
		user.status_state = 0
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

	ut.update(user_id, user)

