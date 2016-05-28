from database import *
from collections import Counter
import re

def get_muscle_groups(exercise):
	""" Takes the user-specified name of an exercise and returns the most relevant muscle groups """

	print exercise
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

	return counts if len(counts) > 0 else None

def count_muscle_groups(ex_string):
	""" 
		Searches the database for the given string and returns a Counter with the counts of each relevant
		muscle group for each found exercise 
	"""

	regex = re.compile(ex_string,re.IGNORECASE)

	#=====[ search for exercises again ]=====
	muscle_groups = exercise_collection.find({"exercise" : regex})
	counts = Counter([ex['muscle'].strip() for ex in muscle_groups])

	return counts


