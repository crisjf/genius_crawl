import pandas as pd,re,nltk
from crisjfpy import list_join
from nltk.stem import WordNetLemmatizer
from collections import Counter,defaultdict
from gensim import corpora, models, similarities
try:
	import cPickle as pickle
except:
	import pickle

num_topics=100

print 'Loading data...'
data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8')
data = data[data['prob']>0.5]

def removeURL(doc_):
    doc = doc_[:]
    for url in re.findall(r'https*://[^ ,\n]*[ ,\n]',doc):
        url = url.strip()
        while url[-1] in set('\'".,;:'):
            url = url[:-1]
        if (url[-1]==')')&(url.count('(')!=url.count(')')):
            url = url[:-1]
        doc = doc.replace(url,'')
    doc = re.sub(r' +',' ',doc)
    for c1 in set('.,;:'):
        doc = doc.replace(' '+c1,c1)
    for c1 in set('.,;:'):
        for c2 in set('\'".,;:'):
            doc = doc.replace(c1+c2,c2)
    return doc

def split_annotations(doc):
    '''Splits the annotations'''
    docs = doc[2:-2].replace('|','\n')
    docs = docs.split("', '")
    docs = [removeURL(annot) for annot in docs]
    return docs

documents = data[data['prob']>0.5]['annotations'].values.tolist()
documents = list_join([split_annotations(doc) for doc in documents])
print 'Number of documents:',len(documents)

lemmatizer = WordNetLemmatizer()
def lemm(w,t,lemmatizer):
    chars = set('\'".,;:()[]/{}?~!@#$%^&*()_+`=1234567890-|\<>*')
    if t[0].lower()=='v':
        lemma = lemmatizer.lemmatize(w,'v')
    else:
        lemma = lemmatizer.lemmatize(w)
    return ''.join([l for l in lemma if l not in chars]).strip()
    
def bagofwords(doc):
    '''More sofisticated splitting into bag of words using lemmatization and pos tagging'''
    parts = {'n','v'}
    stoplist = set('for be a of the and to in a about above across after all along already also although always among an and another are area areas as at b be became because become becomes been before began behind best better between big both but by c came can cannot case cases come could d did do does done down downed downing downs during e each early either end ended ending ends enough even evenly ever every f felt find finds for four from g gave get gets good goods got h had has have having he her here herself him himself his how however i if important in interest interested interesting interests into is it its itself j just k keep keeps kind knew know known knows l large largely last later latest least less let lets like likely long longer longest m made make making may me might more most mostly mr mrs much must my n necessary need needed needing needs no non not now number numbers o of off often on once one only or order ordered ordering orders other others our out over p part parted parting parts per perhaps place places point pointed pointing points possible present presented presenting presents put puts q quite r rather really right room rooms s said same saw say says see seem seemed seeming seems sees several shall she should show showed showing shows side sides since so some still such sure t than that the their them then there therefore these they this those though thought thoughts three through thus to too took toward turn turned turning turns two u under until up upon us use used uses v very w want wanted wanting wants was way ways we well wells went were what when where whether which while who whole whose why will with within without would x y yet you your yours z'.split())
    bag = [(w,lemm(w,t,lemmatizer),t) for w,t in nltk.pos_tag(nltk.word_tokenize(doc)) if t[0].lower() in parts]
    return [lemma.lower() for w,lemma,t in bag if lemma not in stoplist]

print 'Changing to bag of words representation...'
texts = [bagofwords(doc) for doc in documents]

print 'Removing words that occurr only once...'
frequency = defaultdict(int,Counter(list_join(texts)))
texts = [[token for token in text if frequency[token] > 1] for text in texts]

print 'Creating dictionary...'
dictionary = corpora.Dictionary(texts)

print 'Changing the representation of all texts...'
corpus = [dictionary.doc2bow(text) for text in texts]
pickle.dump(corpus, open("processed_data/corpus.p", "wb" ))

print 'Running the model with',num_topics,'topics...'
model_lda = models.LdaModel(corpus, id2word=dictionary, num_topics=num_topics)

pickle.dump(dictionary, open("processed_data/dictionary.p", "wb" ))
pickle.dump(model_lda , open("processed_data/model_lda.p", "wb" ))
