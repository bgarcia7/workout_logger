import utils as ut
import datetime 
from resources import *

command_list = ['list commands', 'sudo log: [suggestion]', 'list workouts','review last workout', 'review workout: [index]', 'review week']

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

		workout_summary = user.workouts[-1].get_summary()
		ut.send_response(workout_summary, user_id)

	
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

	#=============[ Command used to review a weeks worth of workout stats ]================#
	#																				       #
	#	usage: " review week "									   			   #
	#																					   #
	########################################################################################

	elif 'review' in text and 'week' in text:

		info = 'Here\'s your week in review: \n\n'

		info += 'Total Sets: ' + str(user.get_num_sets(7)) + '\n' 
		info += 'Total Volume: ' + str(user.get_volume(7)) + '\n'
		info += 'Avg. Set Time: ' + str(user.get_avg_set_time(7)) + '\n'

		ut.send_response(info, user_id)

	else:

		return False

	return True




