import unittest
from unittest import TestCase
from modules.workout_log import extract_exercise
from classes.xset import xSet

class Test(TestCase):

    def test_extract_exercise(self):
        test_strs =  [
            ("10 reps of bench press at 40", ["bench press", "40", "10"]),
            ("10 rep @ 150", ["", "150", "10"]),
            ("10 reps bench @ 150", ["bench", "150", "10"])
                      ]
        for i, (test_str, gold) in enumerate(test_strs):
            # Compare string so assertion error is more readable
            self.assertEqual(str(extract_exercise(test_str)), str(xSet(*gold)))




