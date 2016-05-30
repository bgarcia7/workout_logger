import utils as ut
from resources import *

def start(user):

	user_id = user.get_id()

	#=====[ Start workout ]=====
	user.status = "feedback"
	user.state = 0
	ut.update(user_id, user)

	ut.send_response(FEEDBACK_QUESTION, user_id)


def process(user, message):

	user_id, text = ut.get_info(user, message)
	workout = user.get_last_workout()

	#On feedback question
	if user.state == 0:

		if "yes" in text.lower() or "ok" in text.lower():
			ut.send_response(RATING_QUESTION, user_id)
			user.state = 1

		elif "no" in text.lower():
			user.status = "idle"
			user.state = 0

		else:
			ut.send_response(FEEDBACK_CLARIFY, user_id)
			ut.send_response(FEEDBACK_QUESTION, user_id)

		ut.update(user_id, user)


	# On rating question
	if user.state == 1:
		if is_integer(text):
			rating = int(text)

			if rating >= 1 and rating <= 10:
				workout.rating = rating
				ut.send_response(QUESTION_END, user_id)
				user.state = 2
				ut.update(user_id, user)
				ut.send_response(DIFFICULTY_QUESTION, user_id)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(RATING_CLARIFY, user_id)
		ut.send_response(RATING_QUESTION, user_id)

		


	# On difficulty question
	elif user.state == 2:
		if is_integer(text):
			rating = int(text)

			if rating >= 1 and rating <= 5:
				workout.rating = rating
				ut.send_response(QUESTION_END, user_id)
				user.state = 3
				ut.update(user_id, user)
				ut.send_response(TIREDNESS_QUESTION, user_id)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(DIFF_TIRED_CLARIFY, user_id)
		ut.send_response(DIFFICULTY_QUESTION, user_id)


	# On tiredness question
	elif user.state == 3:
		if is_integer(text):
			rating = int(text)

			if rating >= 1 and rating <= 5:
				workout.rating = rating
				ut.send_response(FEEDBACK_END, user_id)
				user.status = "idle"
				user.state = 0
				ut.update(user_id, user)
				return

		# If anything goes wrong, send a clarifying message
		ut.send_response(DIFF_TIRED_CLARIFY, user_id)
		ut.send_response(TIREDNESS_QUESTION, user_id)

def is_integer(text):
	try: 
		int(text)
		return True
	except ValueError:
		return False
