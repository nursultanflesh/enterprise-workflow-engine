# Enterprise Workflow Engine

A highly extensible, asynchronous workflow orchestration engine built in Python. This system demonstrates advanced architectural patterns suitable for scalable microservices and complex data pipelines.

## 🏗 Core Architectural Concepts
- **Plugin Architecture:** Utilizes Python's `typing.Protocol` for structural subtyping, ensuring all plugins adhere strictly to the execution interface without tight coupling.
- **Dependency Injection:** The orchestrator accepts task instances dynamically, making the system highly modular and easily testable.
- **Asynchronous Execution:** Built on `asyncio` to prevent I/O blocking during long-running tasks.
- **State Management:** Uses immutable `dataclasses` to pass execution context and metadata securely between pipeline stages.

## 🛠 Tech Stack
- Python 3.10+
- `asyncio`
- `typing` (`Protocol`, `TypeVar`)
- `dataclasses`

## 🚀 Execution Example
The engine dynamically runs registered tasks, tracking context and handling exceptions globally to prevent pipeline crashes.

```bash
python orchestrator.py
