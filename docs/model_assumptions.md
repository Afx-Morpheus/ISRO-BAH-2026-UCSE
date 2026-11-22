# UCSE prototype: data and model assumptions

## What this prototype demonstrates
- A city-zone view of heat and vulnerability indicators.
- Transparent physics-informed explanations for intervention mechanisms.
- Three objective profiles: Budget-Optimized, Cooling-Optimized and Balanced.
- A budget-constrained intervention portfolio and an exportable illustrative report.

## Data status
The bundled Chennai zones and all numerical values are **synthetic demonstration data**. They are not downloaded from ISRO, generated from live satellite scenes, census records, or municipal GIS datasets. The map uses OpenStreetMap basemap tiles when an internet connection is available; the plotted zone attributes remain synthetic.

## Optimization status
The optimizer is a transparent weighted-score and greedy budget-allocation baseline. It is not a globally optimal mixed-integer solver, and it does not solve a calibrated urban microclimate model. Cost values, suitability factors, population reach, cooling indices, renewable-energy indices, carbon indices and resilience indices are illustrative assumptions. The system deliberately labels them as indices rather than claiming precise °C reductions or MWh generation.

## Physics-informed rationale
- Trees: shade and evapotranspiration.
- Cool roofs: increased solar reflectance / albedo.
- Solar canopies: shade plus photovoltaic generation.
- Green roofs: vegetation, shading and evapotranspiration, subject to structural/water constraints.
- Reflective pavements: reduced solar absorption, with glare and pedestrian-comfort checks required.
- Permeable surfaces: infiltration and stormwater resilience.
- Blue-green infrastructure: evapotranspiration and water-sensitive urban design.

## Before real deployment
1. Replace demo zones with validated Landsat / Sentinel / other approved Earth-observation products and document acquisition dates, resolution, cloud masking and processing.
2. Derive LST, NDVI, land-cover, albedo and built-up indicators using a reproducible geospatial workflow.
3. Integrate authoritative population, age/health vulnerability, schools, hospitals, roads, land ownership and municipal asset layers with provenance and privacy safeguards.
4. Obtain local bill-of-quantity / tender / lifecycle cost estimates and land/water/structural feasibility constraints.
5. Calibrate intervention response using peer-reviewed studies, local measurements and/or validated urban climate models; report uncertainty intervals.
6. Replace the greedy baseline with a constrained multi-objective method (e.g. Pareto optimization or MILP) and validate against expert-reviewed plans.
7. Field-check recommendations and make the decision rationale auditable.

## Important limitation
This is a hackathon concept prototype for demonstration and discussion. It must not be used as a basis for actual public spending, engineering design, health-risk decisions or climate-performance guarantees.
