import datetime 
from collections import Counter, OrderedDict
from fuzzywuzzy import fuzz
import numpy as np

class User:

	def __init__(self, user_id):
		self.id = user_id
		self.messages = []
		self.workouts = []
		self.current_workout = None
		self.status = "intro"
		self.stage = 0


	def add_message(self, message):
		self.messages.append({"timestamp":datetime.datetime.now(), "message":message})

	def get_status(self):
		return self.status

	def set_status(self, status):
		self.status = status

	def get_id(self):
		return self.id

	def get_current_workout(self):
		return self.current_workout

	def get_last_workout(self):
		return self.workouts[-1] if self.workouts else None

	def add_workout(self, workout):
		self.workouts.append(workout)

	def get_workouts_from_last_n_days(self, n):
		recent_workouts = []
		for workout in reversed(self.workouts):
			delta = datetime.datetime.now() - workout.start_time

			#=====[ Append to list only if workout within n days of now ]=====
			if delta.days < n:
				recent_workouts.append(workout)

		return recent_workouts

	# Stats from Recent Workouts
	def get_volume(self, n):
		workouts = self.get_workouts_from_last_n_days(n)
		total_volume = 0

		for workout in workouts:
			total_volume += workout.volume if workout.volume else 0

		return total_volume


	def get_total_set_time(self, n):
		workouts = self.get_workouts_from_last_n_days(n)
		total_set_time = 0

		for workout in workouts:
			total_set_time += workout.total_set_time if workout.total_set_time else 0

		return total_set_time

	def get_num_sets(self, n):
		workouts = self.get_workouts_from_last_n_days(n)
		total_sets = 0

		for workout in workouts:
			total_sets += workout.get_num_sets() if workout.get_num_sets() else 0

		return total_sets

	def get_avg_set_time(self, n):
		return float("{0:.2f}".format(self.get_total_set_time(n) * 1.0 / self.get_num_sets(n)))

	def get_muscle_groups(self, n, index, summary=True):
		""" Returns relative counts of all muscle groups worked over past n days """

		workouts = self.get_workouts_from_last_n_days(n)

		counts = Counter()

		for workout in workouts:
			workout.aggregate_muscle_groups()
			counts.update(workout.muscle_groups)

		muscles = counts

		#=====[ Get the N amount of muscle groups to report ]=====
		index = index if len(muscles) >= index else len(muscles)

		#=====[ normalize values ]=====
		values = muscles.values()
		labels = muscles.keys()
		indices = np.asarray(values).argsort()[::-1][:index]

		labels = [labels[idx] for idx in indices]
		values = [values[idx] for idx in indices]
		values = [int(100*val/sum(values)) for val in values]

		#=====[ If don't want summary, return values and labels ]=====
		if not summary:
			return values, labels

		#=====[ Build summary string ]=====		
		summary = 'You worked out the following muscles:\n\n'

		for idx, label in enumerate(labels):

			summary += label + ': ' + str(values[idx]) + ' %\n'

		return summary

	def query_exercise(self, query, workout_limit=1):
		""" Returns an ordered dict where the keys are dates of workouts and the values are lists of sets of exercises that match the query """
		
		num_workouts_query_matched = 0
		sets = OrderedDict()

		# Loop over all workouts
		for workout in self.workouts:

			# Once we find enough workouts that contain the exercise queried, we can return the sets
			if num_workouts_query_matched < workout_limit:

				# Loop through all subroutines in the workout
				for subroutine in workout.subroutines:

					# Loop through the exercises in the subroutine
					for exercise in subroutine.exercises:

						# If the exercise fuzzy matches the search query
						if fuzz.ratio(query, exercise) > 80 or query in exercise or exercise in query:

							workout_date = workout.start_time.date()

							if workout_date not in sets:
								sets[workout_date] = []

							# Add all the sets to the list
							sets[workout_date] += subroutine.sets[exercise]


		return sets

