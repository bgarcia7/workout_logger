import datetime 
from collections import Counter

class User:

	def __init__(self, user_id):
		self.id = user_id
		self.messages = []
		self.workouts = []
		self.current_workout = None
		self.status = "intro"


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

	def get_muscle_groups(self, n):
		""" Returns relative counts of all muscle groups worked over past n days """

		workouts = self.get_workouts_from_last_n_days(n)

		counts = Counter()

		for workout in workouts:
			workout.aggregate_muscle_groups()
			counts.update(workout.muscle_groups)

		return counts

