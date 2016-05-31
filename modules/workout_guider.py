from database import *
import utils as ut
import pickle
from resources import *
from workout_log import extract_exercise

NOT_STARTED = 0
IN_WORKOUT = 1

class WorkoutGuider():
	""" Class that is used to guide a user through a workout template and simultaneously log their workout """

	def __init__(self, workout_template):

		self.workout = Workout()
		self.template = pickle.loads(templates.find_one()['template_object'])
		self.state = NOT_STARTED
		self.workout_state = None

		ut.send_response(workout_template.intro, user_id)


	def process(self, text):
		""" 
			Processes user input for a given state

			state = NOT_STARTED ---> ask user to start
			state = IN_WORKOUT ---> log current set reported by user

		"""

		#=====[ If user has not started workout ]=====
		if self.state == NOT_STARTED:

			if 'yes' in text:

				self.state == IN_WORKOUT
				self.workout_state = (0,0)
				self.subroutine_intro()

			else:

				ut.send_button_confirm_response(START_WORKOUT,user_id)

		#=====[ If in workout, log state ]=====
		elif self.state == IN_WORKOUT:

			sub_state, set_state = self.workout_state

			user_set = extract_exercise(text)
			ut.send_response('Got your first set to be: ' + str(user_set), user_id)






	def subroutine_intro(self):

		sub_state = self.workout_state[0]
		subroutine = self.workout.subroutines[sub_state]
		ut.send_response('Workout is: ' + str(subroutine), user_id)
