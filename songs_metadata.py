from collections import defaultdict
import json,requests,pandas as pd
song_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[2])
song_ids = list(song_ids)[:10]

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
		#data_out['tracking_data'] = {val['key']:val['value'] for val in data_out['tracking_data']}
		#data_out['primary_artist'] = data_out['primary_artist']['api_path']
		#data_out['producer_artists'] = [a['api_path'] for a in data_out['producer_artists']]
		#data_out['writer_artists'] = [a['api_path'] for a in data_out['writer_artists']]
		#data_out['album'] = { key:data_out['album'][key] for key in ['release_date','api_path','url','name','artist']}
		#data_out['album']['artist'] = data_out['album']['artist']['api_path']
		#data_out['description'] = data_out['description']['dom']['children']
		outfile.write( (json.dumps(data_out)+'\n').encode('utf-8'))
	except:
		g.write(song_id+'\n')
outfile.close()
g.close()