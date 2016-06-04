import sys
sys.path.append('modules/')

from muscle_classifier import MuscleClassifier

grouped_muscles = {'back':['lats', 'middle back', 'traps','lower back'], 'legs': ['adductors','quadriceps', 'calves', 'hamstrings'], 'abs':['abdominals'], 'butt':['glutes', 'abductors'], 'arms':['forearms',  'triceps', 'biceps']}

#=====[ Key words ]=====
greetings = ['yo','hi','hello']
yes_words = ['yes', 'yah', 'sure', 'yup', 'ok', 'o.k.']
no_words = ['no', 'nope','nah','later']

#=====[ Muscle information ]=====
muscles = ['lats', 'chest', 'quadriceps', 'biceps', 'middle back', 'traps', 'shoulders', 'calves', 'abdominals', 'glutes', 'forearms', 'lower back', 'triceps', 'hamstrings', 'abductors', 'adductors', 'neck']
grouped_muscles = {'back':['lats', 'middle back', 'traps','lower back'], 'legs': ['adductors','quadriceps', 'calves', 'hamstrings'], 'abs':['abdominals'], 'butt':['glutes', 'abductors'], 'arms':['forearms',  'triceps', 'biceps']}

#=====[ Date information ]=====
months = ['Jan','Feb','Mar','April','May','June','July','Aug','Sep','Oct','Nov','Dec']

#=====[ Classifier ]=====
model = MuscleClassifier()

#=====[ Standard messages ]=====
GREETING = "Hey there!"
WELCOME_MESSAGE = "Hey there! I'm here to help you log and optimize your workouts. At any point, you can review a list commands by saying 'list commands' or 'ls'. Learn more about any command using 'help [command]'." 
COMMAND_INTRO = "For example, if you want to learn how to log a workout, just ask me 'How do I log a workout?' (or something along those lines). Some other things you can do include setting goals for working out certain muscles, setting timers in between each of your sets, reviewing your workouts (in terms of sets, volume, and muscle groups targeted)"
WORKOUT_INTRO = "Do you want to learn about how to log a workout?"
DEFAULT_IDLE_MESSAGE = "That's interesting... just let me know when you're starting your workout. I'll be ready. You can type 'ls' to see all commands."
IDLE_MODE = "Back in idle mode. Waiting on you, boss"
ERROR_MESSAGE = "I had trouble processing that. Let's try again? If that doesn't work, try just typing 'exit' to go back in to idle mode."
NO_PROBLEM = 'No problem!'
INSPIRATIONAL = ["Remember, what get's measured gets grown!", "It's not where you start but where you end up!", "It's all about the delta.", "You the best."]

#=====[ Workout logging messages ]=====
START_WORKOUT_MESSAGE = "Let's go baby, no pain = no gain. Record after each exercise."
DEFAULT_IDLE_MESSAGE = "That's interesting... just let me know when you're starting your workout. I'll be ready."
END_WORKOUT_MESSAGE = "Nice! Good workout!"
RECORDED_WORKOUT_MESSAGE = "Exercise recorded. Now get the fuck off your phone."
NO_EXERCISE_EXTRACTED_MESSAGE = "Could not figure out what exercise you did. Try again using the following: [x] reps of [exercise] at [weight]"
MESSAGE_LOGGED = "Logged your message, boss"
GOAL_EXERCISES = "Here are some examples of muscle groups you might want to specify: " + ' | '.join(grouped_muscles.keys())
SET_GOALS = "Try specifying the muscles you want to focus on by typing 'set goals: muscle1, muscle2, muscle3'"
UPDATED_GOALS = "Alright, I'll remember that you want to focus on"
HOW_TO_SET_TIMER = "Set a timer between each set by saying: set timer for [X] seconds. You can set multiple timers by separating the seconds by commas: set timer for 45, 60, and 90 seconds"
SET_TIMER = "Set timers in between sets: "
CLEARED_TIMER = "Cleared all timers."
TIMING_WARNING = "You've been resting for "
FINAL_TIMING_WARNING = "NEXT SET! LET'S GO! You've been resting for "
NO_WORKOUT_LOGGED = "Doesn't look like we got any sets logged. Didn't log that workout."
ERROR_MESSAGE = "I had trouble processing that. Let's try again? If that doesn't work, try just typing 'exit' to go back in to idle mode."
IDLE_MODE = "Back in idle mode. Waiting on you, boss"

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