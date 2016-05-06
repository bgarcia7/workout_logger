import utils as ut
import datetime 
from responses import *

def process(user, message):

	user_id, text = ut.get_info(user, message)

	#=====[ Set idle status for user ]=====
	user.set_status('idle')

	ut.send_response(WELCOME_MESSAGE, user_id)

	#=====[ Update user in db ]=====
	ut.update(user_id, user)