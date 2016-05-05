import utils as ut
import datetime
from responses import *
import re

def process(user, message):

	user_id, text = ut.get_info(user, message)
	
	#=====[ End Workout ]=====
	if "end" in text and "workout" in text:

		#=====[ Record current workout and end time. Update user ]=====
		user["current_workout"]["end_time"] = datetime.datetime.now()
		user["workouts"] += [user["current_workout"]]
		user["current_workout"] = None
		user["status"] = "idle"
		
		ut.update({"user_id": user_id}, user)
		ut.send_response(END_WORKOUT_MESSAGE, user_id)


	#=====[ Extract exercise ]=====
	else:

		reps, exercise, weight = extract_exercise(text)

		#=====[ Update current workout if exercise extracted ]=====
		if reps:

			user['current_workout']['exercises'] += [{'time':datetime.datetime.now(), 'reps':reps, 'exercise':exercise, 'weight':weight}]
			ut.update({'user_id':user_id}, user)
			ut.send_response("Cool! You just did " + str(reps) + " reps of " + str(exercise) + ' at ' + str(weight) + ' pounds!', user_id)

		#=====[ If no exercise extracted, notify user ]=====
		else:

			ut.send_response(NO_EXERCISE_EXTRACTED_MESSAGE, user_id)


def extract_exercise(text):
	""" Extracts reps, exercise and weight from text """

	regex_weight = r'(\d+) ?reps( of )?(.+)( at ?| ?@ ?)(\d+)'
	regex_no_weight = r'(\d+) ?reps( of )?(.+)'

	#=====[ Check if reps extracted ]=====
	if re.search(regex_weight, text):
		
		#=====[ Get matches ]=====
		matches = re.search(regex_weight, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		exercise = matches.group(3)
		weight = matches.group(5)

	elif re.search(regex_no_weight, text):

		#=====[ Get matches ]=====
		matches = re.search(regex_no_weight, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		exercise = matches.group(3)
		weight = ''

	else:

		return (None, None, None)

	return (reps, exercise, weight)
