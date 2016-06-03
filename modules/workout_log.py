import time
import utils as ut
import datetime
from resources import *
import re
import pickle
import sys
import feedback
sys.path.append('classes/')
from workout import Workout
from subroutine import Subroutine
from xset import xSet
from multiprocessing import Process
import os
import signal
# from spider import *

def start(user):
	""" Initializes users workout fields """

	user_id = user.get_id()

	#=====[ Start workout ]=====
	user.status = "workout"
	user.current_workout = Workout()
	user.time = datetime.datetime.now()
	ut.update(user_id, user)

	ut.send_response(START_WORKOUT_MESSAGE, user_id)

def process(user, message):

	user_id, text = ut.get_info(user, message)
	workout = user.current_workout

	#=====[ End Workout ]=====
	if "end" in text and "workout" in text:

		#=====[ Clear process timers to remind user to start next set ]=====
		clear_timers(user)

		#=====[ Record current workout and end time. Update user ]=====
		if workout.end():

			ut.send_response(END_WORKOUT_MESSAGE, user_id)

			#=====[ Send workout summary, stats, and spider chart ]=====
			ut.send_response(workout.get_summary(), user_id)
			ut.send_response(workout.get_stats(), user_id)

			ut.send_response(workout.summarize_muscle_groups(4), user_id)

		# if generate_spider(user_id, dict(workout.muscle_groups.most_common(4))):
		# 	ut.send_response('Check out the muscles you targeted:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)

		#=====[ After calling get_summary and updating workout stats, save workout ]=====
			end_user_workout(user, user_id, workout)

			feedback.start(user)

		#=====[ If workout was not ended successfully, then no workout is logged ]=====
		else:
			user.current_workout = None
			user.status = 'idle'
			ut.update(user_id, user)
			
			ut.send_response(NO_WORKOUT_LOGGED, user_id)


	#=====[ If starting a new circuit ]=====
	elif "circuit" in text:

		#=====[ Clear process timers to remind user to start next set ]=====
		clear_timers(user)

		#=====[ Get exercises for circuit ]=====
		exercises = [x.strip() for x in (text.split('circuit')[1]).replace(':','').split(',')]

		#=====[ If currently in a subroutine, add to workout ]=====
		if workout.curr_subroutine:

			workout.add_subroutine(workout.curr_subroutine)

			total_seconds = workout.curr_subroutine.get_total_set_time()
			time = str(int(total_seconds/60)) + ' min ' + str(total_seconds % 60) + ' sec' if total_seconds > 60 else str(total_seconds) + ' sec'

			#=====[ Notify user of duration of previous subroutine ]=====
			ut.send_response('Your ' + ', '.join(workout.curr_subroutine.exercises) + ' exercise took you a total of ' + time, user_id)

		#=====[ Making new subroutine in workout ]=====
		workout.new_subroutine('circuit', exercises)

		user.curr_workout = workout 
		ut.update(user_id, user)

	#=====[ Extract exercise ]=====
	else:

		clear_timers(user)
		curr_set = extract_exercise(text)

		#=====[ Update current workout if exercise extracted ]=====
		if curr_set:

			curr_subroutine = workout.curr_subroutine
				
			if curr_subroutine and (not curr_set.exercise or curr_subroutine.has_exercise(curr_set.exercise)):
			#=====[ If we're in the middle of an existing subroutine ]=====

				workout.add_set(curr_set)

			#=====[ Beginning a new subroutine ]=====s
			else:

				if curr_subroutine:
					workout.add_subroutine(curr_subroutine)
					
					total_seconds = curr_subroutine.get_total_set_time()
					time = str(int(total_seconds/60)) + ' min ' + str(total_seconds % 60) + ' sec' if total_seconds > 60 else str(total_seconds) + ' sec'

					#=====[ Notify user of duration of previous subroutine ]=====
					ut.send_response('Your ' + ', '.join(curr_subroutine.exercises) + ' exercise took you a total of ' + time, user_id)

				workout.new_subroutine('exercise', [curr_set.exercise], curr_set)

			user.current_workout = workout
		
			set_timers(user_id, user)
			cur_time = datetime.datetime.now()
			# seconds_passed = int((cur_time - user.time).total_seconds())
			# ut.send_response(str(seconds_passed)+ " seconds since your last log", user_id)

			user.time = cur_time
			ut.update(user_id, user)

		#=====[ If no exercise extracted, notify user ]=====
		else:

			ut.send_response(NO_EXERCISE_EXTRACTED_MESSAGE, user_id)


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

	
def end_user_workout(user, user_id, workout):

	#=====[ Add workout to list of past workouts and put in idle mode ]=====
	user.add_workout(workout)
	user.current_workout = None
	
	ut.update(user_id, user)

def clear_timers(user):
	""" Clears any processes sending timers to user once they log again """

	#=====[ Terminate each timer ]=====
	if hasattr(user, 'timer_processes'):
		for pid in user.timer_processes:
			os.kill(pid, signal.SIGTERM)

def send_warning(user_id, message, seconds):
	""" Sends Timing warning to user for specified amount of time """

	time.sleep(seconds - 2)
	ut.send_response(message + str(seconds) + ' seconds.', user_id)

def set_timers(user_id, user):
	""" Starts a process for each timer set by a user. """

	if hasattr(user, 'timer'):
		user.timer_processes = []
		
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

