# main.py

import asyncio

# Import the container configuration first so that all
# dependency bindings are registered.
from app.container import container
from app.logging_config import configure_logging
from app.persistence.model.entity_base import Base
from app.workflow.workflow_runner import WorkFlowRunner


async def main() -> None:
    configure_logging()
    work_flow_runner = container[WorkFlowRunner]
    print(Base.metadata.tables.keys())
    await work_flow_runner.run()


if __name__ == "__main__":
    asyncio.run(main())
