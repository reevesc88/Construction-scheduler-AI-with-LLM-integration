from src.agent.scheduler_agent import SchedulerAgent
from src.workflows.estimation import enrich_task_with_estimates
from src.models.schemas import Task, ProjectPlan, RiskFactor

class SupervisorAgent:
    def __init__(self):
        self.scheduler = SchedulerAgent()
    
    def run_pipeline(self, context: dict) -> dict:
        """Run full planning pipeline"""
        # 1. Generate initial tasks
        raw_tasks = self.scheduler.create_initial_schedule(context)
        
        # 2. Enrich with costs and durations
        tasks = []
        for t_data in raw_tasks:
            try:
                task = Task(**t_data)
                task = enrich_task_with_estimates(task)
                tasks.append(task)
            except:
                continue
        
        # 3. Create risks (hardcoded for demo)
        risks = [
            RiskFactor(
                risk_type="Weather",
                probability="Medium",
                mitigation_strategy="Monitor weather forecasts and adjust schedules"
            )
        ]
        
        # 4. Aggregate costs and duration
        total_cost = sum(t.total_cost for t in tasks)
        total_duration = sum(t.duration_days for t in tasks)
        critical_path = [t.id for t in tasks]  # Simplified
        
        # 5. Create plan object
        plan = ProjectPlan(
            project_id=context.get("project_id", "Unknown"),
            tasks=tasks,
            risks=risks,
            total_estimated_cost=total_cost,
            total_duration_days=total_duration,
            critical_path=critical_path
        )
        
        return plan.dict()