import time
import utils as ut
import datetime
from resources import *
import re
import pickle
import sys
sys.path.append('classes/')
sys.path.append('modules/')
from workout import Workout
from subroutine import Subroutine
from xset import xSet
from workout_guider import WorkoutGuider
from multiprocessing import Process
import os
import signal
import feedback
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
	clear_timers(user)

	#=====[ End Workout ]=====
	if "end" in text and "workout" in text:
		
		end_user_workout(user, user_id, workout)
		feedback.start(user)

	#======================================================================================#
	#																				       #
	#               		 Code for Manually loggin ad-hoc workout 		   			   #
	#																					   #
	########################################################################################

	elif status_state == FREE_WORKOUT:

		#=====[ If user is moving on to next exercise ]=====
		if ('done' in text or 'end' in text) and ('exercise' in text or 'circuit' in text):

			workout.add_subroutine(workout.curr_subroutine)

			total_seconds = workout.curr_subroutine.get_total_set_time()
			time = str(int(total_seconds/60)) + ' min ' + str(total_seconds % 60) + ' sec' if total_seconds > 60 else str(total_seconds) + ' sec'

			#=====[ Notify user of duration of previous subroutine ]=====
			ut.send_response('Your ' + ', '.join(workout.curr_subroutine.exercises) + ' exercise took you a total of ' + time, user_id)

			workout.curr_subroutine = None

			ut.update(user_id, user)

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
		cur_set_feedback_message, next_set = workout_guider.process(text, user, user_id)

		next_set_feedback_message = True

		#=====[ If there is feedback for the current set, then we were able to successfully extract a log and we move 
		#=====[ on to the next set
		end_subroutine = False
		if next_set:
			next_set_feedback_message, end_subroutine = workout_guider.next_set(user_id)

		#=====[ If there is not feedback for the next set, then that means there are no more sets to perform, and we
		#=====[ end the workout ]=====
		if not next_set_feedback_message:
			end_user_workout(user, user_id, workout)
			workout_guider = None

		elif not end_subroutine:
			message = cur_set_feedback_message.strip()if type(cur_set_feedback_message) == str else ''
			message += ' ' + next_set_feedback_message.strip() if type(next_set_feedback_message) == str else ''
			ut.send_response(message, user_id)

		user.workout_guider = workout_guider
		ut.update(user_id, user)


	
def end_user_workout(user, user_id, workout):

	print 'in end workout'
	#=====[ Clear process timers to remind user to start next set ]=====
	clear_timers(user)

	#=====[ Record current workout and end time. Update user ]=====
	if workout.end():

		ut.send_response(END_WORKOUT_MESSAGE, user_id)

		#=====[ Send workout summary, stats, and spider chart ]=====
		ut.send_response(workout.get_summary(), user_id)
		ut.send_response(workout.get_stats(), user_id)

		ut.send_response(workout.summarize_muscle_groups(4), user_id)
		#=====[ Add workout to list of past workouts and put in idle mode ]=====
		user.add_workout(workout)

	else:
		user.current_workout = None
		user.status = 'idle'
		ut.update(user_id, user)
		
		ut.send_response(NO_WORKOUT_LOGGED, user_id)
	
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
	
	
	set_timers(user_id, user)

	user.time = datetime.datetime.now()
	ut.update(user_id, user)

def clear_timers(user):
	""" Clears any processes sending timers to user once they log again """

	#=====[ Terminate each timer ]=====
	if hasattr(user, 'timer_processes'):
		for pid in user.timer_processes:
			try:
				os.kill(pid, signal.SIGTERM)
			except Exception as e:
				pass

def send_warning(user_id, message, seconds):
	""" Sends Timing warning to user for specified amount of time """

	print 'in send warning'
	time.sleep(seconds - 2)
	print 'after sleep'
	ut.send_response(message + str(seconds) + ' seconds.', user_id)

def set_timers(user_id, user):
	""" Starts a process for each timer set by a user. """

	if hasattr(user, 'timer'):
		user.timer_processes = []

		print 'setting timer'

		print user.timer
		#=====[ Start new process for each timer ]=====
		for idx, time in enumerate(user.timer):

			if idx == len(user.timer) - 1:
				p = Process(target=send_warning, args=(user_id, FINAL_TIMING_WARNING, time,))
			else:
				p = Process(target=send_warning, args=(user_id, TIMING_WARNING, time,))
			#=====[ Keep reference to process and start it ]=====
			p.start()
			user.timer_processes.append(p.pid)


		ut.update(user_id, user)

