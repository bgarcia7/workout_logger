from collections import defaultdict
import xset 

class Subroutine:

	def __init__(self, mode="exercise", exercises=[]):
		""" Initializes subroutine:

			mode = "exercise" or "circuit"
			exercise = [single exercise or exercises in circuit]

		"""

		self.mode = mode
		self.exercises = exercises
		self.sets = defaultdict(list)
		self.num_sets = 0
		self.curr_exercise = exercises[0]

	def add_set(self, xset):
		""" Adds set of exercise to subroutine """
		
		self.num_sets += 1
		exercise = xset.exercise

		if self.mode == "exercise":
			
			#=====[ If user only reported reps/weight, add exercise to set object ]=====
			if not xset.exercise:
				xset.exercise = self.curr_exercise

			self.sets[exercise].append(xset)

		elif self.mode == "circuit":

			#=====[ If no exercise specified, or exercise specified is in correct order, add set ]=====
			if not exercise or exercise == self.curr_exercise:

				xset.exercise = self.curr_exercise
				self.sets[self.curr_exercise].append(xset)

			#=====[ If exercise is out of order ]=====
			else:

				self.curr_exercise = exercise 

				#=====[ Get length of current exercise ]=====
				set_len = len(self.sets[exercise])
				ex_idx = self.exercises.index(exercise)

				#=====[ Iterate through exercises to ensure circuit order consistencey ]====
				for idx, ex in enumerate(self.exercises):
					
					#=====[ Once we reach correct exercise, append set ]=====
					if ex == exercise:
						self.sets[exercise].append(xset)
					
					#=====[ If exercise in circuit has been skipped, append None ]=====
					elif ((len(self.sets[ex]) <= set_len) and idx < ex_idx) or (len(self.sets[ex]) <= set_len -1):
						self.sets[ex].append(None)

			#=====[ Update current exercise ]=====
			self.curr_exercise = self.exercises[(self.exercises.index(xset.exercise) + 1) % len(self.exercises)]

		else:
			raise ValueError("No mode %s" % self.mode)

	def has_exercise(self, exercise):
		return exercise in self.exercises


	def getVolume(self):
		total_volume = 0

		for set_list in self.sets:
			for xset in set_list:
				total_volume += xset.getVolume()

		return total_volume