import cPickle as pickle
from cleanfunctions import split_annotations
from functions import *
import numpy as np,matplotlib.pyplot as plt,pandas as pd,re

no_topics   = 50
no_features = 5000
modeltype = 'NMF'

print 'Creating topics for cities using '+modeltype+' with '+str(no_topics)+' topics and '+str(no_features)+' features.'

#Load the topics ################################################

print 'loading topics...'

if ("lda_"+str(no_topics)+"_"+str(no_features)+".p" not in os.listdir('processed_data'))|("nmf_"+str(no_topics)+"_"+str(no_features)+".p" not in os.listdir('processed_data')):
    raise NameError('Model not found')
[tf   ,tf_vectorizer   ,lda] = pickle.load(open("processed_data/lda_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
[tfidf,tfidf_vectorizer,nmf] = pickle.load(open("processed_data/nmf_"+str(no_topics)+"_"+str(no_features)+".p","rb"))
tf_feature_names    = tf_vectorizer.get_feature_names()
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

#Choose a model between LDA and NMF #############################

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

#Topic to words #################################################

print 'mapping topics to words...'

topics = []
ti=0
for topic in model.components_:
    size = sum(topic)
    topic = topic/sum(topic)
    topic = pd.DataFrame(zip([feature_names[i] for i in range(len(topic))],topic.tolist()),columns=['word','prob']).sort_values(by='prob',ascending=False)
    topic = topic[topic['prob']>=topic['prob'].max()*0]
    topic['topic'] = ti
    ti+=1
    topics.append(topic)
topics = pd.concat(topics)
topics = topics[topics['prob']!=0][['topic','word','prob']]
topics.to_csv('processed_data/topic2words_'+modeltype.lower()+"_"+str(no_topics)+"_"+str(no_features)+".csv",encoding='utf-8',index=False)

#Load the annotated songs #######################################

print 'loading annotated songs and artist msa...'

data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8')
data = data[data['prob']>0.5]
data = pd.merge(data,pd.read_csv('processed_data/release_date.csv'))
data['release_year'] = map(int,[val[0] for val in data['release_date'].str.split('-')])

data = data[(data['release_year']>=1960)&(data['release_year']<=2017)]
data = data[['Song ID','release_year','annotations','Primary Artist ID']]
data['explained_song'] = [re.sub(r'\n+','\n','\n'.join( split_annotations(doc) )) for doc in data['annotations']]

artist_msa = pd.read_csv('processed_data/artist_origin_msa.csv')
a2m = pd.DataFrame([],columns=['Primary Artist ID','NAME'])
tagOrder = ['origin','formation','work_location']
for t in tagOrder:
    a2m = pd.concat([a2m,artist_msa[(artist_msa['tag']==t)&(~artist_msa['Primary Artist ID'].isin(set(a2m['Primary Artist ID'].values)))][['Primary Artist ID','NAME']].drop_duplicates()])
print len(a2m),len(set(a2m['Primary Artist ID']))

data = pd.merge(data,a2m)

#Break songs into topics and merge with cities ##################

print 'breaking songs into topics...'

songs = []
for songId,annotations in data[['Song ID','annotations']].values:
    x   = vectorizer.transform([annotations])
    tsa = model.transform(x)[0]
    if sum(tsa)!=0:
        tsa = tsa/sum(tsa)
        tsa = pd.DataFrame(zip(range(len(tsa)),tsa),columns=['topic','pa'])
        tsa['Song ID'] = songId
        tsa = tsa[tsa['pa']!=0]
        songs.append(tsa[['Song ID','topic','pa']])
songs = pd.concat(songs)

print 'writing results...'

songs.to_csv('processed_data/songs2topics_'+modeltype.lower()+"_"+str(no_topics)+"_"+str(no_features)+".csv")
cities = pd.merge(songs,data[['Song ID','NAME']])
cities.groupby(['NAME','topic']).mean()[['pa']].reset_index().groupby(['NAME','topic']).mean().reset_index().to_csv('processed_data/msa2topics_'+modeltype.lower()+"_"+str(no_topics)+"_"+str(no_features)+".csv")

