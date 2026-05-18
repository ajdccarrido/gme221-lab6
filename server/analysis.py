import pandas as pd
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
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

# Geometry-Based Features
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

# # Prepare dataset
# data = parcels_landuse.dropna(
#     subset = features + ["target_code"]
# )

# X = data[features]
# y = data["target_code"]

# X_train, X_test, y_train, y_test = train_test_split( 
#     X, 
#     y, 
#     test_size=0.30, 
#     random_state=42 
# )

# model = RandomForestClassifier(
#     n_estimators=100,
#     random_state=42
# )

# model.fit(X_train, y_train)

# # Generate predictions
# y_pred = model.predict(X_test)

# accuracy = accuracy_score(y_test, y_pred)

# print("Accuracy:", accuracy)

# data["predicted_class"] = model.predict(X)

# categories = ( 
#     data["ASS_CLASSI"] 
#     .astype("category") 
#     .cat.categories
# ) 

# data["predicted_label"] = data["predicted_class"].apply( 
#     lambda code: categories[code] 
# )

# data["correct_prediction"] = (
#     data["ASS_CLASSI"] ==
#     data["predicted_label"]
# )

# print(data[["ASS_CLASSI", "predicted_label", "correct_prediction"]].head())

# error_agg = (
#     data.groupby("ASS_CLASSI")["correct_prediction"]
#     .value_counts()
#     .unstack(fill_value=0)
# )

# print(error_agg)

# data = data.drop(
#     columns=["centroid"],
#     errors="ignore"
# )

# export to geojson 
# data.to_file( 
#     "output/parcel_geoai_prediction.geojson", 
#     driver="GeoJSON" 
#     ) 

# print("GeoAI output exported.") 

########################
## Challenge Exercise ##
########################

# According to Road Type, R_CLASS field from roads gdf
# Road Types - BARANGAY ROAD, CITY ROAD, EXPRESS WAY (PROPOSED), NATIONAL ROAD, PRIVATE ROAD, Proposed Bypass Road, Provincial Road
# Define major road classes
major_road_classes = [
    "NATIONAL ROAD",
    "EXPRESS WAY (PROPOSED)",
    "Provincial Road"
]

# Filter major roads
major_roads = roads[
    roads["R_CLASS"].isin(major_road_classes)
].copy()

# Distance to nearest major road
parcels_landuse["dist_to_major_road"] = (
    parcels_landuse["centroid"]
    .apply(lambda p: major_roads.distance(p).min())
)

# According to Land Use Diversity
# Count unique land use categories per parcel
landuse_diversity = (
    parcels_landuse
    .groupby(parcels_landuse.index)["Name"]
    .nunique()
)

# Assign diversity score
parcels_landuse["landuse_diversity"] = (
    parcels_landuse.index.map(landuse_diversity)
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
    "landuse_code",
    "dist_to_major_road",
    "landuse_diversity"
]


data = parcels_landuse.dropna(
    subset= features + ["target_code"]
)

X = data[features]
y = data["target_code"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)

# Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:")
print(rf_accuracy)

# Gradient Boosting
gb_model = GradientBoostingClassifier(
    random_state=42
)

gb_model.fit(X_train, y_train)

gb_pred = gb_model.predict(X_test)

gb_accuracy = accuracy_score(y_test, gb_pred)

print("\nGradient Boosting Accuracy:")
print(gb_accuracy)

# Model Comparison

print("\nModel Comparison")
print("----------------")
print(f"Random Forest Accuracy: {rf_accuracy:.4f}")
print(f"Gradient Boosting Accuracy: {gb_accuracy:.4f}")

# Extract feature importance for RF model
rf_importance_df = pd.DataFrame({
    "feature": features,
    "importance": rf_model.feature_importances_
})

# Sort descending
rf_importance_df = rf_importance_df.sort_values(
    by="importance",
    ascending=False
)

print("Random Forest Model Feature Importance")
print(rf_importance_df)

# Extract feature importance for XGBoost model
gb_importance_df = pd.DataFrame({
    "feature": features,
    "importance": gb_model.feature_importances_
})

# Sort descending
gb_importance_df = gb_importance_df.sort_values(
    by="importance",
    ascending=False
)

print("Gradient Boost Model Feature Importance")
print(gb_importance_df)