import pandas as pd
from functions import *
song_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[2])

outfile = open('songs_annotations.tsv',mode='w')
g = open('songs_annotations_log_file.tsv',mode='w')
for song_id in song_ids:
    try:
        song_url = song_id2url(song_id)
        annotation_ids = song_annotations(song_url)
        for annotation_id in annotation_ids:
            outfile.write((song_url+'\t'+song_id+'\t'+annotation_id+'\n').encode('utf-8'))
    except:
        g.write(song_id+'\n')
g.close()
outfile.close()