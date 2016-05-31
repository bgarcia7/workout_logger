from workout import Workout

class WorkoutTemplate():
	""" WorkoutTemplate is a class that allows a user to be guided through a pre-selected workout """

	def __init__(self, intro='LETS GET GOING', workout=None, time=None, author=None):

		self.workout = workout
		self.time = None
		self.author = author
		self.intro = intro