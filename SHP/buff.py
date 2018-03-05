import geopandas as gpd

for b in [0,1,2,3]:
    ctr = gpd.read_file("SDE_DATA_INT_F7STATES_2004/SDE_DATA_INT_F7STATES_2004.shp")
    print b
    if b!=0:
        ctr['geometry'] = ctr.geometry.buffer(b)
    ctr = ctr[['NA2','geometry']].dissolve(by='NA2').reset_index()
    if b!=0:
        ctr.to_file('SDE_DATA_INT_F7STATES_2004_COUNTRIES_BUFFER'+str(b)+'.shp')
    else:
        ctr.to_file('SDE_DATA_INT_F7STATES_2004_COUNTRIES.shp')