import csv
import nltk
import numpy as np
import pandas as pd
import tarfile
import os

# self-defined modules
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

	df = pd.read_csv('../data/screenplay-formats.csv')
	model2 = df[df['format'] == 2]['file'].tolist()
	model3 = df[df['format'] == 3]['file'].tolist()
	model4 = df[df['format'] == 4]['file'].tolist()
	model5 = df[df['format'] == 5]['file'].tolist()
	model6 = df[df['format'] == 6]['file'].tolist()
	no_model = df[df['format'] == 0]['file'].tolist()

def is_model1(f):
	''' Returns if film has model 1 screenplay formatting. '''

	global model2, model3, model4, model5, model6, no_model

	m0 = f not in no_model
	m2 = f not in model2
	m3 = f not in model3
	m4 = f not in model4 
	m5 = f not in model5 
	m6 = f not in model6

	return (m0 and m2 and m3 and m4 and m5 and m6)


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




''' ====================================================================
	MAIN PROGRAM
	==================================================================== '''
if __name__ == '__main__':
	load_screenplay_formats()
	df = pd.read_csv('../data/main_chars.csv')
	mc_df = df[~np.isnan(df['gender'])] # removed chars w unidentified gender

	for filename in os.listdir(os.getcwd() + '/../data/scriptbase/scriptbase_alpha'):
		if (filename != '.DS_Store'):
			m = load_model(filename)
			film = filename.replace('.tar.gz','')

			if (m != None): # film is parsable
				film_df = mc_df[mc_df['film'] == film][['main_char']]

				# if is model 1, also topic model directions
				do_dirs_model = is_model1(filename) 

				for (_,row) in film_df.iterrows():
					mc = row['main_char']

					# topic model dialogue
					dialogue = ''
					if mc in m.char_lines:
						dialogue = m.remove_char_names(m.char_lines[mc])

					# issue with parsing dialogue vs dirs -
					# treat all dirs lines as dialogue lines
					else: 
						do_dirs_model = False
						mc_dialogue = 'DIRECTIONS - ' + mc
						if mc_dialogue in m.char_lines:
							dialogue = m.remove_char_names(m.char_lines[mc_dialogue])
						else:
							continue
					
					dialogue_file = '../data/topic_modeling/dialogue/' + film + '_' + mc + '.txt'
					with open(dialogue_file, 'w') as output:
						output.write(dialogue)
					output.close()

					# topic model directions (if applicable)
					if do_dirs_model:
						dirs = ''
						mc_dirs = 'DIRECTIONS - ' + mc
						if mc_dirs in m.char_lines:
							dirs = m.remove_char_names(m.char_lines[mc_dirs])
						
							dirs_file = '../data/topic_modeling/dirs/' + film + '_' + mc + '.txt'
							with open(dirs_file, 'w') as output:
								output.write(dirs)
							output.close()

