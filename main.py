from functions import artists_all,artist_url2id,artist_songs

f = open('songs.tsv',mode='w')
g = open('log_file.tsv',mode='w')

artists = artists_all()
for a_url in artists:
	try:
		a_id = genius_url2id(a_url)
		songs = artist_songs(a_id)
		for s in songs:
			f.write((a_url+'\t'+a_id+'\t'+s+'\n').encode('utf-8'))
	except:
		g.write(a_url+'\n')
f.close()
g.close()