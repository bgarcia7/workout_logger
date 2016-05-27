import sys
sys.path.append('../')

from muscle_detector import muscles, grouped_muscles
from fuzzywuzzy import fuzz
from collections import defaultdict
from resources import *
import utils as ut
import re

def process(user, user_id, text):

	muscle_groups = defaultdict(list)

	text_muscles = [x.strip() for x in re.split(',|and',text) if x.strip()]

	print text_muscles
	
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
	ut.update(user_id, user)
	ut.send_response(UPDATED_GOALS + ', '.join(user.goals['specific']) + ' ' + ', '.join(user.goals['group']), user_id)




