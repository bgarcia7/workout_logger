from pymongo import MongoClient


token = 


#=====[ Set up Mongo DB ]=====
db_client = MongoClient()

#=====[ Use this DB for Live server ]=====
db = db_client['production_db']
#=====[ Use this db for testing ]=====
# db = db_client['test_workout_db']
ex_db = db_client['exercise_db']

# db = db_client['brandon_workout_db']

users = db['users']

#===================[ Exercise collection schema ]==================#
#																	#
#		'exercise': name of the exercise 							#
#		'muscle': the muscle group that the exercise targets 		#
#		'rating': ratings as assigned by users on bodybuilding.com  #
#																	#
#####################################################################	

templates = db['workout_templates']


#===================[ Exercise collection schema ]==================#
#																	#
#		'exercise': name of the exercise 							#
#		'muscle': the muscle group that the exercise targets 		#
#		'rating': ratings as assigned by users on bodybuilding.com  #
#																	#
#####################################################################																	#	

exercise_collection = ex_db['exercises']



