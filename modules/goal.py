import sys
sys.path.append('../')

from muscle_detector import muscles, grouped_muscles
from fuzzywuzzy import fuzz
from collections import defaultdict
from resources import *
import utils as ut
import re

def set(user, user_id, text):

	muscle_groups = defaultdict(list)

	text_muscles = [x.strip() for x in re.split(',|and',text) if x.strip()]
	
	#=====[ Check to see if each item in text matches against a muscle group ]=====
	for muscle in text_muscles:
		
		#=====[ Checks for individual muscles: e.g. lats, traps]=====
		if muscle in muscles:
			muscle_groups['specific'].append(muscle)
		#=====[ Checks for muscle groups: e.g. back, legs ]=====
		elif muscle in grouped_muscles:
			muscle_groups['group'].append(muscle)

	#=====[ If no muscle groups found, inform user of possible muscle groups to specify ]===== 
	if not len(muscle_groups):
		ut.send_response(GOAL_EXERCISES, user_id)
		return 
			
	#=====[ Update user object ]=====            
	user.goals = muscle_groups
	for key in user.goals.keys():
		print key
		for key2 in user.goals[key]:
			print key2
	ut.update(user_id, user)
	
	message = UPDATED_GOALS + ', '.join(user.goals['specific'])
	message += ', ' + ', '.join(user.goals['group']) if user.goals['group'] else ''

	ut.send_response(message, user_id)


grouped_muscles = {'back':['lats', 'middle back', 'traps','lower back'], 'legs': ['adductors','quadriceps', 'calves', 'hamstrings'], 'abs':['abdominals'], 'butt':['glutes', 'abductors'], 'arms':['forearms',  'triceps', 'biceps']}

def review(user, user_id, days=7, num_muscles=7):
	""" Provides feedback on muscles targeted over the past week """

	#=====[ Get muscle groups and target muscle groups ]=====
	values, labels = user.get_muscle_groups(days, num_muscles, False)
	target_muscles = user.goals

	#=====[ Initialize holders ]=====
	summary = ''
	not_targeted = []
	barely_targeted = []
	not_targeted_groups = defaultdict(list)
	barely_targeted_groups = defaultdict(list)

	#=====[ Get indices of muscles that have been heavily focused on ]=====
	focus_idxs = [idx for idx, val in enumerate(values) if val > 30]

	if focus_idxs:
		ut.send_response("You've focused heavily on " + ', '.join([labels[idx] for idx in focus_idxs]), user_id)

	#=====[ Check to see if each specific target muscle has been worked out and, if it has, to what degree ]=====
	for muscle in target_muscles['specific']:
		if muscle not in labels:

			not_targeted.append(muscle)

		else:
			
			idx = labels.index(muscle)
			
			if values[idx] < 10:
				barely_targeted.append(muscle)

	#=====[ Check to see which (if any) specific target muscles within specified larger muscle groups have been worked out, 
	#=====[ and, if they have, to what degree 
	for muscle_group in target_muscles['group']:

		for muscle in grouped_muscles[muscle_group]:

			if muscle not in labels:

				not_targeted_groups[muscle_group].append(muscle)

			else:
				
				idx = labels.index(muscle)
				
				if values[idx] < 10:
					barely_targeted_groups[muscle_group].append(muscle)

	#=====[ Formulate muscle review message for specific muscles ]=====
	message = ''
	
	for muscle in not_targeted:

		message += 'You have not targeted ' + ', '.join(not_targeted) + ' at all. '

	for muscle in barely_targeted:

		message += 'You have not focused much on ' + ', '.join(barely_targeted) + '. '

	#=====[ Send update for specific muscles ]=====
	if message:
		ut.send_response(message, user_id)

	message = ''

	#=====[ Formulate muscle review message for muscle groups ]=====
	for muscle_group in not_targeted_groups:

		message += "You wanted to focus on " + muscle_group + ", but you have not worked out " + ', '.join(not_targeted_groups[muscle_group]) + '. '

	for muscle_group in barely_targeted_groups:

		message += "For " + muscle_group + ", you've barely worked out " + ', '.join(barely_targeted_groups[muscle_group]) + '. '

	if message: 
		ut.send_response(message, user_id)
	








