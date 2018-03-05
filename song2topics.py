try:
	import cPickle as pickle
except:
	import pickle
from cleanfunctions import split_annotations
from functions import *
import numpy as np,matplotlib.pyplot as plt,pandas as pd,re
%matplotlib inline

#Load the topics ################################################

no_topics   = 50
no_features = 5000

if ("lda_"+str(no_topics)+"_"+str(no_features)+".p" not in os.listdir('processed_data'))|("nmf_"+str(no_topics)+"_"+str(no_features)+".p" not in os.listdir('processed_data')):
	raise NameError('Model not found')
[tf   ,tf_vectorizer   ,lda] = pickle.load(open("processed_data/lda_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
[tfidf,tfidf_vectorizer,nmf] = pickle.load(open("processed_data/nmf_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
tf_feature_names    = tf_vectorizer.get_feature_names()
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

#Choose a model between LDA and NMF #############################

modeltype = 'NMF'

if modeltype=='LDA':
	vectorizer    = tf_vectorizer
	feature_names = tf_feature_names
	model         = lda
elif modeltype=='NMF':
	vectorizer    = tfidf_vectorizer
	feature_names = tfidf_feature_names
	model         = nmf
else:
	raise NameError('Wrong model type')

#Load the annotated songs #######################################

data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8')
data = data[data['prob']>0.5]
data = pd.merge(data,pd.read_csv('processed_data/release_date.csv'))
data['release_year'] = map(int,[val[0] for val in data['release_date'].str.split('-')])

mydata = data[(data['release_year']>=1960)&(data['release_year']<=2017)]
mydata = mydata[['Song ID','release_year','annotations']]
mydata['explained_song'] = [re.sub(r'\n+','\n','\n'.join( split_annotations(doc) )) for doc in mydata['annotations']]

#Chose a song ###################################################

song_url    = 'https://genius.com/Kendrick-lamar-alright-lyrics'
song_id     = int(genius_url2id(song_url).split('/')[-1])
annotations = mydata[mydata['Song ID']==song_id]['explained_song'].values[0]
lyrics      = re.sub(r'\n+','\n',re.sub(r'\[[^\]]*\]','',song_lyrics(song_url).encode('utf-8'))).strip()

#Break a song into topics #####################################

x = vectorizer.transform([lyrics])
tsl = model.transform(x)[0]
tsl = tsl/sum(tsl)
tsl = pd.DataFrame(zip(range(len(tsl)),tsl),columns=['topic','pl'])

#Break the annotations into topics ##############################

x   = vectorizer.transform([annotations])
tsa = model.transform(x)[0]
tsa = tsa/sum(tsa)
tsa = pd.DataFrame(zip(range(len(tsa)),tsa),columns=['topic','pa'])

#Merge and sort #################################################

ts = pd.merge(tsl,tsa,how='outer').sort_values(by='pa',ascending=False)

