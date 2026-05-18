# Laboratory Exercise 6 - GeoAI: Spatial Prediction Using Parcel-Based Feature Engineering

This laboratory extends the previous exercises from: 
- descriptive GIS analysis 
- overlay analysis 
- spatial statistics 
- raster-vector integration 

into GeoAI-based spatial prediction.

## How to Run

1. Activate virtual environment
2. Install requirements.txt
3. Run `py server/analysis.py`

## Expected Outputs

1. Parcel GeoAI Prediction GeoJSON

## Commit Milestones

### Data Loading Reflection

**1. Why are parcels the prediction unit?**

Parcels are treated as the prediction unit because they serve as the minimum mapping unit. Information from the different criteria is aggregated and stored for each parcel, making parcels the most appropriate spatial unit for both training and prediction.

**2. What spatial processes might roads influence?**

Roads influence accessibility and proximity analysis because they determine how easily a parcel can be reached. Parcels located within a certain distance from roads may have higher accessibility, which can affect land use, development potential, and overall suitability.

**3. Why might tourism affect parcel classification?**

Tourism can affect parcel classification because areas with high tourism potential often experience increased land value, commercial activity, and infrastructure development. These factors may influence how a parcel is classified or prioritized in the analysis.

**4. Is machine learning occuring at this stage?**

No. Machine learning is not yet occurring at this stage. This phase focuses on data preparation and input generation, where the relevant spatial criteria and prediction variables are identified and organized before being used in the GeoAI model.

### Feature Engineering Reflection

**5. Why can geometry not be used directly in ML?**

Raw geometry cannot be used directly in most machine learning models because models cannot inherently interpret spatial shapes and coordinates in their original form. Geometries must first be transformed into numerical features, such as area, perimeter, compactness, distance to roads, or encoded land use categories, so that the model can process and learn from them effectively.

**6. Why are distances meaningful features?**

Distances are meaningful features because they represent the accessibility or spatial relationship of a parcel to important features such as roads, commercial centers, or public facilities. This is one of the key distinctions between spatial modelling and traditional statistical modelling, as spatial models explicitly account for location and proximity effects.

**7, Which feature do you think is most influential?**

At this stage, accessibility appears to be the most influential feature in predicting parcel assessment classification. Parcels that are closer to roads and key services are generally more accessible and economically valuable, which can strongly influence their classification and development potential.

### Model Reflection
**8. What does accuracy mean spatially?**

It refers to how well the model correctly classifies parcels based on their geographic and spatial characteristics. In this exercise, an accuracy of approximately 96.18% means that most parcels in the testing dataset were correctly predicted according to their target classification. This indicates that the selected spatial features—such as distance to roads, water bodies, schools, tourism areas, parcel shape, and land use—are effective predictors of parcel behavior or suitability. Spatial accuracy also reflects how well the model captures real-world spatial patterns and relationships between locations.

**9. Can a model have high accuracy but poor spatial interpretation?**

Yes. A model may achieve high numerical accuracy while still having poor spatial interpretation. For example, the model may correctly classify parcels statistically, but the predictions may appear spatially inconsistent or unrealistic when mapped. This can happen if the model overfits the training data or fails to account for spatial dependence and geographic context. In spatial analysis, it is important not only to evaluate accuracy metrics but also to examine the spatial distribution of predictions to determine whether they make geographic sense.

**10. What features may improve the model?**

The model may be imporved by incorporating additional spatial and socio-economic variables such as:
- Elevation and slope
- Distance to Commercial Centers
- Susceptibility to hazards (Flood, Landslide, Earthquake, etc.)
- Population Density
- Accessibility to Public Transportation
- Neighborhood or surrounding parcel characteristics

Incorporating temporal and environmental variables may also improve the model's ability to capture more complex spatial relationships and increase its predictive performance.

### Spatial Misclassification

To identify which categories were predicted poorly, the following code was implemented:

```bash
error_agg = (
    data.groupby("ASS_CLASSI")["correct_prediction"]
    .value_counts()
    .unstack(fill_value=0)
)
```

The results are shown below:

| ASS_CLASSI | False | True
|:------------:|:-------:|:------:
|A|108|1887
|C|36|129
|GP|0|1
|I|5|10
|R|73|27849
|R4|1|2
|S|5|10

The results indicate that most misclassifications occurred in Agricultural (A) and Residential (R) parcels. Although Residential areas had a relatively high number of incorrect predictions, they also had a very large number of correctly classified parcels, suggesting that the model still performed well overall for this category. Agricultural parcels showed a comparatively higher proportion of errors relative to their total sample size.

Spatially, these misclassifications may occur in transition or mixed-use areas where parcel characteristics overlap between categories. For example, agricultural parcels located near roads, commercial centers, or expanding urban areas may exhibit spatial characteristics similar to residential or commercial parcels. Likewise, residential parcels in peri-urban or rural areas may resemble agricultural parcels in terms of accessibility, size, and surrounding land use.

The errors may also cluster spatially in areas experiencing rapid land conversion, urban expansion, or inconsistent land use patterns. Such areas often contain heterogeneous parcel characteristics that make classification more difficult for the model.

These misclassifications suggest that additional explanatory variables—such as zoning, population density, land value, building density, or temporal land use change—may help improve the spatial interpretation and predictive performance of the model.

### Challenge Exercise

I selected road class proximity and land use diversity as the two additional spatial features to improve the model.

For the road class proximity feature, I first examined the roads dataset and identified the following road classifications:

- BARANGAY ROAD
- CITY ROAD
- EXPRESS WAY (PROPOSED)
- NATIONAL ROAD
- PRIVATE ROAD
- Proposed Bypass Road
- Provincial Road

From these categories, I selected National Roads, Express Ways (Proposed), and Provincial Roads as the major road classes because they function as primary transportation corridors and typically experience higher traffic volumes. These roads are expected to have stronger influence on accessibility, urban development, and parcel valuation.

The feature was implemented by calculating the distance of each parcel centroid to the nearest major road segment using the following code:

```bash
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
```

For land use diversity, I utilized the existing spatial join result between parcels and land use polygons. Since the spatial join used the `intersects` predicate in a one-to-many relationship, a parcel could intersect multiple land use categories. This provided a basis for measuring the diversity of land uses associated with each parcel.

The land use diversity feature was computed by counting the number of unique land use categories intersecting each parcel:

```bash
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
```

To further improve and compare the modelling approach, I also tested the Gradient Boosting Classifier. This algorithm is commonly used in spatial and land cover classification tasks because it incrementally improves prediction performance by combining multiple weak learners into a stronger predictive model.

The model was implemented using the following code:

```bash
# Gradient Boosting
gb_model = GradientBoostingClassifier(
    random_state=42
)

gb_model.fit(X_train, y_train)

gb_pred = gb_model.predict(X_test)

gb_accuracy = accuracy_score(y_test, gb_pred)

print("\nGradient Boosting Accuracy:")
print(gb_accuracy)
```

The resulting accuracy of the Gradient Boosting model was 94.77%, which is slightly lower than the 96.45% accuracy achieved by the improved Random Forest model. Compared to the initial Random Forest accuracy of 96.16% before adding the two new features, the updated Random Forest model showed a slight improvement in predictive performance.

This suggests that the additional spatial features contributed useful information to the model, particularly in capturing accessibility and land use heterogeneity, although the improvement in accuracy was relatively modest.