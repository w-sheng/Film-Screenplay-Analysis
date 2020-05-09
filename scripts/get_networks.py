import csv
import matplotlib.pyplot as plt
import networkx as nx
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

	# list to create df later
	cent_rows = []
	for filename in os.listdir(os.getcwd() + '/../data/scriptbase/scriptbase_alpha'):
		if (filename != '.DS_Store'):
			m = load_model(filename)
			film = filename.replace('.tar.gz','')

			if (m != None): # film is parsable
				all_dc = list(nx.degree_centrality(m.G).values())
				mu_dc = np.mean(all_dc)
				std_dc = np.std(all_dc)
				
				all_bc = list(nx.betweenness_centrality(m.G).values())
				mu_bc = np.mean(all_bc)
				std_bc = np.std(all_bc)
				
				# looping through all main characters in a film
				for (mc,_) in (m.main_chars.items()):
					dc = nx.degree_centrality(m.G)[mc]
					dc_norm = (dc - mu_dc) / std_dc
					bc = nx.betweenness_centrality(m.G)[mc]
					bc_norm = (bc - mu_bc) / std_bc
					cent_rows.append([film, mc, dc_norm, bc_norm])

	# save data
	cent_df = pd.DataFrame(cent_rows, columns=['film','main_char','degree','betweenness'])
	cent_df.to_csv('../data/centralities.csv', index=False)
	print(cent_df.head(2))
	
