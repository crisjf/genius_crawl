import pandas as pd,re,nltk
from numpy import log
from sklearn.svm import SVC

def _normalize(s):
    n = re.sub(r'\([^\)]*\)',' ',s)
    n = re.sub(r'\[[^\)]*\]',' ',n)
    n = re.sub(r' +',' ',n)
    punctuation = {'.',',',';',':','?','!','-','+','|',' ',"'"}
    for p in punctuation:
        n = n.replace(p,'')
    return n

def _str(s):
    try:
        s.lower()
        return s
    except:
        return str(s)

def get_feats(row):
    '''Returns a dictionary with the features used for the classifier'''
    non_artists = {'kingofthedot','rapgenius','geniususers','geniuslists','genius','thebreakfastclub','noisey','dontflop','versusbattle','urltv','udubbnetwork','popgenius','rapgeniuseditors','mtv','entertainmenttonight','theextra','producergenius','xxl','splashmag','top4','#12for12boston','funkvolume','bet','rockgenius','popgenius','rapgeniusranch','outsidethelineswithrapgenius','sciencegenius','rapgeniususers','epicrapbattlesofhistory'} #use only lower case, and no punctuation signs or parenthesis
    
    title  = _str(row['Title']).lower()
    artist = _str(row['Primary Artist']).lower()
    feats = {}
    #feats['n_annotations'] = log(row['n_annotations']+1)
    feats['n_annotations'] = row['n_annotations']
    feats['len_annotations'] = log(row['len_annot']+1)
    feats['primary_tag'] = row['Primary Tag']
    feats['l_name'] = len(row['Title'])
    feats['vs'] = ('vs' in title)|('versus' in title)
    feats['tracklist'] = ('tracklist' in title)
    feats['itw'] = ('interview' in title)|('itw' in title)
    feats['ge_name'] = ('genius' in title)
    feats['ge_artist'] = ('genius' in artist)
    feats['ge_album'] = ('genius' in _str(row['Primary Album']).lower())
    feats['has_album'] = (row['Primary Album']!='NULL')
    feats['non-artist'] = (_normalize(artist).lower() in non_artists)
    return feats

#Read the data and the training set
data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned.csv',encoding='utf-8').fillna('NULL')
data_train = pd.read_csv('processed_data/songs_training.csv',encoding='utf-8').drop_duplicates()
if len(data_train)!=len(set(data_train['Song ID'])):
    raise NameError('Check the training set')

#Create a testing set (the size of the testing set is set to 0% for running the classifier)
data_test = data_train.sample(int(len(data_train)*0.))
data_train = data_train[~data_train['Song ID'].isin(data_test['Song ID'])]
data_train = pd.merge(data,data_train)
data_test = pd.merge(data,data_test)
data = data[~data['Song ID'].isin(data_train['Song ID'])]
data = data[~data['Song ID'].isin(data_test['Song ID'])]
print len(data),len(data_train),len(data_test)

#Convert data to features
train_set = [(get_feats(row),row['is_song']) for index,row in data_train.iterrows()]

#Train the classifier
classifier = nltk.classify.SklearnClassifier(SVC(kernel='linear',probability=True))
classifier.train(train_set)

#Use it to classify the rest of the data
for index,row in data.iterrows():
    probs = classifier.prob_classify(get_feats(row))
    data.loc[index,'prob'] = probs.prob(True)

#Add the training data to the final output
data_train['prob'] = 0
data_train.loc[data_train['is_song'],'prob'] = 1
data = pd.concat([data,data_train]).drop('is_song',1)

#Save the classified data
data.to_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8',index=False)