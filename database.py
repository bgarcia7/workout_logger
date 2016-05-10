from pymongo import MongoClient

#=====[ Set up Mongo DB ]=====
db_client = MongoClient()

# db = db_client['brandon_workout_db']
db = db_client['test_workout_db']


users = db['users']
# users.remove()
# users = db['users']