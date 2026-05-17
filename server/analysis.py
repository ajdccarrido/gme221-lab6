import geopandas as gpd

parcels = gpd.read_file("data/parcel.geojson")

# print(parcels.head())
# print(parcels.crs)

roads = gpd.read_file("data/roads.geojson")
water = gpd.read_file("data/water_network.geojson")
landuse = gpd.read_file("data/landuse.geojson")
schools = gpd.read_file("data/schools.geojson")
tourism = gpd.read_file("data/tourism.geojson")

roads = roads.to_crs(parcels.crs)
water = water.to_crs(parcels.crs)
landuse = landuse.to_crs(parcels.crs)
schools = schools.to_crs(parcels.crs)
tourism = tourism.to_crs(parcels.crs)

# Geoemtry-Based Features
parcels["area"] = parcels.geometry.area
parcels["perimeter"] = parcels.geometry.length
parcels["compactness"] = (
    parcels["area"] /
    (parcels["perimeter"] ** 2)
)

# Parcel Centroids
parcels["centroid"] = parcels.geometry.centroid

# Distance to Raods
parcels["dist_to_road"] = parcels["centroid"].apply(
    lambda p: roads.distance(p).min()
)

# Distance to Water Network
parcels["dist_to_water"] = parcels["centroid"].apply( 
    lambda p: water.distance(p).min() 
)

# Distance to Schools
parcels["dist_to_school"] = parcels["centroid"].apply(
    lambda p: schools.distance(p).min()
)

# Distance to Tourism Sites
parcels["dist_to_tourism"] = parcels["centroid"].apply(
    lambda p: tourism.distance(p).min()
)

# Spatial Join with Land Use
parcels_landuse = gpd.sjoin( 
    parcels, 
    landuse[["Name", "geometry"]], 
    how="left", 
    predicate="intersects" 
)

# Encode Land Use Category
parcels_landuse["landuse_code"] = (
    parcels_landuse["Name"]
    .astype("category")
    .cat.codes
)

# print unique land use categories and their codes 
print( 
    parcels_landuse[["Name", "landuse_code"]] 
    .drop_duplicates() 
    .sort_values("landuse_code") 
) 