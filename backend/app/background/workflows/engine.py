from typing import Dict, Any, List, Callable
import logging

logger = logging.getLogger(__name__)

class WorkflowStep:
    def __init__(self, name: str, action: Callable, compensation: Callable = None):
        self.name = name
        self.action = action
        self.compensation = compensation

class WorkflowPipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[WorkflowStep] = []
        
    def add_step(self, name: str, action: Callable, compensation: Callable = None):
        self.steps.append(WorkflowStep(name, action, compensation))
        return self

class WorkflowEngine:
    """
    Executes a multi-step background workflow pipeline.
    Implements the Saga pattern: if a step fails, it runs compensation for previous steps.
    """
    _workflows: Dict[str, WorkflowPipeline] = {}
    
    @classmethod
    def register(cls, pipeline: WorkflowPipeline):
        cls._workflows[pipeline.name] = pipeline
        
    @classmethod
    def execute(cls, pipeline_name: str, payload: Any):
        pipeline = cls._workflows.get(pipeline_name)
        if not pipeline:
            logger.error(f"No workflow found for {pipeline_name}")
            return
            
        completed_steps = []
        logger.info(f"Starting workflow {pipeline_name}")
        
        for step in pipeline.steps:
            try:
                logger.info(f"Executing step {step.name}")
                # Execute the step, usually enqueueing a Celery BaseJob
                payload = step.action(payload)
                completed_steps.append(step)
            except Exception as e:
                logger.error(f"Workflow {pipeline_name} failed at {step.name}: {e}")
                cls._compensate(completed_steps, payload)
                break
                
    @classmethod
    def _compensate(cls, completed_steps: List[WorkflowStep], payload: Any):
        # Reverse order compensation
        for step in reversed(completed_steps):
            if step.compensation:
                try:
                    logger.info(f"Running compensation for {step.name}")
                    step.compensation(payload)
                except Exception as ce:
                    logger.error(f"Compensation failed for {step.name}: {ce}")

workflow_engine = WorkflowEngine()
