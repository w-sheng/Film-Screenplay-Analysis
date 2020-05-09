import csv
import nltk
import numpy as np
import pandas as pd
import os
import tarfile
import sys

from sklearn.feature_extraction.text import TfidfVectorizer

''' ==================================================================== '''

def get_doc_text(filename):
	''' Given a filename, return a string list representation of 
	    its contents. '''

	contents = []
	with open(filename, 'r') as f:
		contents = f.readlines()
	f.close()

	return ' '.join(contents)


''' ====================================================================
	MAIN PROGRAM
	==================================================================== '''
if __name__ == '__main__':
	f_arg = sys.argv[1] # either 'common' or 'hero'
	arch_folder = os.getcwd() + '/../data/topic_modeling/archetypes/' + f_arg
	texts = []
	files = []

	texts.append(get_doc_text(arch_folder + '/aphrodite.txt'))

	# for f in os.listdir(arch_folder): # add all archetype description texts
	# 	file = arch_folder + '/' + f
	# 	texts.append(get_doc_text(file))
	# 	files.append(f.replace('.txt',''))

	topic_folder = os.getcwd() + '/../data/topic_modeling/archetypes/topics'
	texts.append(get_doc_text(topic_folder + '/topic5.txt'))
	# for f in os.listdir(topic_folder): # add all archetype description texts
	# 	file = topic_folder + '/' + f
	# 	texts.append(get_doc_text(file))
	# 	files.append(f.replace('.txt',''))

	tfidf = TfidfVectorizer().fit_transform(texts)
	pairwise_similarity = tfidf * tfidf.T
	print(pairwise_similarity)

	# res_file = f_arg + '_topic_similarity.csv'
	# res_path = os.getcwd() + '/../data/topic_modeling/archetypes/' + res_file
	# np.savetxt(res_path, pairwise_similarity.A, delimiter=',')

