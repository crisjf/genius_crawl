import requests
import re
from bs4 import BeautifulSoup


def artist_songs(artist_id):
	'''Gets all the song ids, sorted by popularity'''
	song_ids = []
	next_page = 0
	base_url = 'https://genius.com/api'+artist_id+'/songs?sort=popularity'
	while next_page is not None:
		url = base_url+'&page='+str(next_page) if next_page!=0 else base_url
		r = requests.get(url)
		song_ids += [song['api_path'] for song in r.json()['response']['songs']]
		next_page = r.json()['response']['next_page']
	return song_ids

def annotation_content(annotation_id):
	'''Given the annotation ID, returns a single string with the annotation content'''
	annotation_url = 'https://genius.com/api/annotations/'+str(annotation_id)
	r = requests.get(annotation_url)
	annot = []
	for a in r.json()['response']['annotation']['body']['dom']['children']:
		note = []
		if a != '':
			if (a['tag'] == 'p')|(a['tag'] == 'a'):
				for aa in a['children']:
					if not isinstance(aa, dict):
						note.append(aa.strip())
					else:
						if 'children' in aa.keys():
							for aaa in aa['children']:
								if not isinstance(aaa, dict):
									note.append(aaa.strip())
								else:
									if 'children' in aaa.keys():
										for aaaa in aaa['children']:
											if not isinstance(aaaa, dict):
												note.append(aaaa.strip())
											else:
												if 'children' in aaaa.keys():
													for aaaaa in aaaa['children']:
														if not isinstance(aaaaa, dict):
															note.append(aaaaa.strip())
														else:
															print 'Warning: Depth exceeded for annotation:',annotation_id
		annot.append(''.join(note).strip())
	annot = '\n'.join(annot).strip()
	annot = re.sub(r'\n+','\n',annot)
	return annot

def artist_url2id(artist_url):
	'''Given the artist url, returns the artist ID'''
	r = requests.get(artist_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	artist_id = soup.find_all(name='meta',attrs={'name':'newrelic-resource-path'})[0]['content']
	return artist_id

def song_id2url(song_id):
	'''Given the song ID, returns the song url'''
	song_url = 'https://genius.com/api/songs/'+str(song_id) 
	r = requests.get(song_url)
	page_url = "http://genius.com" + r.json()["response"]["song"]["path"]
	return page_url


def song_annotations(song_url):
	'''Given the song url, returns a list with all the annotation IDs.'''
	page = requests.get(song_url)
	html = BeautifulSoup(page.text, "html.parser")
	annotation_ids = [link['data-id'] for link in html.find_all(name='a',attrs={'class':"referent",'classification':"accepted"})]
	return annotation_ids


if __name__ == '__main__':
	page_url = 'https://genius.com/Billy-joel-we-didnt-start-the-fire-lyrics'
	print page_url
	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
	for i,a in annotations:
		print i
		print a
		print '--------'

	song_id = 347866
	page_url = song_id2url(song_id)
	print page_url
	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
	for i,a in annotations:
		print i
		print a
		print '--------'