import re,nltk

def removeURL(doc_):
    doc = doc_[:]
    for url in re.findall(r'https*://[^ ,\n]*',doc):
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
    docs = [removeURL(annot).strip() for annot in docs]
    docs = [annot for annot in docs if annot != '']
    return docs

def word_tokenize(doc):
    '''Uses the nltk tokenizer, but it also fixes typos, slangs, saves U.S., and splits words joined by /'''
    tokens = []
    for t in nltk.word_tokenize(doc):
        if '/' in t[1:-1]:
            out = t.split('/')
            while '' in out:
                out.remove('')
        elif t.lower() == 'hes':
            out = [t[0]+'e','is']
        elif t.lower() == 'shes':
            out = [t[0]+'he','is']
        elif t.lower() == 'im':
            out = ['I','am']
        elif t.lower() == 'i\'mma':
            out = ['I','am','going','to']
        elif t != '':
            out = [t]
        else:
            out = []
        tokens += out
    return tokens

def lemm(w,t,lemmatizer):
    chars = set('\'".,;:()[]/{}?~!@#$%^&*()_+`=1234567890-|\<>*')
    if w.lower() in set(['texting','texts','text','texted']):
        lemma = 'text'
    elif w.lower() in set(['googled','googles','google','googling']):
        lemma = 'google'
    elif w.lower() in set(['tweet','tweets','tweeted','tweeting']):
        lemma = 'tweet'
    elif t[0].lower()=='v':
        lemma = lemmatizer.lemmatize(w,'v')
    else:
        lemma = lemmatizer.lemmatize(w)
    if lemma == 'U.S.':
        return lemma
    else:
        return ''.join([l for l in lemma if l not in chars]).strip()

def bagofwords(doc,lemmatizer):
    '''More sofisticated splitting into bag of words using lemmatization and pos tagging'''
    # doc = removequestions(doc)
    parts = {'n','v','j','r'}
    stoplist = set('for song im be a of the and to in about above across after all along already also although always among an and another are area areas as at b be became because become becomes been before began behind best better between big both but by c came can cannot case cases come could d did do does done down downed downing downs during e each early either end ended ending ends enough even evenly ever every f felt find finds for four from g gave get gets good goods got h had has have having he her here herself him himself his how however i if important in interest interested interesting interests into is it its itself j just k keep keeps kind knew know known knows l large largely last later latest least less let lets like likely long longer longest m made make making may me might more most mostly mr mrs much must my n necessary need needed needing needs no non not now number numbers o of off often on once one only or order ordered ordering orders other others our out over p part parted parting parts per perhaps place places point pointed pointing points possible present presented presenting presents put puts q quite r rather really right room rooms s said same saw say says see seem seemed seeming seems sees several shall she should show showed showing shows side sides since so some still such sure t than that the their them then there therefore these they this those though thought thoughts three through thus to too took toward turn turned turning turns two u under until up upon us use used uses v very w want wanted wanting wants was way ways we well wells went were what when where whether which while who whole whose why will with within without would x y yet you your yours z'.split())|set(['',' '])
    bag = [(w,lemm(w,t,lemmatizer),t) for w,t in nltk.pos_tag(word_tokenize(doc)) if t[0].lower() in parts]
    return [lemma.lower().replace('.','') for w,lemma,t in bag if lemma.lower() not in stoplist]