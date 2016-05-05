import datetime

class Set():

	def __init__(self, exercise, weight, reps):
		self.exercise = exercise
		self.weight = weight
		self.reps = reps
		self.time = datetime.datetime.now()