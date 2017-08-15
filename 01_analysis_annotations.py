import os
import pandas as pd
from datetime         import datetime

start = datetime.now()
print ('Sarting at: {0}\n'.format(str(start)))

pwd = os.getcwd()+('/annotations/')
files = os.listdir(pwd)

df = pd.DataFrame(columns = ['song_id','annotation_id','text'])
for file in files[:1000]:
    song_id = file.replace('.tsv','')
    file = open (pwd+files[0],'rb')
    for line in file.readlines():
        line = line.decode().split('\t')
        annotation_id = line[0].replace('/annotations/','')
        annotation_text = line[1].encode('ascii', 'ignore')
        annotation_text = annotation_text.decode().replace('\n','')
        df.loc[len(df)] = [song_id, annotation_id, annotation_text]

finish = datetime.now()
print ('Finished at: {0}\n'.format(str(finish)))
