import utils as ut
from resources import *
import re

def start(user):

	user_id = user.get_id()

	#=====[ Start workout ]=====
	user.status = "feedback"
	user.status_state = 0
	ut.update(user_id, user)

	ut.send_response(FEEDBACK_QUESTION, user_id)


def process(user, message):

	user_id, text = ut.get_info(user, message)
	workout = user.get_last_workout()

	rating = extract_int(text)
	print rating

	#On feedback question
	if user.status_state == 0:

		if "yes" in text.lower() or "ok" in text.lower():
			ut.send_response(RATING_QUESTION, user_id)
			user.status_state = 1

		elif "no" in text.lower():
			user.status = "idle"
			user.status_state = 0

		else:
			ut.send_response(FEEDBACK_CLARIFY, user_id)
			ut.send_response(FEEDBACK_QUESTION, user_id)

		ut.update(user_id, user)


	# On rating question
	elif user.status_state == 1:

		if rating:

			if rating >= 1 and rating <= 10:
				workout.rating = rating
				ut.send_response(QUESTION_END, user_id)
				user.status_state = 2
				ut.update(user_id, user)
				ut.send_response(DIFFICULTY_QUESTION, user_id)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(RATING_CLARIFY, user_id)
		ut.send_response(RATING_QUESTION, user_id)

		


	# On difficulty question
	elif user.status_state == 2:
		
		if rating:
			if rating >= 1 and rating <= 5:
				workout.rating = rating
				ut.send_response(QUESTION_END, user_id)
				user.status_state = 3
				ut.update(user_id, user)
				ut.send_response(TIREDNESS_QUESTION, user_id)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(DIFF_TIRED_CLARIFY, user_id)
		ut.send_response(DIFFICULTY_QUESTION, user_id)


	# On tiredness question
	elif user.status_state == 3:
		
		if rating:

			if rating >= 1 and rating <= 5:
				workout.rating = rating
				ut.send_response(FEEDBACK_END, user_id)
				user.status = "idle"
				user.status_state = 0
				ut.update(user_id, user)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(DIFF_TIRED_CLARIFY, user_id)
		ut.send_response(TIREDNESS_QUESTION, user_id)

def extract_int(text):
	
	number = None

	#=====[ regex to extract weight ]=====
	regex = r"\d+"

	if re.search(regex,text):

		match = re.search(regex, text)

		#=====[ Store weight ]=====
		number = int(match.group(0))
		
	return number
