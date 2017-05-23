from collections import defaultdict
import json,requests,pandas as pd
artist_ids = set(pd.read_csv('songs.tsv',delimiter='\t',header=None)[1])

artist_ids = list(artist_ids)[:10]
outfile = open('artists_metadata.json',mode='w')
for artist_id in artist_ids:
    url = 'https://genius.com/api'+artist_id
    #print url
    r = requests.get(url)
    data = defaultdict(lambda:'NULL',r.json()['response']['artist'])
    fields = ['followers_count','alternate_names','name','url','api_path','twitter_name']
    data_out = {key:data[key] for key in fields}
    outfile.write( (json.dumps(data_out)+'\n').encode('utf-8'))
outfile.close()