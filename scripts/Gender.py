import gensim.downloader as api
import re

class GenderPredictor(object):
	''' A model to predict the gender of a character based on their name. '''

	def __init__(self):
		self.model = api.load('glove-wiki-gigaword-300')

	def predict(self, word):
	    word_split = word.lower().split()
	    vector = [re.sub(r'[^\w\s]','',w) for w in word_split]

	    all_in = True
	    for v in vector:
	        if v not in self.model:
	            all_in = False
	        
	    if all_in:
	        male = self.model.n_similarity(vector,['masculinity'])
	        female = self.model.n_similarity(vector,['femininity'])

	        # 0: male, 1: female
	        label = 0 if male > female else 1

	        return label
	    
	    else:
	        print(word)
	        return float('NaN')
