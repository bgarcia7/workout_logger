import utils as ut
import datetime 
from responses import *
import workout_log

def process(user, message):

	user_id, text = ut.get_info(user, message)

	if "start" in text and "workout" in text:

		workout_log.start(user)

	#=====[ Send default message ]=====
	else:

		ut.send_response(DEFAULT_IDLE_MESSAGE, user_id)