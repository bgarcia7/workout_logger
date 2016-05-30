import sys
sys.path.append('modules/')

from muscle_classifier import MuscleClassifier
from muscle_detector import grouped_muscles

#=====[ Standard messages ]=====
WELCOME_MESSAGE = "Start a workout / end a workout. Just text me."
START_WORKOUT_MESSAGE = "Let's go baby, no pain = no gain. Record after each exercise."
DEFAULT_IDLE_MESSAGE = "That's interesting... just let me know when you're starting your workout. I'll be ready."
END_WORKOUT_MESSAGE = "Nice! Good workout!"
RECORDED_WORKOUT_MESSAGE = "Exercise recorded. Now get the fuck off your phone."
NO_EXERCISE_EXTRACTED_MESSAGE = "Could not figure out what exercise you did. Try again using the following: [x] reps of [exercise] at [weight]"
MESSAGE_LOGGED = "Logged your message, boss"
GOAL_EXERCISES = "Here are some examples of muscle groups you might want to specify: " + ' | '.join(grouped_muscles.keys())
SET_GOALS = "Try specifying the muscles you want to focus on by typing 'set goals: muscle1, muscle2, muscle3'"
UPDATED_GOALS = "Alright, I'll remember that you want to focus on"

#=====[ Feedback Messages ]=====
FEEDBACK_QUESTION = "Would you like to give feedback by answering 3 quick questions?"
FEEDBACK_CLARIFY = "Sorry I didn't quite get that, please answer yes or no"
RATING_QUESTION = "How likely are you to repeat this workout in the future? Please enter a number from 1 to 10"
RATING_CLARIFY = "Sorry I didn't quite get that, please enter a number from 1 to 10"
DIFFICULTY_QUESTION = "How difficult did you find this workout? Please enter a number from 1 to 5"
TIREDNESS_QUESTION = "How tired are you after this workout? Please enter a number from 1 to 5"
DIFF_TIRED_CLARIFY = "Sorry I didn't quite get that, please enter a number from 1 to 5"
FEEDBACK_END = "Thank you! Your feedback has been recorded"
QUESTION_END = "Got it, thanks!"

months = ['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec']

model = MuscleClassifier()