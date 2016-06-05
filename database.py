from pymongo import MongoClient


server_token = 'EAAYWALshr2kBAIVdPVwKscuFZAGjdB2dJzFx1qd8JA3bMnDTaZCr0fH0avAlPfLv72yBFEVtSXgXICMGWXZCbHS97OgZA5Q4qF0xdZAFRs0CtQ5HpMGUuNZCHJoewtR5ZCdKZA0UdHGwR6FZAETigcCYOU1bPH6xH00yfgV7ZASpGhbgZDZD'
kelvin_token = 'EAAak1FpgZAygBAFkr1NOD2DJUwL4r3j74VScIDCMmW4bpBvfnoQi1VmS1KvZCFM0yooJ7Sisg8IUcioQReVAFt25RwberE8olwX8Vsre412IaNdc07fV4GDYIS4bsil4dJmRtp2r6nud8I8SeOGB8R6IO1I8E1td8QljAQNwZDZD'
brandon_token = 'EAAYjxWLX4AUBAG8W5qtCZBhmaNulNn2CtlsFP4ppNZCgiygOrafREWsLFDWZChDQ27fUMs7jpKyt5I56n8Q76ESlORNnOjYYZCIOAZCp5sHhZBIBkZCDeZBi5Yr1uiLNVlZB1WxfYx1vz8ZC9x9WYAelh4vQnz2rZCZAB9EkX5eBoFoRpAZDZD'

token = server_token

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



