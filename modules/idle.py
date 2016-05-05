import utils as ut
import datetime 
from responses import *

def process(user, message):

	user_id, text = ut.get_info(user, message)

	if "start" in text and "workout" in text:
		#=====[ Start workout ]=====
		user["status"] = "workout"
		user["current_workout"] = {"start_time": datetime.datetime.now(), "exercises": []}

		ut.update({"user_id": user_id}, user)
		ut.send_response(START_WORKOUT_MESSAGE, user_id)

	else:
		ut.send_response(DEFAULT_IDLE_MESSAGE, user_id)