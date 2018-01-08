import pandas as pd,numpy as np,shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

msa = shapefile.Reader("MSA/cb_2016_us_cbsa_500k.shp")
msa_shapes = msa.shapes()
origin = pd.read_csv('processed_data/artist_origin.tsv',encoding='utf-8',delimiter='\t')

def sort_poly(poly):
    poly = np.array(poly)
    center = poly.transpose()
    center = np.mean(center[0]),np.mean(center[1])
    poly_center = [(point-center) for point in poly]
    angles = [np.arctan(y/x) for x,y in poly_center]
    I = np.argsort(angles)
    return [poly[i] for i in I]

out = []
for pname,lat,lon in origin[['Place Wiki Title','lat','lon']].drop_duplicates().values:
    point = Point(lat, lon)
    found = False
    for i,shape in enumerate(msa_shapes):
        poly = [(lat,lon) for lon,lat in shape.points]
        polygon = Polygon(poly)
        if polygon.contains(point):
            found = True
            break
        if not found:
            poly = sort_poly(poly)
            polygon = Polygon(poly)
            if polygon.contains(point):
                found = True
                break
    if found:
        r = msa.record(i)
        msa_name = r[4]
        msa_id = r[2]
        dusa_id = '31000US'+msa_id.split('US')[-1]
        out.append((pname,msa_name,msa_id,dusa_id))
    else:
        out.append((pname,'NULL','NULL','NULL'))
out = pd.DataFrame(out,columns=['Place Wiki Title','msa_name','msa_id','dusa_id'])
out = pd.merge(origin,out,how='left').fillna('NULL')[['Primary Artist','Primary Artist ID','Wiki Title','tag','Place Wiki Title','msa_name','msa_id','dusa_id']]

out.to_csv('processed_data/artist_origin_msa.csv',encoding='utf-8',index=False)