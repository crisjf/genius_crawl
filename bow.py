import pandas as pd
from crisjfpy import list_join
from collections import Counter,defaultdict
from cleanfunctions import *
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
try:
	import cPickle as pickle
except:
	import pickle

print 'Loading data...'
data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8')
data = data[data['prob']>0.5]

documents = data[data['prob']>0.5]['annotations'].values.tolist()
documents = list_join([split_annotations(doc) for doc in documents])
print 'Number of documents:',len(documents)

print 'Changing to bag of words representation...'
texts = [bagofwords(doc,lemmatizer) for doc in documents]

print 'Removing words that occurr only once...'
frequency = defaultdict(int,Counter(list_join(texts)))
texts = [[token for token in text if frequency[token] > 1] for text in texts]
pickle.dump(texts, open("processed_data/texts.p", "wb" ))

f = open('processed_data/texts.txt',mode='w')
for doc in texts:
    f.write((' '.join(doc)+'\n').encode('utf-8'))
f.close()
