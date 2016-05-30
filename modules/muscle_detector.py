from database import *
from collections import Counter
from resources import *
import re
from muscle_classifier import MuscleClassifier

model = MuscleClassifier()

muscles = ['lats', 'chest', 'quadriceps', 'biceps', 'middle back', 'traps', 'shoulders', 'calves', 'abdominals', 'glutes', 'forearms', 'lower back', 'triceps', 'hamstrings', 'abductors', 'adductors', 'neck']
grouped_muscles = {'back':['lats', 'middle back', 'traps','lower back'], 'legs': ['adductors','quadriceps', 'calves', 'hamstrings'], 'abs':['abdominals'], 'butt':['glutes', 'abductors'], 'arms':['forearms',  'triceps', 'biceps']}


def get_muscle_groups(exercise):
	""" Takes the user-specified name of an exercise and returns the most relevant muscle groups """

	if not exercise:
		return None

	#=====[ Count up occurrences of each muscle group ]=====
	counts = count_muscle_groups(exercise)


	#=====[ If no exercises found, then search for subgroups of the user-input string ]=====
	if len(counts) == 0:

		exs = exercise.split()

		#=====[ Search for exercises using all permutations of 2 words from the input string ]=====
		for idx in range(len(exs)-1):

			#=====[ formulate new search string ]=====
			ex_string = ' '.join(exs[idx:idx+2])

			#=====[ Aggregate all results ]=====
			counts.update(count_muscle_groups(ex_string))
				
		#=====[ If we still don't find any results, take each word individually and search it ]=====
		if len(counts) == 0:

			for ex in exs:

				#=====[ Aggregate all results ]=====
				counts.update(count_muscle_groups(ex))

	if len(counts) > 0:
		return counts
	else:
		return Counter(model.predict(exercise))

def count_muscle_groups(ex_string):
	""" 
		Searches the database for the given string and returns a Counter with the counts of each relevant
		muscle group for each found exercise 
	"""

	regex = re.compile(ex_string,re.IGNORECASE)

	#=====[ search for exercises again ]=====
	muscle_groups = exercise_collection.find({"exercise" : regex})
	counts = Counter([ex['muscle'].strip().lower() for ex in muscle_groups])

	return counts


