import datetime

class xSet:

	def __init__(self, exercise, weight, reps):
		self.exercise = exercise
		self.weight = weight
		self.reps = reps
		self.time = datetime.datetime.now()

	def __str__(self):
		""" Returns string representation of set """

		string = 'Reps: ' + str(self.reps)
		string += ' | Weight: ' + str(self.weight) if self.weight else ''

		return string

	def __eq__(self, other):
		return (self.exercise, self.weight, self.reps) == (other.exercise, other.weight, other.reps)
