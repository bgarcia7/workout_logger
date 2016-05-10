import datetime
import xset
from subroutine import Subroutine
from resources import months

class Workout:

	def __init__(self):
		self.start_time = datetime.datetime.now()
		self.curr_subroutine = None
		self.subroutines = []

		# Workout Statistics
		self.volume = None
		self.num_sets = None
		self.total_set_time = None

	def __str__(self):
		return str(months[self.start_time.month - 1] + ' ' + str(self.start_time.day) + ': [STATS]')

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

	# Workout Statistics

	def calculate_volume(self):
		""" calculate the total volume of the workout and set a cached copy """
		total_volume = 0

		for subroutine in self.subroutines:
			total_volume += subroutine.get_volume()

		self.volume = total_volume
	
	def get_volume(self):
		""" return cached copy of workout volume """
		return self.volume

	def calculate_total_set_time(self):
		""" calculate total time spent on sets in workout """
		total_time = 0

		for subroutine in self.subroutines:
			total_time += subroutine.get_total_set_time()

		self.total_set_time = total_time

	def get_total_set_time(self):
		return self.total_set_time

	def calculate_num_sets(self):
		""" calculate total number of sets performed in workout """
		total_sets = 0

		for subroutine in self.subroutines:
			total_sets += subroutine.get_num_sets()

		self.num_sets = total_sets

	def get_num_sets(self):
		return self.num_sets

	def get_avg_set_time(self):
		""" get the average time per set of a workout """
		return self.total_set_time * 1.0 / self.num_sets

