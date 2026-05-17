import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score 

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
# print( 
#     parcels_landuse[["Name", "landuse_code"]] 
#     .drop_duplicates() 
#     .sort_values("landuse_code") 
# ) 

# Encode target variable (land use class)
parcels_landuse["target_code"] = (
    parcels_landuse["ASS_CLASSI"]
    .astype("category")
    .cat.codes
)

# Defining Feature Matrix
features = [
    "area",
    "perimeter",
    "compactness",
    "dist_to_road",
    "dist_to_water",
    "dist_to_school",
    "dist_to_tourism",
    "landuse_code"
]

# Prepare dataset
data = parcels_landuse.dropna(
    subset = features + ["target_code"]
)

X = data[features]
y = data["target_code"]

X_train, X_test, y_train, y_test = train_test_split( 
    X, 
    y, 
    test_size=0.30, 
    random_state=42 
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Generate predictions
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)

data["predicted_class"] = model.predict(X)

categories = ( 
    data["ASS_CLASSI"] 
    .astype("category") 
    .cat.categories
) 

data["predicted_label"] = data["predicted_class"].apply( 
    lambda code: categories[code] 
)

data["correct_prediction"] = (
    data["ASS_CLASSI"] ==
    data["predicted_label"]
)

print(data[["ASS_CLASSI", "predicted_label", "correct_prediction"]].head())

error_agg = (
    data.groupby("ASS_CLASSI")["correct_prediction"]
    .value_counts()
    .unstack(fill_value=0)
)

print(error_agg)