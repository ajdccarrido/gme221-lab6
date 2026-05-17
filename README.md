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