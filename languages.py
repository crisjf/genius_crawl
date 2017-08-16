import pandas as pd
from langdetect import detect
import re
def to_list(s):
    sp = re.sub(r"', *'",'. ',s[2:-2])
    sp = re.sub(r'http://[^ ]*','',sp)
    sp = re.sub(r' +',' ',sp)
    punctuation = '1234567890.,;:?!-+| /()"|'+"'"
    ss = sp[:]
    for p in punctuation:
        ss = ss.replace(p,'')
    if len(ss)==0:
        return ''
    else:
        return sp

data = pd.read_csv('processed_data/data_song_annotation_merged_20170815.csv',encoding='utf-8').sample(1000)
print len(data)

data['lang'] = 'NULL'
data['is_null'] = True
data['len_annot'] = 0
print len(data[data['lang']=='NULL'])
for index,row in data.iterrows():
    s = to_list(row['annotations'])
    data.loc[index,'len_annot'] = len(s)
    if len(s)!=0:
        try:
            data.loc[index,'lang'] = detect(s)
            data.loc[index,'is_null'] = False
        except:
            pass

print len(data[data['lang']=='NULL'])
data.to_csv('processed_data/data_song_annotation_merged_20170815_withlangs.csv',index=False,encoding='utf-8')