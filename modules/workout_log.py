import utils as ut
import datetime
from responses import *
import re
import pickle
from classes.workout import Workout
from classes.subroutine import Subroutine
from classes.xset import xSet

def start(user):
	""" Initializes users workout fields """

	user_id = user.get_id()

	#=====[ Start workout ]=====
	user.status ="workout"
	user.current_workout = Workout()
	ut.update(user_id, user)

	ut.send_response(START_WORKOUT_MESSAGE, user_id)

def process(user, message):

	user_id, text = ut.get_info(user, message)
	workout = user.current_workout

	#=====[ End Workout ]=====
	if "end" in text and "workout" in text:

		end_workout(user, user_id, workout)
		ut.send_response(workout.get_summary(), user_id)

	#=====[ If starting a new circuit ]=====
	elif "circuit" in text:

		#=====[ Get exercises for circuit ]=====
		exercises = [x.strip() for x in (text.split(':')[1]).split(',')]

		#=====[ If currently in a subroutine, add to workout ]=====
		if workout.curr_subroutine:
			workout.add_subroutine(workout.curr_subroutine)

		#=====[ Making new subroutine in workout ]=====
		workout.new_subroutine('circuit', exercises)

		user.curr_workout = workout 
		ut.update(user_id, user)

	#=====[ Extract exercise ]=====
	else:

		curr_set = extract_exercise(text)

		#=====[ Update current workout if exercise extracted ]=====
		if curr_set:

			curr_subroutine = workout.curr_subroutine

			if curr_subroutine and (not curr_set.exercise or curr_subroutine.has_exercise(curr_set.exercise)):
			#=====[ If we're in the middle of an existing subroutine ]=====

				curr_subroutine.add_set(curr_set)

			#=====[ Beginning a new subroutine ]=====s
			else:

				if curr_subroutine:
					workout.add_subroutine(curr_subroutine)

				workout.new_subroutine('exercise', [curr_set.exercise], curr_set)

			user.current_workout = workout

			ut.update(user_id, user)
			ut.send_response("Cool!", user_id)

		#=====[ If no exercise extracted, notify user ]=====
		else:

			ut.send_response(NO_EXERCISE_EXTRACTED_MESSAGE, user_id)


def extract_exercise(text):
	""" Extracts reps, exercise and weight from text """

	full_reg = r'(\d+) ?reps( of )?(.+)( at ?| ?@ ?)(\d+)'
	no_weight_reg = r'(\d+) ?reps( of )?(.+)'
	no_ex_reg = r'(\d+) ?rep(s)?( at ?| ?@ ?)(\d+)'
	no_ex_weight_reg = r'(\d+) ?rep(s)?'

	#=====[ Check if reps extracted ]=====
	if re.search(full_reg, text):
		
		#=====[ Get matches ]=====
		matches = re.search(full_reg, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		exercise = matches.group(3)
		weight = matches.group(5)

	elif re.search(no_ex_reg, text):

		#=====[ Get matches ]=====
		matches = re.search(no_ex_reg, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		weight = matches.group(4)
		exercise = None

	elif re.search(no_weight_reg, text):

		#=====[ Get matches ]=====
		matches = re.search(no_weight_reg, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		exercise = matches.group(3)
		weight = None

	elif re.search(no_ex_weight_reg, text):

		#=====[ Get matches ]=====
		matches = re.search(no_ex_weight_reg, text)

		#=====[ Extract reps, exercise and weight ]=====
		reps = matches.group(1)
		weight = None
		exercise = None

	else:
		return None

	return xSet(exercise, weight, reps)

def end_workout(user, user_id, workout):

	#=====[ Record current workout and end time. Update user ]=====
	workout.end()

	#=====[ Add workout to list of past workouts and put in idle mode ]=====
	user.add_workout(workout)
	user.current_workout = None
	user.status = "idle"
	
	ut.update(user_id, user)
	ut.send_response(END_WORKOUT_MESSAGE, user_id)

