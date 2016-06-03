from database import *
import utils as ut
import pickle
from resources import *
from workout import Workout
sys.path.append('../')
import workout_log

NOT_STARTED = 0
IN_WORKOUT = 1

class WorkoutGuider():
	""" Class that is used to guide a user through a workout template and simultaneously log their workout """

	def __init__(self, user_id, workout_template):

		self.workout = Workout()
		self.template = pickle.loads(templates.find_one()['template_object'])
		self.state = NOT_STARTED
		self.workout_state = None

		ut.send_response(self.template.intro, user_id)
		ut.send_response(START_WORKOUT, user_id)


	def process(self, text, user, user_id):
		""" 
			Processes user input for a given state

			state = NOT_STARTED ---> ask user to start
			state = IN_WORKOUT ---> log current set reported by user

			Returns bool representing successful parse and whether we should move on to next set

		"""
		print 'Were in process!'

		#=====[ If user has not started workout ]=====
		print self.state
		if self.state == NOT_STARTED:
			print "NOT STARTED"
			if 'yes' in text:

				self.state = IN_WORKOUT
				self.workout_state = (0,0)
				self.subroutine_intro(user_id)
				return True

			else:
				ut.send_response(START_WORKOUT,user_id)
				return False

		#=====[ If in workout, log state ]=====
		elif self.state == IN_WORKOUT:
			print "IN WORKOUT"
			sub_state, set_state = self.workout_state

			user_set = ut.extract_exercise(text)
			if user_set:
				workout_log.log_set(user_set, self.workout, user, user_id)
				ut.send_response('Got your last set to be: ' + str(user_set), user_id)
				return True
			else:
				ut.send_response('Exercise not recognized, please retry', user_id)
				return False


	def subroutine_intro(self, user_id):
		sub_state = self.workout_state[0]

		subroutine = self.template.workout.subroutines[sub_state]
		response = 'Subroutine is:\n'

		for exercise in subroutine.exercises:
			response += exercise + '\n'

		ut.send_response(response, user_id)

	def next_set(self, user_id):
		sub_state, set_state = self.workout_state

		set_state += 1

		if set_state >= self.template.workout.subroutines[sub_state].num_sets:
			set_state = 0
			sub_state += 1


		if sub_state >= len(self.template.workout.subroutines):
			return None

		# TODO: FOR BRANDON
		# get_feedback - current user set, current template set, next template set (None for diff subroutine)

		# Update object workout state
		self.workout_state = (sub_state, set_state)

		# set_state == 0 means we are starting a new subroutine
		if set_state == 0:
			self.subroutine_intro(user_id)

		response = "Your next set is: "

		sets = self.template.workout.subroutines[sub_state].get_flattened_sets()
		xset = sets[set_state]

		response += xset.exercise + ' ' + str(xset) + "\n"

		ut.send_response(response, user_id)

		
		print self.workout_state
		return self.workout_state

