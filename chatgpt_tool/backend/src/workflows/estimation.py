import re
from src.models.schemas import Task, MaterialSpec

RATES = {
    "concrete": {"rate": 150, "daily_output": 50, "unit": "cy"},
    "steel": {"rate": 3000, "daily_output": 5, "unit": "tons"},
    "framing": {"rate": 100, "daily_output": 500, "unit": "lf"},
    "finish": {"rate": 50, "daily_output": 1000, "unit": "sf"},
    "default": {"rate": 100, "daily_output": 1, "unit": "ls"}
}

def enrich_task_with_estimates(task: Task) -> Task:
    """Add cost and duration estimates to a task"""
    desc = task.description.lower()
    
    # Extract quantity
    qty = 10.0
    match = re.search(r'(\d+)', desc)
    if match:
        qty = float(match.group(1))
    
    # Match material type
    mat_type = "default"
    for key in RATES.keys():
        if key in desc:
            mat_type = key
            break
    
    rate_data = RATES[mat_type]
    
    # Calculate duration and costs
    task.duration_days = max(1, int(qty / rate_data["daily_output"]))
    task.material_cost = qty * rate_data["rate"]
    task.labor_cost = task.duration_days * 500
    task.total_cost = task.material_cost + task.labor_cost
    
    task.materials.append(
        MaterialSpec(
            name=mat_type,
            quantity=qty,
            unit=rate_data["unit"],
            unit_cost=rate_data["rate"]
        )
    )
    
    return task