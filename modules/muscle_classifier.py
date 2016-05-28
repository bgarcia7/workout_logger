from database import *
from sklearn import feature_extraction
from sklearn import preprocessing
from sklearn.pipeline import FeatureUnion
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
import pickle
import numpy as np

class MuscleClassifier():

	def __init__(self, auto_load=True):
		""" Initializes our MuscleClassifier
			Option to preload it or start from fresh model 
		"""

		#=====[ If auto_load, then we rehydrate our existing models ]=====
		if auto_load:

			self.model = pickle.load(open('modules/pickled/muscle_classifier.p','r'))
			self.le = pickle.load(open('modules/pickled/muscle_classifier_le.p','r'))
			self.vectorizer = pickle.load(open('modules/pickled/muscle_classifier_vectorizer.p','r'))

		else:

			self.model = BernoulliNB()

	def train(self, muscle_groups, labels):
		""" 
			Vectorizes raw input and trains our classifier 
		"""

		#=====[ Instantiate label encoder to turn text labels into ints ]=====
		self.le = preprocessing.LabelEncoder()

		#=====[ Declare vectorizers and merge them via a FeatureUnion ]=====
		char_vzr = feature_extraction.text.CountVectorizer(lowercase=True, ngram_range=(3,8), analyzer='char', encoding='utf-8')
		word_vzr = feature_extraction.text.CountVectorizer(lowercase=True, ngram_range=(1,5), analyzer='word', encoding='utf-8')

		self.vectorizer = FeatureUnion([('char',char_vzr),('word',word_vzr)])

		#=====[ Transform our input and labels ]=====
		X = self.vectorizer.fit_transform(muscle_groups).toarray()
		Y = self.le.fit_transform(labels)

		#=====[ Fit our model and then run inference on training data ]=====
		self.model.fit(X,Y)
		y = self.model.predict(X)

		#=====[ Report Traning Accuracy ]=====
		print "Training Accuracy: %f " % (sum(y != Y)/float(len(Y)))

	def predict(self, exercises):
		""" Takes in raw input, vectorizes it, and reports back predicted muscle group """

		X = self.vectorizer.transform(exercises).toarray()
		y = self.model.predict(X)

		return self.le.classes_[y]
