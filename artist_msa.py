import pandas as pd,geopandas as gpd
from shapely.geometry import Point

a2w = pd.read_csv("processed_data/artist2wiki.tsv",encoding='utf-8',delimiter='\t')
origin = pd.read_csv('processed_data/artist_origin.tsv',encoding='utf-8',delimiter='\t')

msa = gpd.read_file("SHP/cb_2016_us_cbsa_500k.shp")
msa['DUSA_ID'] = ['31000US'+i for i in msa['GEOID'].astype(str)]
ctr = gpd.read_file("SHP/SDE_DATA_INT_F7STATES_2004_COUNTRIES_BUFFER2.shp")

out = []
for pname,lat,lon in origin[['Place Wiki Title','lat','lon']].drop_duplicates().values:
    point = Point(lon, lat)
    country = 'NULL'
    city = 'NULL'
    for index,row in ctr.iterrows():
        polygon = row['geometry']
        if polygon.contains(point):
            country = row['NA2']
            break
    if country =='US':
        for index,row in msa.iterrows():
            polygon = row['geometry']
            if polygon.contains(point):
                city = row['NAME']
                break
    out.append(( pname,country,city))
out = pd.DataFrame(out,columns=['Place Wiki Title','ccode2','MSA'])

origin = pd.merge(origin,out,how='left').fillna('NULL').rename(columns={'MSA':'NAME'})
origin = pd.merge(origin,msa[['NAME','GEOID','DUSA_ID']],how='left').fillna('NULL')
oritin = origin[[u'Primary Artist',u'Primary Artist ID',u'Wiki Title',u'tag',u'Place Wiki Title',u'ccode2',u'NAME',u'GEOID',u'DUSA_ID']].rename(columns={'NAME':'msaName','GEOID':'msaId','DUSA_ID':'msaDusaId'})

origin.to_csv('processed_data/artist_origin_msa.csv',encoding='utf-8',index=False)
