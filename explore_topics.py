try:
	import cPickle as pickle
except:
	import pickle
import numpy as np,matplotlib.pyplot as plt,pandas as pd
%matplotlib inline

def bar(topic,size):
	'''Function to plot the word distribution of the topic'''
    tags = topic['word'].values.tolist()
    height = topic['prob'].values.tolist()
    y_pos = np.arange(len(tags))

    fig, ax = plt.subplots(figsize=(5,5))
    ax.barh(y_pos, height, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tags)
    ax.invert_yaxis()
    ax.set_title('Model size: '+str(size))
    plt.show()

def draw_topic(i,model,size=None,no_top_words=20):
	'''Draws the ith topic of the model.'''
    topic = model.components_[i]
    size = sum(topic) if size is None else size
    topic = topic/sum(topic)
    topic = pd.DataFrame(zip([feature_names[i] for i in range(len(topic))],topic.tolist()),columns=['word','prob']).sort_values(by='prob',ascending=False)
    topic = topic[topic['prob']>=topic['prob'].max()*0]
    if len(topic) > no_top_words:
        topic = topic.iloc[:no_top_words]
    bar(topic,size)

#Load the topics ################################################

no_topics = 50
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

#Draw all topics ################################################

sizes = np.array([sum(topic) for topic in model.components_])
for i in sizes.argsort()[::-1]:
	draw_topic(i,model,no_top_words=no_top_words)


#Draw one topic #################################################

i = 0 
draw_topic(i,model)
