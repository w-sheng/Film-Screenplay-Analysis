import csv
import pandas as pd
import sys
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
	f = sys.argv[1] + '.tar.gz'
	c = sys.argv[2]
	load_screenplay_formats()
	mc_df = pd.read_csv('../data/main_chars.csv')

	m = load_model(f)
	m.draw_graph(mc_df)
	m.draw_char_graph(mc_df,c)



