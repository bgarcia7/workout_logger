from pymongo import MongoClient

#=====[ Set up Mongo DB ]=====
db_client = MongoClient()

db = db_client['brandon_workout_db']
# db = db_client['test_workout_db']


# master_users = db['users']

users = db['test_users']


# users.remove()
# users = db['users']