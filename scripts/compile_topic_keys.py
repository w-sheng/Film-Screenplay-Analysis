import csv
import os

if __name__ == '__main__':
	topics = []
	with open('../data/topic_modeling/archetypes/keys.txt') as f:
		for l in f:
			topics.append(l.split()[2:]) # add topic keywords
	f.close()

	for (i,t) in zip(range(1,26),topics):
		filename = '../data/topic_modeling/archetypes/topics/topic' + str(i) + '.txt'
		with open(filename, 'w') as output:
			output.write(' '.join(t))
		output.close()