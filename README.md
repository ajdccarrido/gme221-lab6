# Laboratory Exercise 6 - GeoAI: Spatial Prediction Using Parcel-Based Feature Engineering

## Overview

## Expected Outputs

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