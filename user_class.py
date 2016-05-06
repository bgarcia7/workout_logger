import datetime 

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