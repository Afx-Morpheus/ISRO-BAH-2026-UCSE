"""Transparent, illustrative portfolio optimizer for the UCSE prototype.

All values are demo assumptions, not engineering guarantees or measured forecasts.
"""
from __future__ import annotations
from typing import Any

INTERVENTIONS = [
    {"id":"trees", "name":"Urban forestry", "cost":18, "cooling":0.82, "energy":0.02, "carbon":0.78, "resilience":0.76, "feasibility":0.72, "water":"Medium", "why":"Shade and evapotranspiration can reduce surface and near-surface heat."},
    {"id":"cool_roofs", "name":"Cool roofs", "cost":12, "cooling":0.70, "energy":0.72, "carbon":0.52, "resilience":0.55, "feasibility":0.88, "water":"Low", "why":"High-albedo roof coatings reflect more incoming solar radiation and can lower roof heat gain."},
    {"id":"solar_canopies", "name":"Solar canopies", "cost":28, "cooling":0.48, "energy":1.00, "carbon":0.86, "resilience":0.64, "feasibility":0.66, "water":"Low", "why":"Canopies provide shade while photovoltaic panels generate renewable electricity."},
    {"id":"green_roofs", "name":"Green roofs", "cost":24, "cooling":0.74, "energy":0.34, "carbon":0.70, "resilience":0.72, "feasibility":0.55, "water":"High", "why":"Vegetated roofs add shade and evapotranspiration, subject to structural and water constraints."},
    {"id":"reflective_roads", "name":"Reflective pavements", "cost":15, "cooling":0.54, "energy":0.00, "carbon":0.28, "resilience":0.50, "feasibility":0.78, "water":"Low", "why":"Higher pavement reflectance can reduce absorbed solar energy; glare and pedestrian comfort need local checks."},
    {"id":"permeable", "name":"Permeable surfaces", "cost":20, "cooling":0.42, "energy":0.00, "carbon":0.36, "resilience":0.92, "feasibility":0.63, "water":"Medium", "why":"Permeability supports infiltration and stormwater management, improving resilience during intense rainfall."},
    {"id":"blue_green", "name":"Blue-green infrastructure", "cost":26, "cooling":0.68, "energy":0.00, "carbon":0.48, "resilience":0.94, "feasibility":0.48, "water":"High", "why":"Connected vegetation and water-sensitive spaces can support evaporative cooling and flood resilience."},
]

WEIGHTS = {
    "balanced": {"cooling":.30,"energy":.14,"carbon":.14,"resilience":.14,"feasibility":.13,"equity":.15},
    "cooling":  {"cooling":.55,"energy":.06,"carbon":.08,"resilience":.10,"feasibility":.08,"equity":.23},
    "budget":   {"cooling":.22,"energy":.10,"carbon":.10,"resilience":.10,"feasibility":.25,"equity":.33},
}


def _candidate(zone: dict[str, Any], intervention: dict[str, Any], weights: dict[str, float]) -> dict[str, Any]:
    # Zone modifiers are normalized illustrative factors, not calibrated physical models.
    heat = max(.35, min(1.0, (zone["lst_c"] - 31.0) / 10.0))
    need = zone["vulnerability"]
    suitability = zone["suitability"].get(intervention["id"], .65)
    cooling = intervention["cooling"] * heat * suitability
    equity = need * (0.55 + 0.45 * zone["population_millions"] / 1.0)
    score = (
        weights["cooling"] * cooling + weights["energy"] * intervention["energy"] +
        weights["carbon"] * intervention["carbon"] + weights["resilience"] * intervention["resilience"] +
        weights["feasibility"] * intervention["feasibility"] * suitability + weights["equity"] * equity
    )
    return {"zone_id":zone["id"],"zone":zone["name"],"intervention":intervention["name"],
            "intervention_id":intervention["id"],"cost_crore":round(intervention["cost"] * zone["scale"],2),
            "score":round(score,4),"cooling_index":round(cooling,3),"energy_index":intervention["energy"],
            "carbon_index":intervention["carbon"],"resilience_index":intervention["resilience"],
            "feasibility":intervention["feasibility"]*suitability,"water":intervention["water"],
            "why":intervention["why"],"population_millions":zone["population_millions"]}


def optimize(zones: list[dict[str, Any]], budget_crore: float, mode: str = "balanced") -> dict[str, Any]:
    if mode not in WEIGHTS:
        raise ValueError("mode must be balanced, cooling, or budget")
    if budget_crore <= 0:
        raise ValueError("budget must be greater than zero")
    weights = WEIGHTS[mode]
    candidates = [_candidate(z, i, weights) for z in zones for i in INTERVENTIONS]
    # Greedy marginal-value selection with one intervention per zone in this demo.
    candidates.sort(key=lambda x: (x["score"] / max(x["cost_crore"], .01), x["score"]), reverse=True)
    chosen, used, seen_zones = [], 0.0, set()
    for item in candidates:
        if item["zone_id"] in seen_zones:
            continue
        if used + item["cost_crore"] <= budget_crore:
            chosen.append(item); used += item["cost_crore"]; seen_zones.add(item["zone_id"])
    # If budget permits, fill remaining capacity with a second intervention in zones,
    # while avoiding duplicate intervention types in the same zone.
    chosen_keys = {(x["zone_id"], x["intervention_id"]) for x in chosen}
    for item in candidates:
        key=(item["zone_id"],item["intervention_id"])
        if key in chosen_keys: continue
        if used + item["cost_crore"] <= budget_crore:
            chosen.append(item); used += item["cost_crore"]; chosen_keys.add(key)
    total_pop = sum(z["population_millions"] for z in zones)
    benefitted = sum(x["population_millions"] * .32 for x in chosen)
    weighted_cooling = sum(x["cooling_index"] for x in chosen)
    return {
        "mode":mode,"budget_crore":round(budget_crore,2),"allocated_crore":round(used,2),
        "remaining_crore":round(budget_crore-used,2),"portfolio":chosen,
        "summary":{"interventions":len(chosen),"zones_covered":len({x["zone_id"] for x in chosen}),
                   "population_reached_millions":round(min(total_pop,benefitted),2),
                   "cooling_index":round(weighted_cooling,2),
                   "renewable_energy_index":round(sum(x["energy_index"] for x in chosen),2),
                   "carbon_reduction_index":round(sum(x["carbon_index"] for x in chosen),2),
                   "resilience_index":round(sum(x["resilience_index"] for x in chosen),2)},
        "disclaimer":"Illustrative prototype estimates using synthetic demo data and assumed intervention scores; not measured outcomes or engineering forecasts."
    }


def compare_scenarios(zones: list[dict[str, Any]], budget_crore: float) -> list[dict[str, Any]]:
    labels={"budget":"Budget-Optimized","cooling":"Cooling-Optimized","balanced":"Balanced"}
    return [{"label":labels[m], **optimize(zones,budget_crore,m)} for m in ("budget","cooling","balanced")]
