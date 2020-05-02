import csv
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import tarfile
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
# nltk.download('vader_lexicon')

# self-defined modules
from Gender import GenderPredictor
from ScreenplayModel import ScreenplayModel

''' ==================================================================== '''

# global variables
model2 = []
model3 = []
model4 = []
model5 = []
model6 = []
no_model = []

def load_screenplay_formats():
	''' Loading correct film screenplay formats. '''

	global model2, model3, model4, model5, model6, no_model

	df = pd.read_csv('data/screenplay-formats.csv')
	model2 = df[df['format'] == 2]['file'].tolist()
	model3 = df[df['format'] == 3]['file'].tolist()
	model4 = df[df['format'] == 4]['file'].tolist()
	model5 = df[df['format'] == 5]['file'].tolist()
	model6 = df[df['format'] == 6]['file'].tolist()
	no_model = df[df['format'] == 0]['file'].tolist()

def load_model(filename):
	''' Loads film screenplay according to its corresponding format. '''

	if (filename in model2):
		return ScreenplayModel(filename, 2)
	elif (filename in model3):
		return ScreenplayModel(filename, 3)
	elif (filename in model4):
		return ScreenplayModel(filename, 4)
	elif (filename in model5):
		return ScreenplayModel(filename, 5)
	elif (filename in model6):
		return ScreenplayModel(filename, 6)
	elif (filename in no_model):
		return
	else:
		return ScreenplayModel(filename, 1)

def get_sentiment_score(m,c):
	''' m = ScreenplayModel; c = main character '''

	upper_names = [n.upper() for n in m.characters.keys()] # gets entire cast
	compound_sum = 0
	avg_compound = 0
	
	if c in m.char_lines:
		for l in m.char_lines[c]:
			scores = sia.polarity_scores(l)
			compound_sum += scores['compound']
		avg_compound = compound_sum / len(m.char_lines[c])

	return avg_compound

def get_network_info(m,c):
	''' m = ScreenplayModel; c = main character '''

	main_intxns, all_intxns = m.get_char_intxns(c)
	main_size = len(main_intxns)
	all_size = len(all_intxns)
	num_all_intxns = sum(all_intxns.values())
	num_main_intxns = num_all_intxns - main_intxns['Other']

	main_size_ratio = 0
	if (all_size > 0):
		main_size_ratio = main_size / all_size
	main_intxns_ratio = 0
	if (num_all_intxns > 0):
		main_intxns_ratio = num_main_intxns / num_all_intxns

	return main_size_ratio, main_intxns_ratio



''' ====================================================================
	MAIN PROGRAM
	==================================================================== '''
if __name__ == '__main__':
	load_screenplay_formats()
	sia = SIA() # sentiment analysis

	print('Starting to initialize gender predictor...')
	gp = GenderPredictor() # predict gender of names
	print('Done setting up gender predictor!')

	# lists to create df's later
	protag_rows = []
	mc_rows = []

	for filename in os.listdir(os.getcwd() + '/data/scriptbase/scriptbase_alpha'):
		if (filename != '.DS_Store'):
			m = load_model(filename)
			film = filename.replace('.tar.gz','')

			if (m != None): # film is parsable
				# building protagonist df
				protag = m.get_protag()
				protag_rows.append([film, protag])

				# looping through all main characters in a film
				for (mc,_) in (m.main_chars.items()):
					g = gp.predict(mc)
					lines_ratio = m.get_char_lines_ratio(mc)
					sentiment_score = get_sentiment_score(m,mc)
					main_size_ratio, main_intxns_ratio = get_network_info(m,mc)
					
					mc_row = [film, mc, g, lines_ratio, sentiment_score, main_size_ratio, main_intxns_ratio]
					mc_rows.append(mc_row)

	# save csv files of data
	protag_df = pd.DataFrame(protag_rows, columns=['film','protag'])
	protag_df.to_csv('data/protags.csv', index=False)
	print(protag_df.shape)
	print(protag_df.head(2))

	mc_cols = ['film','main_char','gender','lines_ratio','sentiment_score','main_network_ratio','main_intxn_ratio']
	mc_df = pd.DataFrame(mc_rows, columns=mc_cols)
	mc_df.to_csv('data/main_chars.csv', index=False)
	print(mc_df.shape)
	print(mc_df.head(2))





			