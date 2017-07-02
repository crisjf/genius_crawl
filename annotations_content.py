import pandas as pd
from functions import *

songs = pd.read_csv('songs_annotations.tsv',delimiter='\t',header=None,encoding='utf-8')
songs.columns=['song_url','song_id','annotation_id']
songs = songs[['song_id','annotation_id']].drop_duplicates()
songs = pd.DataFrame(songs.groupby('song_id')['annotation_id'].apply(list))

g = open('annotations_content_log_file.tsv',mode='w')
for song_id,row in songs.iterrows():
    try:
        annotations = row['annotation_id']
        f = open('annotations/'+song_id.split('/')[-1]+'.tsv',mode='w')
        for annotation_id in annotations:
            annotation = annotation_content(annotation_id).replace('\t',' ').replace('\n','|')
            f.write((annotation_id+'\t'+annotation+'\n').encode('utf-8'))
        f.close()
    except:
        g.write(song_id+'\n')
g.close()