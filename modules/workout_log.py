import utils as ut
import datetime
from resources import *
import re
import pickle
import sys
sys.path.append('classes/')
from workout import Workout
from subroutine import Subroutine
from xset import xSet
from workout_guider import WorkoutGuider
# from spider import *

GUIDED_WORKOUT = 1
FREE_WORKOUT = 0

def start(user, workout_template=None):
	""" Initializes users workout fields """

	user_id = user.get_id()
	
	user.time = datetime.datetime.now()
	user.status ="workout"

	#=====[ Updates user status state depending on whether workout is guided for free, manual entry ]=====
	if workout_template:
		user.status_state = GUIDED_WORKOUT
		user.workout_guider = WorkoutGuider(user_id, workout_template)

		#=====[ START GUIDED WORKOUT ]=====
	
	else:
		user.current_workout = Workout()
		user.status_state = FREE_WORKOUT
		ut.send_response(START_WORKOUT_MESSAGE, user_id)

	ut.update(user_id, user)


def process(user, message):

	user_id, text, status_state = ut.get_info(user, message, state=True)
	workout = user.current_workout if user.status_state == FREE_WORKOUT else user.workout_guider.workout

	#=====[ End Workout ]=====
	if "end" in text and "workout" in text:

		#=====[ Record current workout and end time. Update user ]=====
		workout.end()

		ut.send_response(END_WORKOUT_MESSAGE, user_id)

		#=====[ Send workout summary, stats, and spider chart ]=====
		ut.send_response(workout.get_summary(), user_id)
		ut.send_response(workout.get_stats(), user_id)

		ut.send_response(workout.summarize_muscle_groups(4), user_id)

		# if generate_spider(user_id, dict(workout.muscle_groups.most_common(4))):
		# 	ut.send_response('Check out the muscles you targeted:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)

		#=====[ After calling get_summary and updating workout stats, save workout ]=====
		end_user_workout(user, user_id, workout)


	#======================================================================================#
	#																				       #
	#               		 Code for Manually loggin ad-hoc workout 		   			   #
	#																					   #
	########################################################################################

	elif status_state == FREE_WORKOUT:

		#=====[ If starting a new circuit ]=====
		if "circuit" in text:

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

			curr_set = ut.extract_exercise(text)

			#=====[ Update current workout if exercise extracted ]=====
			if curr_set:
				log_set(curr_set, workout, user, user_id)

			#=====[ If no exercise extracted, notify user ]=====
			else:

				ut.send_response(NO_EXERCISE_EXTRACTED_MESSAGE, user_id)

	#======================================================================================#
	#																				       #
	#                		Code for logging guided workout 							   #
	#																					   #
	########################################################################################

	elif status_state == GUIDED_WORKOUT:

		workout_guider = user.workout_guider

		#=====[ Log set and move to next set in workout ]=====
		next_set = workout_guider.process(text, user, user_id)

		# status will be None if there is no next set do
		status = True

		# process returns whether we should move on to next set
		if next_set:
			status = workout_guider.next_set(user_id) if next_set else True

		# If there is no next set, the workout guider is done and None will be returned so we should end the workout
		if not status:
			# TODO: This code is duplicated from above. Factor out to helper
			#=====[ Record current workout and end time. Update user ]=====
			workout.end()

			ut.send_response(END_WORKOUT_MESSAGE, user_id)

			#=====[ Send workout summary, stats, and spider chart ]=====
			ut.send_response(workout.get_summary(), user_id)
			ut.send_response(workout.get_stats(), user_id)

			ut.send_response(workout.summarize_muscle_groups(4), user_id)
			end_user_workout(user, user_id, workout)
			# END TODO

			workout_guider = None

		user.workout_guider = workout_guider
		ut.update(user_id, user)



	
def end_user_workout(user, user_id, workout):

	#=====[ Add workout to list of past workouts and put in idle mode ]=====
	user.add_workout(workout)
	user.current_workout = None
	user.status = "idle"
	
	ut.update(user_id, user)

def log_set(curr_set, workout, user, user_id):
	curr_subroutine = workout.curr_subroutine
					
	if curr_subroutine and (not curr_set.exercise or curr_subroutine.has_exercise(curr_set.exercise)):
	#=====[ If we're in the middle of an existing subroutine ]=====

		workout.add_set(curr_set)

	#=====[ Beginning a new subroutine ]=====s
	else:

		if curr_subroutine:
			workout.add_subroutine(curr_subroutine)

		workout.new_subroutine('exercise', [curr_set.exercise], curr_set)

	user.current_workout = workout
	
	cur_time = datetime.datetime.now()
	seconds_passed = int((cur_time - user.time).total_seconds())
	ut.send_response(str(seconds_passed)+ " seconds since your last log", user_id)

	user.time = cur_time
	ut.update(user_id, user)
