# genius_crawl
Crawler for genius

get_songs.py
Retrieves a list of all the songs from genius and saves it to songs.tsv as:
artist_url	artist_id	song_id

songs_metadata.py
Retrieves the metadata for all the songs in songs.tsv and saves it to songs_metadata.json.
If a songs_metadata.json file already exists, it will ommit the songs in it and save the new songs to songs_metadata1.json.

artists_metadata.py
Retrieves the metadata for all the artists in songs.tsv and saves it to artists_metadata.json.
If a artists_metadata.json file already exists, it will ommit the artists in it and save the new artists to artists_metadata1.json.

annotations.py
Retrieves all the annotation ids for all the songs in songs.tsv and saves it to songs_annotations.tsv as:
song_url	song_id	annotation_id

annotations_content.py
Retrieves the content for all the annotations in songs_annotations.tsv and saves it as independent .tsv files (one for each song, with the song_id as the file name) in annotations/.
Each file has the format:
annotation_id	annotation_content