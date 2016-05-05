import utils as ut
import datetime 
from responses import *

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def process(user, message):

	user_id, text = ut.get_info(user, message)
	triggers = ['what', 'how', 'when', 'get']
	#=====[ Question or request for a stat ]=====
	if any([trigger in text for trigger in triggers]):
		# sample question: "what was the weight I did last time when I did bench press?"
		# sample question: "how long ago did I do bench press?"
		# sample question: ""
		workouts = user["workouts"]
		relevant_exercises = {}
		for workout in reversed(workouts):
			time = workout['start_time']
			for exercise in workout["exercises"]:
				if exercise["exercise"] in text:
					ex_name =exercise['exercise']
					if ex_name in relevant_exercises:
						relevant_exercises[ex_name] += [exercise]
					else:
						relevant_exercises[ex_name] = [exercise]

			if len(relevant_exercises) > 0:
				break

		if len(relevant_exercises) > 0:

			#=====[ Get last time exercise was performed ]=====
			day = time.day
			month = months[time.month - 1]

			response = 'On ' + str(month) + ' ' + str(day) + ' you did: \n\n'

			for exercise in relevant_exercises:
				print 'RELEVANT EXERCISES:', relevant_exercises
				response += relevant_exercises[exercise][0]['exercise'] + ':\n'
				for ex_set in relevant_exercises[exercise]:
					response += str(ex_set['reps']) + ' reps'
					if len(ex_set["weight"]) > 0:
						response += " at " + str(ex_set["weight"])
					response += '\n'
				response += '\n'
			ut.send_response(response, user_id)

			return True

	return False
			
