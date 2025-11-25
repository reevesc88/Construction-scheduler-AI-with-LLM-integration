from pydantic import BaseModel, Field
from typing import List, Optional

class MaterialSpec(BaseModel):
    name: str
    quantity: float
    unit: str
    unit_cost: float = 0.0

class Task(BaseModel):
    id: str
    description: str
    phase: str
    duration_days: int = 0
    labor_cost: float = 0.0
    material_cost: float = 0.0
    total_cost: float = 0.0
    dependencies: List[str] = []
    materials: List[MaterialSpec] = []

class RiskFactor(BaseModel):
    risk_type: str
    probability: str
    mitigation_strategy: str

class ProjectPlan(BaseModel):
    project_id: str
    tasks: List[Task]
    risks: List[RiskFactor]
    total_estimated_cost: float
    total_duration_days: int
    critical_path: List[str]