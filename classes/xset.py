import datetime
import re
from pymongo import MongoClient
from collections import Counter
from muscle_detector import *


db_client = MongoClient()
ex_db = db_client['exercise_db']
exercise_collection = ex_db['exercises']

class xSet:

	def __init__(self, exercise, weight, reps, note=None):
		self.exercise = exercise
		self.weight = weight
		self.reps = reps
		self.time = datetime.datetime.now()
		self.note = note


	def __str__(self):
		""" Returns string representation of set """

		string = str(self.reps) + ' reps'
		string += ' @ ' + str(self.weight) + ' lbs' if self.weight else ''

		return string

	def __eq__(self, other):
		return (self.exercise, self.weight, self.reps) == (other.exercise, other.weight, other.reps)


	def get_volume(self):
		#=====[ Return weight x reps or 0 if exercise doesn't have weight ]=====
		return int(self.weight) * int(self.reps) if self.weight else 0

	def get_muscle_group(self):
		""" Uses muscle_detector to predict primary muscle groups targeted by exercise """

		self.muscle_groups = get_muscle_groups(self.exercise)
		
		#=====[ Return empty array if no muscle_groups found ]=====
		if not self.muscle_groups:
			return []

		#=====[ normalize the results ]=====
		norm_factor = max(self.muscle_groups.values())

		for key, value in self.muscle_groups.items():
			self.muscle_groups[key] = float(value)/norm_factor

		return self.muscle_groups 
