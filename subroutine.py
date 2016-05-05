from Collections import defaultdict

class Subroutine():

	def __init__(self, mode="exercise", exercises=[]):
		self.mode = mode
		self.exercises = exercises
		self.sets = defaultdict(list)
		self.num_sets = 0

	def addSet(self, xset):
		self.num_sets += 1
		exercise = xset.exercise

		if self.mode == "exercise":
			self.sets[exercise].append(xset)

		elif self.mode == "circuit":

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

		else:
			raise ValueError("No mode %s" % self.mode)