import codecs,json,pandas as pd

out = []
lines = []

f = codecs.open('songs_metadata.json',encoding='utf-8')
lines += f.read().split('\n')
f.close()
f = codecs.open('songs_metadata2.json',encoding='utf-8')
lines += f.read().split('\n')
f.close()

for line in lines:
	if line.strip() != '':
		song = json.loads(line)
		song_id = None
		release = song['release_date']
		for i in song['tracking_data']:
			if i['key'] == 'Song ID':
				song_id = i['value']
				break
		if (song_id is not None)&(release is not None):
			out.append((song_id,release))
out = pd.DataFrame(out,columns=['Song ID','release_date'])
out.to_csv('processed_data/release_date.csv',index=False,encoding='utf-8')