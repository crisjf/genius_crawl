import pandas as pd
import johnny5 as j5
a2w = pd.read_csv('processed_data/artist2wiki.tsv',delimiter='\t',encoding='utf-8')

def origin(a):
	o = None
	for tag in ['musical artist','musician']:
		if tag in a.infobox().keys():
			if 'origin' in a.infobox()[tag].keys():
				if o is None:
					o = a.infobox()[tag]['origin']
					o = None if o.strip() == '' else o
	if o is not None:
		if '[[' in o:
			o = o[:o.find(']]')].replace('[[','').strip()
		if '|' in o:
			o = o.split('|')[0]
		if '/' in o:
			o = o.split('/')[0]
		fplace = j5.place(o)
		fplace.find_article()
		pname = fplace.title()
		lat,lon = fplace.coords()
		return [pname,str(lat),str(lon)]
	else:
		return ['NULL','NULL','NULL']
	
def residence(a):
	o = None
	if 'person' in a.infobox().keys():
		if 'residence' in a.infobox()['person'].keys():
			if o is None:
				o = a.infobox()['person']['residence']
				o = None if o.strip() == '' else o
	if o is not None:
		if '[[' in o:
			o = o[:o.find(']]')].replace('[[','').strip()
		if '|' in o:
			o = o.split('|')[0]
		if '/' in o:
			o = o.split('/')[0]
		fplace = j5.place(o)
		fplace.find_article()
		pname = fplace.title()
		lat,lon = fplace.coords()
		return [pname,str(lat),str(lon)]
	else:
		return ['NULL','NULL','NULL']
	
def wd_location(a,prop):
	if a.wd_prop(prop)[0]['id'] !='NA':
		p = j5.place(a.wd_prop(prop)[0]['id'])
		p.find_article()
		pname = p.title()
		lat,lon = p.coords()
		return [pname,str(lat),str(lon)]
	else:
		return ['NULL','NULL','NULL']
	
def formation(a):
	return wd_location(a,'P740')

def work_location(a):
	return wd_location(a,'P937')

def birth_place(a):
	return wd_location(a,'P19')

f = open('processed_data/artist_origin.tsv',mode='w')
f.write('Primary Artist\tPrimary Artist ID\tWiki Title\ttag\tPlace Wiki Title\tlat\tlon\n')
for artist,artist_id,artist_wiki in a2w[['Primary Artist','Primary Artist ID','Wiki Title']].dropna().values:
	out = [artist,str(int(artist_id)),artist_wiki]
	a = j5.article(artist_wiki)
	for tag,func in [('formation',formation),('work_location',work_location),('birth_place',birth_place),('residence',residence),('origin',origin)]:
		p = func(a)
		if p[0] != 'NULL':
			f.write(('\t'.join(out+[tag]+p)+'\n').encode('utf-8'))
f.close()


