# import os
# from gensim import corpora, models, similarities
import sys
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
try:
	import cPickle as pickle
except:
	import pickle

args = sys.argv
if len(args)<3:
	print 'Warning: Setting number of topics to default. To change the number of topics run\n>>> python topic_model.py 200 1000'
	no_topics   = 50
	no_features = 1000
else:
	no_topics   = int(args[1])
	no_features = int(args[2])

print 'Number of topics: ',no_topics
print 'Numer of features:',no_features
print 'Loading texts...'
texts = pickle.load(open("processed_data/texts.p","rb"))
print 'Number of texts:',len(texts)
documents = [' '.join(t) for t in texts]


# Run NMF
print 'Running NMF...'
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()
nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

print 'Saving NMF...'
pickle.dump([tfidf,tfidf_vectorizer,nmf], open("processed_data/nmf_"+str(no_topics)+"_"+str(no_features)+".p", "wb" ))

# Run LDA
# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
print 'Running LDA...'
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

print 'Saving LDA...'
pickle.dump([tf,tf_vectorizer,lda], open("processed_data/lda_"+str(no_topics)+"_"+str(no_features)+".p", "wb" ))





# print 'Loading texts...'
# texts = pickle.load(open("processed_data/texts.p","rb"))

# print 'Creating dictionary...'
# if 'dictionary.p' in os.listdir('processed_data'):
# 	print '\tFound dictionary, loading...'
# 	dictionary = pickle.load(open("processed_data/dictionary.p","rb"))
# else:
# 	dictionary = corpora.Dictionary(texts)
# 	pickle.dump(dictionary, open("processed_data/dictionary.p", "wb" ))

# print 'Creating corpus...'
# if 'corpus.p' in os.listdir('processed_data'):
# 	print '\tFound corpus, loading...'
# 	corpus = pickle.load(open("processed_data/corpus.p","rb"))
# else:
# 	corpus = [dictionary.doc2bow(text) for text in texts]
# 	pickle.dump(corpus, open("processed_data/corpus.p", "wb" ))


# print 'Running the model with',num_topics,'topics...'
# model_lda = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics)
# pickle.dump(model_lda , open("processed_data/model_lda_"+str(num_topics)+"topics.p", "wb" ))
