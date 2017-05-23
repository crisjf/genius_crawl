from collections import defaultdict
import json,requests,pandas as pd
song_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[2])

fields = ['tracking_data','release_date_components','release_date','stats','annotation_count','comment_count','title',
          'spotify_uuid','url','recording_location','primary_artist','featured_artists','producer_artists',
          'writer_artists','album','primary_tag','tags','description','instrumental','api_path','is_music']
outfile = open('songs_metadata.json',mode='w')
g = open('songs_metadata_log_file.tsv',mode='w')
for song_id in song_ids:
	try:
		url = 'https://genius.com/api'+song_id
		r = requests.get(url)
		data = defaultdict(lambda:'NULL',r.json()['response']['song'])
		data_out = {key:data[key] for key in fields}
		outfile.write( (json.dumps(data_out)+'\n').encode('utf-8'))
	except:
		g.write(song_id+'\n')
outfile.close()
g.close()