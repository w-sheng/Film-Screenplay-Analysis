import csv
import numpy as np
import pandas as pd
import tarfile
import os

''' ==================================================================== '''

def update_film_char(df):
	''' Returns the same pandas dataframe but with film_char column
	    parsed into two separate columns of film and main_char. '''

	list_of_rows = []
	for row in df.values.tolist():
		# fix encoding
	    film_char_raw = row[0].replace('%20',' ').replace('%22','"').replace('%23','#').replace('%3F','?')
	    film_char = film_char_raw.split('_')
	    film = film_char[0]
	    mc = film_char[1].replace('.txt','').lower()
	    
	    topic_scores = row[1:]
	    max_score = max(topic_scores)
	    top_topic = np.argmax(topic_scores) + 1
	    
	    new_row = [film, mc, top_topic]
	    list_of_rows.append(new_row)

	return pd.DataFrame(list_of_rows, columns=['film','main_char','top_topic'])


''' ====================================================================
	MAIN PROGRAM
	==================================================================== '''
if __name__ == '__main__':
	# get topic composition data
	composition_df = pd.read_csv('../data/topic_modeling/dialogue-composition10.csv')
	topics_df = update_film_char(composition_df)

	# get all main characters with identified genders
	mc_df = pd.read_csv('../data/main_chars.csv')
	mc_df['main_char'] = mc_df['main_char'].apply(lambda x: x.lower())
	mc_df = mc_df[~np.isnan(mc_df['gender'])][['film','main_char','gender']]

	# merge to find top topic
	res_df = mc_df.merge(topics_df, on=['film','main_char'], how='inner')
	res_df.to_csv('../data/char_topics10.csv', index=False)

