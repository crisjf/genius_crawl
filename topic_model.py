import os
from gensim import corpora, models, similarities
try:
	import cPickle as pickle
except:
	import pickle

print 'Loading texts...'
texts = pickle.load(open("processed_data/texts.p","rb"))

print 'Creating dictionary...'
if 'dictionary.p' in os.listdir('processed_data'):
	print '\tFound dictionary, loading...'
	dictionary = pickle.load(open("processed_data/dictionary.p","rb"))
else:
	dictionary = corpora.Dictionary(texts)
	pickle.dump(dictionary, open("processed_data/dictionary.p", "wb" ))

print 'Creating corpus...'
if 'corpus.p' in os.listdir('processed_data'):
	print '\tFound corpus, loading...'
	corpus = pickle.load(open("processed_data/corpus.p","rb"))
else:
	corpus = [dictionary.doc2bow(text) for text in texts]
	pickle.dump(corpus, open("processed_data/corpus.p", "wb" ))

num_topics=100
print 'Running the model with',num_topics,'topics...'
model_lda = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics)
pickle.dump(model_lda , open("processed_data/model_lda_"+str(num_topics)+"topics.p", "wb" ))
