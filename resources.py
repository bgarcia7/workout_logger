import sys
sys.path.append('modules/')

from muscle_classifier import MuscleClassifier

#=====[ Key words ]=====
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
WELCOME_MESSAGE = "Hey there! I'm here to help you log and optimize your workouts. At any point, you can review a list commands by saying 'list commands' or 'ls'. Learn more about any command using 'help [command]'." 
COMMAND_INTRO = "For example, if you want to learn how to log a workout, just ask me 'How do I log a workout?' (or something along those lines). Some other things you can do include setting goals for working out certain muscles, setting timers in between each of your sets, reviewing your workouts (in terms of sets, volume, and muscle groups targeted)"
WORKOUT_INTRO = "Do you want to learn about how to log a workout?"
DEFAULT_IDLE_MESSAGE = "That's interesting... just let me know when you're starting your workout. I'll be ready."
IDLE_MODE = "Back in idle mode. Waiting on you, boss"
ERROR_MESSAGE = "I had trouble processing that. Let's try again? If that doesn't work, try just typing 'exit' to go back in to idle mode."

#=====[ Workout logging messages ]=====
START_WORKOUT_MESSAGE = "Let's go baby, no pain = no gain. Record after each exercise."
END_WORKOUT_MESSAGE = "Nice! Good workout!"
RECORDED_WORKOUT_MESSAGE = "Exercise recorded. Now get the fuck off your phone."
NO_EXERCISE_EXTRACTED_MESSAGE = "Could not figure out what exercise you did. Try again using the following: [x] reps of [exercise] at [weight]"
NO_WORKOUT_LOGGED = "Doesn't look like we got any sets logged. Didn't log that workout."
TIMING_WARNING = "You've been resting for "
FINAL_TIMING_WARNING = "NEXT SET! LET'S GO! You've been resting for "

#=====[ Command messages ]=====
MESSAGE_LOGGED = "Logged your message, boss"
GOAL_EXERCISES = "Here are some examples of muscle groups you might want to specify: " + ' | '.join(grouped_muscles.keys())
SET_GOALS = "Try specifying the muscles you want to focus on by typing 'set goals: muscle1, muscle2, muscle3'"
UPDATED_GOALS = "Alright, I'll remember that you want to focus on"
HOW_TO_SET_TIMER = "Set a timer between each set by saying: set timer for [X] seconds. You can set multiple timers by separating the seconds by commas: set timer for 45, 60, and 90 seconds"
SET_TIMER = "Set timers in between sets: "
CLEARED_TIMER = "Cleared all timers."
HELP_COMMAND = "Sorry, I couldn't find that command."
WORKOUT_START_INSTRUCTIONS = "Type 'start workout' to begin a workout. Then you can start logging some subroutine. A subroutine is either a circuit or single exercise. A single exercise can be something like squat sets. A circuit is a set of exercises you do in rapid succession: squats, followed by lunges, followed by box jumps"
WORKOUT_SET_INITIALIZATION = "To start logging a single exercise, just let me know how many reps you did, what exercise it was, and what weight (if any) you did it at. Here are several examples of how you could tell me:\n\n I just did 15 reps of squats at 135 pounds\n20 reps of pushups\n10 reps of bench press at 185\n\nWhen you're first logging an exercise, make sure to specify reps first, followed by the exercise (and use the word 'reps' ;))"
WORKOUT_SET_CONTINUATION = "After you've logged your first set for an exercise, I know now what exercise you're working on and you can simply denote reps and weight (if any). Here are some examples:\n\n10 reps at 30 pounds\n10 at 20\n10 <--- I'll assume these are just reps\n\nWhen you move on to your next exercise, simply log a new exercise as described above or a new circuit as described below."
WORKOUT_CIRCUIT_INITIALIZATION = "To start logging a circuit, you must tell me that you are starting a circuit and list the exercises you will do. Here are some examples:\n\nstart circuit: bench press, squats, lunges\ncircuit bench press, lunges "
WORKOUT_CIRCUIT_CONTINUATION = "Once you've started a circuit, you can log reps and weights for each exercise just like with sets:\n\n10 at 20\n10 reps at 20 pounds\n\nI will automatically move through each circuit exercise, so that each rep/weight that you log will be recorded for the next exercise in the circuit. If you want to go out of order in your circuit (or you skipped one of the exercises, for example), just log the appropriate exercise in addition to your reps like so:\n\n10 reps of [exercise in circuit] at 20 pounds"
WORKOUT_TIMER = "You can set timers in between sets so that I can remind you when to move on. Type 'help set timer' for more info"
LEARN_ABOUT_CIRCUITS = "Do you want to learn about how to log circuits?"
DONE_INSTRUCTIONS = "Alrighty then. Remember: to get started, type 'start workout'"
ASSUME_DONE_INSTRUCTIONS = "I'll take that as a 'no'. Remember: to get started, type 'start workout'"

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
NO_FEEDBACK = "No worries. Maybe next time!"
