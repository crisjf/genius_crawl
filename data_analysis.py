import os
import json
import pickle
import pandas as pd

def extract_song_id(line):
    line = line.replace('\n','')
    line = line.split('\t')
    return line[1].replace('/songs/','')

def extract_annotation_id(line):
    line = line.replace('\n','')
    line = line.split('\t')
    return line[2].replace('/annotations/','')

# identify list of songs with annotations
songs_annotation_list = open('songs_annotations.tsv', 'r')
songs_annotation_list = songs_annotation_list.readlines()

songs_annotations = [[extract_song_id(song), extract_annotation_id(song)] for song in songs_annotation_list]
songs_annotated = [s[0] for s in songs_annotations]
songs_annotated = list(set(songs_annotated))

print ("generating the dict")
annotations_dic_fast = dict((song, [s[1] for s in songs_annotations if s[0] == song]) for song in songs_annotated)
print("saving to pickle")
pickle.dump(annotations_dic_fast, open( "annotation_songs_dic.p", "wb" ) )
