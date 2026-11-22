from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .optimizer import optimize, compare_scenarios

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "data" / "zones.json").open(encoding="utf-8") as f:
    ZONES = json.load(f)

app = FastAPI(title="UCSE | Urban Cooling Strategy Engine", version="1.0.0", description="Illustrative urban cooling decision-support prototype")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

class OptimizeRequest(BaseModel):
    budget_crore: float = Field(default=150, gt=0, le=100000)
    mode: str = Field(default="balanced")

@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(ROOT / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"status":"ok","service":"UCSE","timestamp":datetime.now(timezone.utc).isoformat(),"data_mode":"synthetic_demo"}

@app.get("/api/zones")
def zones():
    return {"city":"Chennai","data_mode":"synthetic_demo","zones":ZONES,
            "note":"Demonstration values only. Replace with validated satellite and census/GIS layers for real deployment."}

@app.post("/api/optimize")
def run_optimizer(req: OptimizeRequest):
    try:
        return optimize(ZONES, req.budget_crore, req.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/scenarios")
def scenarios(req: OptimizeRequest):
    try:
        return {"budget_crore":req.budget_crore,"scenarios":compare_scenarios(ZONES,req.budget_crore)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/report", response_class=PlainTextResponse)
def report(req: OptimizeRequest):
    try:
        result=optimize(ZONES,req.budget_crore,req.mode)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    s=result["summary"]
    lines=["URBAN COOLING STRATEGY ENGINE (UCSE)","ILLUSTRATIVE PLANNING REPORT",f"Generated: {datetime.now().astimezone().isoformat()}","City: Chennai (synthetic demonstration dataset)",f"Scenario: {req.mode.title()}",f"Planning budget: INR {req.budget_crore:.2f} crore",f"Allocated: INR {result['allocated_crore']:.2f} crore",f"Unallocated: INR {result['remaining_crore']:.2f} crore","", "PORTFOLIO"]
    for p in result["portfolio"]:
        lines.append(f"- {p['zone']}: {p['intervention']} | INR {p['cost_crore']:.2f} crore | {p['why']}")
    lines += ["","INDICATIVE SUMMARY",f"Interventions: {s['interventions']}",f"Zones covered: {s['zones_covered']}",f"Population reached (modelled): {s['population_reached_millions']} million",f"Cooling index: {s['cooling_index']}",f"Renewable energy index: {s['renewable_energy_index']}",f"Carbon reduction index: {s['carbon_reduction_index']}",f"Resilience index: {s['resilience_index']}","","LIMITATIONS",result["disclaimer"],"Before policy use, validate satellite products, local costs, land ownership, water availability, structural constraints, demographic data and intervention response with domain experts."]
    return "\n".join(lines)
