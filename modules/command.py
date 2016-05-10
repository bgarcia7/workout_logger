import utils as ut
import datetime 
from resources import *

command_list = ['list commands', 'sudo log: [suggestion]', 'list workouts','review last workout', 'review workout: [index]']

def process(user, message):

	user_id, text = ut.get_info(user, message)


	#==========[ Command used to list all super commands for the workout logger ]==========#
	#																				       #
	#	usage: " list commands "									   					   #
	#																					   #
	########################################################################################

	if 'list' in text and 'commands' in text:

		ut.send_response('Here are a list of commands:\n\n' + '\n'.join(command_list), user_id)


	#=====[ Command used to log thoughts/improvements while using the workout logger ]=====#
	#																				       #
	#	usage: " sudo log: [suggestion to improve] "									   #
	#																					   #
	########################################################################################

	elif 'sudo' in text and 'log' in text and ':' in text:

		with open('to_improve_log','a') as f:
			f.write(text.split(':')[1].strip() + '\n\n')

		ut.send_response(MESSAGE_LOGGED, user_id)


	#=========================[ Command used list recent workouts ]========================#
	#																				       #
	#	usage: " list workouts "									   					   #
	#																					   #
	########################################################################################

	elif 'list' in text and 'workouts' in text:

		ut.send_response('\n'.join([str(idx + 1) + '. ' + str(workout) for idx, workout in enumerate(reversed(user.workouts))]), user_id)


	#=====================[ Command used to review most recent workout ]===================#
	#																				       #
	#	usage: " review last workout "									   				   #
	#																					   #
	########################################################################################

	elif 'review' in text and 'last' in text and 'workout' in text:

		ut.send_response(user.workouts[-1].get_summary(), user_id)

	
	#==================[ Command used to review a particular workout ]=====================#
	#																				       #
	#	usage: " review workout: [index] "									   			   #
	#																					   #
	########################################################################################

	elif 'review' in text and 'workout' in text and ':' in text:

		try: 
			
			idx = int(text.split(':')[1].strip())

			ut.send_response(user.workouts[-idx].get_summary(), user_id)

		except Exception as e:
			
			print e

	else:

		return False

	return True




