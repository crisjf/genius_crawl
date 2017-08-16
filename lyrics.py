import pandas as pd
from functions import *
data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned.csv',encoding='utf-8')
print len(data)
g = open('lyrics_log_file.tsv',mode='w')
for i in data['Song ID'].values:
	try:
		f = open('lyrics/'+str(int(i))+'.txt',mode='w')
		song_id = '/songs/'+str(int(i))
		song_url = song_id2url(song_id)
		f.write(song_lyrics(song_url).encode('utf-8'))
		f.close()
	except:
		g.write(str(int(i))+'\n')
g.close()