import json,pandas as pd
from functions import metadata,available_songsmetadata
song_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[2])

fields = ['tracking_data','release_date_components','release_date','stats','annotation_count','comment_count','title',
		  'spotify_uuid','url','recording_location','primary_artist','featured_artists','producer_artists',
		  'writer_artists','album','primary_tag','tags','description','instrumental','api_path','is_music']

songs,nfiles = available_songsmetadata()
song_ids = song_ids.difference(songs)

outfile = open('songs_metadata.json',mode='w') if nfiles==0 else open('songs_metadata'+str(nfiles+1)+'.json',mode='w')
g = open('songs_metadata_log_file.tsv',mode='w') if nfiles==0 else open('songs_metadata_log_file'+str(nfiles+1)+'.tsv',mode='w')

for song_id in song_ids:
	try:
		data_out = metadata(song_id,fields)
		outfile.write((json.dumps(data_out)+'\n').encode('utf-8'))
	except:
		g.write(song_id+'\n')
outfile.close()
g.close()