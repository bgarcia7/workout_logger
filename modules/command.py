import utils as ut
import datetime 
import goal
from resources import *
# from spider import *

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

		workout = user.workouts[-1]

		ut.send_response(workout.get_summary(), user_id)
		ut.send_response(workout.get_stats(),user_id)

		index = 4 if len(workout.muscle_groups) > 3 else len(workout.muscle_groups)

		# if generate_spider(user_id, dict(workout.muscle_groups.most_common(index))):
		# 	ut.send_response('Check out the muscles you targeted:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)

	
	#==================[ Command used to review a particular workout ]=====================#
	#																				       #
	#	usage: " review workout: [index] "									   			   #
	#																					   #
	########################################################################################

	elif 'review' in text and 'workout' in text and ':' in text:

		try: 
			
			idx = int(text.split(':')[1].strip())
			workout = user.workouts[-idx]

			ut.send_response(user.workouts[-idx].get_summary(), user_id)
			ut.send_response(user.workouts[-idx].get_stats(), user_id)

			index = 4 if len(workout.muscle_groups) > 3 else len(workout.muscle_groups)

			# if generate_spider(user_id, dict(workout.muscle_groups.most_common(index))):
			# 	ut.send_response('Check out the muscles you targeted:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)

		except Exception as e:
			
			print e

	#=============[ Command used to review a weeks worth of workout stats ]================#
	#																				       #
	#	usage: " review week "									   			   			   #
	#																					   #
	########################################################################################

	elif 'review' in text and 'week' in text:

		info = 'Here\'s your week in review: \n\n'

		info += 'Total Volume: ' + str(user.get_volume(7)) + '\n'
		info += 'Total Sets: ' + str(user.get_num_sets(7)) + '\n' 
		info += 'Total Time: ' + "{0:.2f}".format(float(user.get_total_set_time(7)/3600.0)) + ' hours' + '\n'
		info += 'Avg. Set Time: ' + "{0:.2f}".format(user.get_avg_set_time(7)) + '\n'

		ut.send_response(info, user_id)

		index = 6 if len(workout.muscle_groups) > 5 else len(workout.muscle_groups)

		# if generate_spider(user_id, dict(user.get_muscle_groups(7).most_common(index))):
		# 	ut.send_response('Check out the muscles you targeted most:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)


	elif 'q:' in text:
		exercise = text.split(':')[1].strip()
		info = 'You queried for: %s\n\n' % exercise

		sets = user.query_exercise(exercise)

		for date in sets:
			workout_sets = sets[date]

			info += "Workout on %s:\n" % date

			for xset in workout_sets:
				info += "%s reps of %s @ %s\n" % (xset.reps, xset.exercise, xset.weight)

		ut.send_response(info, user_id)


	#==================[ Command used to drop a user from the database ]===================#
	#																				       #
	#	usage: " reset db "									   			   			   	   #
	#																					   #
	########################################################################################

	elif text == 'reset db':
		
		ut.send_response('BYE FOREVER! :( ', user_id)
		ut.remove_user(user_id)


	#==================[ Command used set goals for targeted muscles ]=====================#
	#																				       #
	#	usage: " set goals "									   			   			   	   #
	#																					   #
	########################################################################################

	elif 'set' in text and 'goal' in text:

		muscle_groups = text.split(':')

		#=====[ Check to make sure there are muscle groups specified after a colon ]=====
		if len(muscle_groups) == 1:
			ut.send_response(SET_GOALS, user_id)

		#=====[ set goals for user ]=====
		goal.process(user, user_id, muscle_groups[1])

	else:

		return False

	return True




