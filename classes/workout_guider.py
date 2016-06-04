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
		self.prev_user_set = None

		ut.send_response(self.template.intro, user_id)
		ut.send_response(START_WORKOUT, user_id)


	def process(self, text, user, user_id):
		""" 
			Processes user input for a given state

			state = NOT_STARTED ---> ask user to start
			state = IN_WORKOUT ---> log current set reported by user

			Returns bool representing successful parse and whether we should move on to next set

		"""

		#=====[ If user has not started workout ]=====
		if self.state == NOT_STARTED:
			if 'yes' in text:

				self.state = IN_WORKOUT
				self.workout_state = (0, -1)
				return True

			else:
				ut.send_response(START_WORKOUT,user_id)
				return False

		#=====[ If in workout, log state ]=====
		elif self.state == IN_WORKOUT:
			sub_state, set_state = self.workout_state

			user_set = ut.extract_exercise(text)

			if user_set:

				template_workout = self.template.workout
				sub_state, set_state = self.workout_state

				xsets = template_workout.subroutines[sub_state].get_flattened_sets()
				user_set.exercise = xsets[set_state].exercise

				#=====[ Log set and give feedback ]=====
				workout_log.log_set(user_set, self.workout, user, user_id)
				ut.send_response('Got your last set to be: ' + str(user_set), user_id)

				self.prev_user_set = user_set
				self.cur_set_feedback(user_set, xsets[set_state], user_id)
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

		# Get the subroutine of the current set
		curr_subroutine = self.template.workout.subroutines[sub_state]

		set_state += 1

		if set_state >= curr_subroutine.num_sets:
			set_state = 0
			sub_state += 1

		if sub_state >= len(self.template.workout.subroutines):
			return None


		# Update curr_subroutine after updating indexes
		curr_subroutine = self.template.workout.subroutines[sub_state]
		sets_per_cycle = len(curr_subroutine.exercises)
		subroutine_mode = curr_subroutine.mode

		# Update object workout state
		self.workout_state = (sub_state, set_state)

		# set_state == 0 means we are starting a new subroutine
		if set_state == 0:
			self.subroutine_intro(user_id)

			self.workout.add_subroutine()

			next_subroutine = self.template.workout.subroutines[sub_state]
			self.workout.new_subroutine(next_subroutine.mode, next_subroutine.exercises)

		# If we are at the beginning of a cycle in a circuit
		if subroutine_mode == "circuit" and set_state % sets_per_cycle == 0:
			response = "Next Cycle of Circuit: \n"

			sets = self.template.workout.subroutines[sub_state].get_flattened_sets()
		
			for i in range(sets_per_cycle):
				xset = sets[set_state + i]
				response += xset.exercise + ' ' + str(xset) + "\n"

			ut.send_response(response, user_id)

		# TODO: FOR BRANDON
		# get_feedback - current user set, current template set, next template set (None for diff subroutine)

		response = "Your next set is: "

		sets = self.template.workout.subroutines[sub_state].get_flattened_sets()
		xset = sets[set_state]

		response += xset.exercise + ' ' + str(xset) + "\n"

		#=====[ Give feedback for up and coming set ]=====
		if self.prev_user_set:
			self.next_set_feedback(self.prev_user_set, xset, user_id)

		ut.send_response(response, user_id)

		return self.workout_state


	def cur_set_feedback(self, user_set, cur_set, user_id):
		""" Analyzes a user's current set and gives feedback """

		print 'in feedback'

		print 'cur set: ',cur_set.reps, 'type:', type(cur_set.reps)
		print 'user set: ',user_set.reps, 'type: ', type(user_set.reps)
			
		#=====[ Check to see if we're giving feedback on a body weight set ]=====
		if cur_set.weight == None and user_set.weight == None:

			#=====[ If user did more sets than required ]=====
			if int(user_set.reps) > int(cur_set.reps):

				ut.send_response(GOOD_REPS_NO_WEIGHT, user_id)

		else:

			rep_percentage = float(user_set.reps)/float(cur_set.reps)

			if int(user_set.reps) < int(cur_set.reps):

				#=====[ Feedback on not doing enough reps on current set ]=====
				if rep_percentage:
					ut.send_response(DID_TOO_MUCH_WEIGHT + str(int(rep_percentage*100)) + "% of your reps", user_id)
				
				elif int(user_set.reps) != int(cur_set.reps) - 1:
					ut.send_response(DID_A_BIT_TOO_MUCH_WEIGHT, user_id)


			if int(user_set.reps) > int(cur_set.reps):

				#=====[ Feedback on doing too many reps on current set ]=====
				if rep_percentage > 1.3:
					ut.send_response(DID_NOT_DO_ENOUGH_WEIGHT + str(int((rep_percentage-1)*100)) + "%", user_id)
				
				elif int(user_set.reps) != int(cur_set.reps) + 1:
					ut.send_response(DID_A_BIT_TOO_LIGHT, user_id)


		
	def next_set_feedback(self, user_set, next_set, user_id):
		""" Analyzes a user's current set and gives feedback for next set """

		print 'next set: ',next_set.reps, 'type:', type(next_set.reps)
		print 'user set: ',user_set.reps, 'type: ', type(user_set.reps)

		if next_set.weight:

			#=====[ Give feedback on weight for next set ]=====
			if int(user_set.reps) < int(next_set.reps) - 1:

				ut.send_response(REDUCE_WEIGHT, user_id)

			elif int(user_set.reps) > int(next_set.reps) + 1:

				ut.send_response(INCREASE_WEIGHT, user_id)

			else:

				ut.send_response(KEEP_WEIGHT, user_id)

		else:

			if int(user_set.reps) < int(next_set.reps):

				ut.send_response(MORE_REPS_NO_WEIGHT, user_id)








