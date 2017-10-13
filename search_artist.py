import johnny5 as j5,pandas as pd

data = pd.read_csv('processed_data/data_song_annotation_merged_20170815_cleaned_classified.csv',encoding='utf-8')
data = data[data['prob']>0.5]

f = open('processed_data/artist2wiki.tsv',mode='w')
f.write('Primary Artist\tPrimary Artist ID\tWiki Title\twdid\tL\tinstance_of\n')
for artist,artist_id in data[['Primary Artist','Primary Artist ID']].drop_duplicates().values[:20]:
    out = [artist,str(artist_id)]
    try:
        a = j5.article(artist,slow_connection=True)
        a.find_article()
        if a.title() is None:
            a = j5.search(artist)
            out += [a.title(),a.wdid(),str(a.L()),j5.article(a.wd_prop('P31')[0]['id']).title()]
        else:
            out += [a.title(),a.wdid(),str(a.L()),j5.article(a.wd_prop('P31')[0]['id']).title()]
    except:
        out += ['NULL','NULL','NULL','NULL']
    out = [(val if val is not None else 'NULL') for val in out ]
    f.write(('\t'.join(out)+'\n').encode('utf-8'))
f.close()