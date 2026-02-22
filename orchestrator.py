import asyncio
import logging
import time
from typing import Protocol, TypeVar, List, Dict, Any
from dataclasses import dataclass, field
from abc import abstractmethod

# Configure enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("WorkflowOrchestrator")

T = TypeVar('T')

@dataclass
class ExecutionContext:
    """Context object passed through the execution pipeline."""
    workflow_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class TaskPlugin(Protocol):
    """Protocol defining the strict interface for executable plugins."""
    @property
    def name(self) -> str: ...
    
    @abstractmethod
    async def execute(self, context: ExecutionContext) -> Any: ...

class BaseTask:
    """Abstract base implementation with shared utility methods."""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

class DataIngestionTask(BaseTask):
    """Concrete task simulating async data extraction."""
    async def execute(self, context: ExecutionContext) -> Any:
        logger.info(f"[{context.workflow_id}] Starting ingestion pipeline...")
        await asyncio.sleep(0.5)  # Simulate network I/O
        return {"status": "ingested", "records": 1024, "source": "API_V2"}

class DataTransformationTask(BaseTask):
    """Concrete task simulating CPU-bound data transformation."""
    async def execute(self, context: ExecutionContext) -> Any:
        logger.info(f"[{context.workflow_id}] Applying transformation matrix...")
        await asyncio.sleep(0.3)  # Simulate CPU-bound work
        return {"status": "transformed", "integrity_check": "passed"}

class WorkflowEngine:
    """Core engine responsible for dynamic task orchestration and error handling."""
    def __init__(self):
        self._registry: List[TaskPlugin] = []

    def register_task(self, task: TaskPlugin) -> None:
        """Registers a new plugin strictly matching the TaskPlugin Protocol."""
        self._registry.append(task)
        logger.debug(f"Registered task: {task.name}")

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        context = ExecutionContext(workflow_id=workflow_id)
        logger.info(f"Initializing workflow: {workflow_id}")
        
        results = {}
        for task in self._registry:
            try:
                res = await task.execute(context)
                results[task.name] = res
            except Exception as e:
                logger.error(f"Task {task.name} failed: {e}", exc_info=True)
                results[task.name] = {"error": str(e)}
                # In a real enterprise system, we might implement retry logic here
                break 
                
        duration = time.time() - context.timestamp
        logger.info(f"Workflow {workflow_id} completed. Total duration: {duration:.2f}s")
        return results

if __name__ == "__main__":
    # Dependency Injection: Assembling the engine with concrete implementations
    engine = WorkflowEngine()
    engine.register_task(DataIngestionTask("IngestionTask_v1"))
    engine.register_task(DataTransformationTask("TransformationTask_v2"))
    
    # Execute the asynchronous pipeline
    final_state = asyncio.run(engine.execute_workflow("WF-9001-ALPHA"))
    print(f"\nFinal State Export:\n{final_state}")
