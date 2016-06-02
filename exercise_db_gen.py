import urllib

base_url = 'http://www.bodybuilding.com/exercises/list/index/selected/'
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

results = []

for letter in letters:
    html = str(urllib.urlopen(base_url+letter).read())
    exercises = html.split('class="exerciseName">')[1:]

    for exercise in exercises:
        info = exercise.split('</a>')
        name = (info[0].split('>')[-1])
        targeted = (info[1].split('>')[-1])

        try:
            rating = (info[2].split("rating"))[1].split('<')[0].split('>')[1]
        except:
            rating = None
            
        results.append((name, targeted, rating))
        print name, targeted, rating
        
to_insert = []

for result in results:
    
    exercise = result[0].strip()
    muscle = result[1].strip()
    rating = result[2].strip() if result[2] else None
    
    to_insert.append({'exercise':exercise,'muscle':muscle,'rating':rating})

from pymongo import MongoClient

db_client = MongoClient()
db = db_client['exercise_db']

exercise_collection = db['exercises']