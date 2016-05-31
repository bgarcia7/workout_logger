import utils as ut
import datetime 
from resources import *
import workout_log


def process(user, message):

	user_id, text = ut.get_info(user, message)

	if "start" in text and "workout" in text:

		#=====[ Start guided workout ]=====
		if "guided" in text:
			workout_template = True
			workout_log.start(user, workout_template)

		#=====[ Manually log workout ]=====
		else:
			workout_log.start(user)

	#=====[ Send default message ]=====
	else:

		ut.send_response(DEFAULT_IDLE_MESSAGE, user_id)