import datetime
import xset
from subroutine import Subroutine

class Workout:

	def __init__(self):
		self.start_time = datetime.datetime.now()
		self.curr_subroutine = None
		self.subroutines = []

	def get_start_time(self):
		return self.start_time

	def end(self):
		self.subroutines.append(self.curr_subroutine)
		self.curr_subroutine = None

		self.end_time = datetime.datetime.now()

	def get_curr_subroutine(self):
		return self.curr_subroutine

	def set_curr_subroutine(self, subroutine):
		self.curr_subroutine = subroutine

	def get_subroutines(self):
		return self.subroutines

	def add_subroutine(self, subroutine):

		self.subroutines.append(subroutine)

	def get_summary(self):
		""" Returns string representation of workout summary """

		workout_summary = ''

		#=====[ iterate through each subroutine ]=====
		for subroutine in self.subroutines:
			#=====[ Iterate through exercise in each subroutine ]=====
			for ex in subroutine.exercises:

				workout_summary += str(ex) + ': \n'

				#=====[ Iterate through each set ]=====
				for xset in subroutine.sets[ex]:

					workout_summary += str(xset) + '\n'

				workout_summary += '\n'

		return workout_summary 

	def new_subroutine(self, mode, exercises, curr_set=None):

		new_subroutine = Subroutine(mode, exercises=exercises)
		
		if curr_set:
			new_subroutine.add_set(curr_set)
		
		self.curr_subroutine = new_subroutine