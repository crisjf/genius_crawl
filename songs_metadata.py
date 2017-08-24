import json,pandas as pd
from functions import metadata,available_songsmetadata
song_ids = pd.read_csv('songs.tsv',delimiter='\t',header=None)
song_ids = set(song_ids[song_ids.columns[2]])

# fields = ['tracking_data','release_date_components','release_date','stats','annotation_count','comment_count','title',
# 		  'spotify_uuid','url','recording_location','primary_artist','featured_artists','producer_artists',
# 		  'writer_artists','album','primary_tag','tags','description','instrumental','api_path','is_music']

# songs,nfiles = available_songsmetadata()
# song_ids = song_ids.difference(songs)

nfiles = 0
outfile = open('songs_metadata_all.json',mode='w') if nfiles==0 else open('songs_metadata'+str(nfiles+1)+'.json',mode='w')
g = open('songs_metadata_all_log_file.tsv',mode='w') if nfiles==0 else open('songs_metadata_log_file'+str(nfiles+1)+'.tsv',mode='w')

# print 'Found a total of',len(songs),'songs already there'
print 'Getting data for',len(song_ids),'songs'
for song_id in song_ids:
	try:
		data_out = metadata(song_id)
		outfile.write((json.dumps(data_out)+'\n').encode('utf-8'))
	except:
		g.write(song_id+'\n')
outfile.close()
g.close()