import requests
import re
import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict

def metadata(api_id,fields=None,show_url=False):
	'''Gets the song's metadata or the artist's metadata, depending on the provided id. '''	
	url = 'https://genius.com/api'+api_id
	if show_url:
		print(url)
	r = requests.get(url)
	data = r.json()['response'][api_id.split('/')[1][:-1]]
	if fields is None:
		return data
	else:
		data = defaultdict(lambda:'NULL',data)
		data_out = {key:data[key] for key in fields}
		return data_out

def artist_songs(artist_id,show_url=False):
	'''Gets all the song ids, sorted by popularity'''
	song_ids = []
	next_page = 0
	base_url = 'https://genius.com/api'+artist_id+'/songs?sort=popularity&per_page=50'
	while next_page is not None:
		url = base_url+'&page='+str(next_page) if next_page!=0 else base_url
		if show_url:
			print url
		r = requests.get(url)
		song_ids += [song['api_path'] for song in r.json()['response']['songs']]
		next_page = r.json()['response']['next_page']
	return song_ids

def artists_all(show_url=False):
	'''Crawls the site for all the artists' urls'''
	artists_out = []
	letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0']
	for lett in letters:
		url = 'https://genius.com/artists-index/'+lett
		if show_url:
			print url
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		artists = soup.find_all(name='a',attrs={'class':"artists_index_list-artist_name"})+soup.find_all(name='ul',attrs={'class':"artists_index_list"})[1].find_all(name='a')
		artists_out += [link['href'] for link in artists]
	return artists_out

def top100(show_url=False):
	song_ids = []
	next_page=0
	base_url = 'https://genius.com/api/songs/chart?per_page=50&time_period=all_time'
	while next_page is not None:
		url = base_url+'&page='+str(next_page) if next_page!=0 else base_url
		if show_url:
			print url
		r = requests.get(url)
		next_page = r.json()['response']['next_page']
		song_ids += [song['item']['api_path'] for song in r.json()['response']['chart_items']]
	return song_ids



def parse_content(content):
	annot = []
	for a in content:
		note = []
		if a != '':
			if (a['tag'] in set(['blockquote','p']))|(a['tag'] == 'a'):
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
															print 'Warning: Depth exceeded for content:',content
			if a['tag']=='blockquote':
				annot.append('"'+' '.join(note).strip()+'"')
			else:
				annot.append(' '.join(note).strip())
	annot = '\n'.join(annot).strip()
	annot = annot.replace(' ,',',').replace(' .','.').replace(' ;',';').replace(' :',':')
	annot = re.sub(r'\n+','\n',annot)
	annot = re.sub(r' +',' ',annot)
	return annot


def available_songsmetadata():
	'''Finds all the files of the form songs_metadata*.json 
	and reads all the song_ids found in them'''
	songs = set([])
	available_files = [fname for fname in os.listdir('.') if (fname[:14]=='songs_metadata')&(fname.split('.')[-1]=='json')]
	for fname in available_files:
		with open(fname) as f:
			for line in f:
				try:
					data = json.loads(line)
					songs.add(data['api_path'])
				except:
					pass
	return songs,len(available_files)

def available_artistsmetadata():
	'''Finds all the files of the form artists_metadata*.json 
	and reads all the artists_ids found in them'''
	artist = set([])
	available_files = [fname for fname in os.listdir('.') if (fname[:16]=='artists_metadata')&(fname.split('.')[-1]=='json')]
	for fname in available_files:
		with open(fname) as f:
			for line in f:
				try:
					data = json.loads(line)
					artist.add(data['api_path'])
				except:
					pass
	return artist,len(available_files)

def annotation_content(annotation_id):
	'''Given the annotation ID, returns a single string with the annotation content'''
	annotation_url = 'https://genius.com/api'+str(annotation_id)
	r = requests.get(annotation_url)
	annot = parse_content(r.json()['response']['annotation']['body']['dom']['children'])
	return annot

def genius_url2id(url):
	'''Given the url, returns the ID (works for songs and artists'''
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	artist_id = soup.find_all(name='meta',attrs={'name':'newrelic-resource-path'})[0]['content']
	return artist_id

def song_id2url(song_id):
	'''Given the song ID, returns the song url'''
	song_url = 'https://genius.com/api'+song_id
	r = requests.get(song_url)
	page_url = "http://genius.com" + r.json()["response"]["song"]["path"]
	return page_url


def song_annotations(song_url):
	'''Given the song url, returns a list with all the annotation IDs.'''
	page = requests.get(song_url)
	html = BeautifulSoup(page.text, "html.parser")
	annotation_ids = [ '/annotations/'+str(link['data-id']) for link in html.find_all(name='a',attrs={'class':"referent",'classification':"accepted"})]
	return annotation_ids


def song_lyrics(song_url):
	'''Given the song url, returns the lyrics.'''
	page = requests.get(song_url)
	html = BeautifulSoup(page.text, "html.parser")
	lyrics  = html.find_all(name='div',attrs={'class':'lyrics'})[0].text.strip()
	return lyrics

if __name__ == '__main__':
	page_url = 'https://genius.com/Billy-joel-we-didnt-start-the-fire-lyrics'
	print page_url
	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
	for i,a in annotations:
		print i
		print a
		print '--------'

	song_id = '/songs/347866'
	page_url = song_id2url(song_id)
	print page_url
	annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
	for i,a in annotations:
		print i
		print a
		print '--------'