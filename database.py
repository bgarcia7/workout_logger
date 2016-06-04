from pymongo import MongoClient

#=====[ Set up Mongo DB ]=====
db_client = MongoClient()

# db = db_client['brandon_workout_db']
db = db_client['test_workout_db']
# db = db_client['test_workout_db_2']



users = db['users']

#=====[ Used to drop user collection ]=====
# users.remove()
# users = db['users']


ex_db = db_client['exercise_db']

#===================[ Exercise collection schema ]==================#
#																	#
#		'exercise': name of the exercise 							#
#		'muscle': the muscle group that the exercise targets 		#
#		'rating': ratings as assigned by users on bodybuilding.com  #
#																	#
#####################################################################																	#	

exercise_collection = ex_db['exercises']