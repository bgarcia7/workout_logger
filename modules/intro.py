import utils as ut
import datetime 
from responses import *

def process(user, message):

	user_id, text = ut.get_info(user, message)

	user['status'] = 'idle'
	ut.send_response(WELCOME_MESSAGE, user_id)

	ut.update({'user_id':user_id}, user)