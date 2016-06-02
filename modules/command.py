import utils as ut
import datetime 
import goal
from resources import *
import re
# from spider import *

command_list = {'help': 'Type "help [some_command]" in order to get more information about that command. By the way, when you see brackets, it is indicating a placeholder for some command or string, but you should not actually type the brackets when you use some command',
	'list commands':'Using the "list commands" command will list all of your commands',
 	'sudo log: [suggestion]': 'Type "sudo log: [some message]" in order to give us some feedback about how we can improve the logger!',
  	'list workouts': 'This will list all of your workouts',
  	'review last workout': 'This will give you a summary of your most recent workout -- exercises performed, total time and volume, and muscle groups targeted',
    'review workout: [index]': 'Type "review workout: [index]" where index is a corresponding number for a workout as seen after typing "list workouts"',
    'review week': "This command will give you a summary of your last 7 days' worth of workouts",
    'reset db': "This will DELETE ALL OF YOUR DATA. No questions asked. Be careful",
    'query: [exercise]': 'Type "query: [some exercise you have previously performed]" to pull up the reps and weights you did last time. You can also just type "q: [exercise]" if you\'re lazy, like us :D',
    'set timer': 'Type "set timer(s) [number of seconds], [number of seconds], and [number of seconds]" to set as many timers as you want. These timers will start as soon as you log an exercise. The assumption is that you do some exercise and immediately log it -- at that point, we start your rest timer.',
    'clear timer': 'Type "clear timer(s)" in order to turn all of your timers off',
    'set goal': 'Type "set goals: [muscle group 1], [muscle group 2], [muscle group 3]" in order to let us know that you want to target those muscles. Eventually, we\'ll actually hold you to it!',
	'exit': 'Type "exit" to get out of any current flow. We won\'t save any workout in progress.'}

command_shortcuts = {'help':['help'],'list commands':['list commands','ls'],'sudo log: [suggestion]': ['sudo log', 'log'],
  	'list workouts': ['list workouts'], 'review last workout': ['review last workout'],'review workout: [index]': ['review workout'], 'review week': ['review week'],
    'reset db': ['reset db'], 'query: [exercise]': ['query', 'q'], 'set timer': ['set timer', 'set timers'], 'clear timer': ['clear timer', 'clear timers'], 'set goal': ['set goal', 'set goals'],
	'exit': ['exit']}

def process(user, message):

	user_id, text = ut.get_info(user, message)


	#==========[ Command used to list all super commands for the workout logger ]==========#
	#																				       #
	#	usage: " list commands "									   					   #
	#																					   #
	########################################################################################

	if ('list' in text and 'commands' in text) or text == 'ls':

		ut.send_response('Here are a list of commands:\n\n' + '\n'.join(command_list.keys()), user_id)


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

		ut.send_response(workout.summarize_muscle_groups(4), user_id)
		# index = index if len(workout.muscle_groups) >= index else len(workout.muscle_groups)

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

			ut.send_response(workout.summarize_muscle_groups(4), user_id)

			# index = 4 if len(workout.muscle_groups) > 3 else len(workout.muscle_groups)

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

		ut.send_response(user.get_muscle_groups(20, 7), user_id)

		# index = 6 if len(workout.muscle_groups) > 5 else len(workout.muscle_groups)

		# if generate_spider(user_id, dict(user.get_muscle_groups(7).most_common(index))):
		# 	ut.send_response('Check out the muscles you targeted most:\nfile:///Users/Brandon/Desktop/Projects/workout_logger/spider.png', user_id)


	elif 'q:' in text or 'query:' in text:
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
	#	usage: " set goals: muslce1, muscle2, muscle3"			   			   			   #
	#																					   #
	########################################################################################

	elif 'set' in text and 'goal' in text:

		muscle_groups = text.split(':')

		#=====[ Check to make sure there are muscle groups specified after a colon ]=====
		if len(muscle_groups) == 1:
			ut.send_response(SET_GOALS, user_id)

		#=====[ set goals for user ]=====
		goal.process(user, user_id, muscle_groups[1])

	#================[ Command used set timers at specified intervals ]====================#
	#																				       #
	#	usage: " set timer for 45 and 60 seconds"			   			   			       #
	#																					   #
	########################################################################################

	elif 'set' in text and 'timer' in text:

		times = re.split(',|and',text)
		found_time = False

		#=====[ Checks each comma separated value for a time ]=====
		for time_candidate in times:

			time = extract_int(time_candidate)

			#=====[ If time for timer extracted, save info ]=====
			if time:
				
				found_time = True

				if hasattr(user,'timer'):
					user.timer.append(time)
				else:
					user.timer = [time]

		#=====[ Tell user how to set timer ]=====
		if not found_time:
			ut.send_response(HOW_TO_SET_TIMER, user_id)
		else:
			ut.send_response(SET_TIMER + ', '.join([str(x) for x in user.timer]) + ' seconds', user_id	)
			ut.update(user_id, user)

	#========================[ Command used to clear all timers ]==========================#
	#																				       #
	#	usage: " clear timer "			   			   			       					   #
	#																					   #
	########################################################################################

	elif 'clear' in text and 'timer' in text:

		user.timer = []
		ut.send_response(CLEARED_TIMER, user_id)
		ut.update(user_id, user)

	#========================[ Command used to exit to idle mode ]=========================#
	#																				       #
	#	usage: " exit "			   			   			       					  	 	   #
	#																					   #
	########################################################################################

	elif text == 'exit':
		
		user.status = 'idle'
		ut.send_response(IDLE_MODE, user_id)
		ut.update(user_id, user)

	#=====================[ Command used to get help for any command ]=====================#
	#																				       #
	#	usage: " help [command] "			   			   			       				   #
	#																					   #
	########################################################################################

	elif 'help' in text:

		user_command = text.replace('help','').strip()

		#=====[ Check if user command is in our command shortcut list. If so, send appropriate help response ]=====
		for command in command_shortcuts:
			
			if user_command in command_shortcuts[command]:
				
				ut.send_response(command_list[command], user_id)
				return True

		#=====[ Tell user that we couldn't find specified command and send list of commands ]=====
		ut.send_response(HELP_COMMAND, user_id)
		ut.send_response('Here are a list of commands:\n\n' + '\n'.join(command_list.keys()), user_id)

	else:

		return False

	return True

def extract_int(text):
	
	number = None

	#=====[ regex to extract weight ]=====
	regex = r"\d+"

	if re.search(regex,text):

		match = re.search(regex, text)

		#=====[ Store weight ]=====
		number = int(match.group(0))
		
	return number





