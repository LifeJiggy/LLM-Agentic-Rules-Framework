# Development Domain - Examples

## Overview

This document provides development examples for LLM/agentic systems.

## Example 1: Agent Implementation

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: List[Any] = []
    
    @abstractmethod
    def execute(self, task: str) -> Dict[str, Any]:
        """Execute the given task."""
        pass
    
    def add_tool(self, tool):
        """Add a tool to the agent."""
        self.tools.append(tool)


class ToolAgent(BaseAgent):
    """Agent that can use tools."""
    
    def execute(self, task: str) -> Dict[str, Any]:
        results = []
        for tool in self.tools:
            result = tool.execute(task)
            results.append(result)
        return {"task": task, "results": results}
```

## Example 2: Configuration Management

```python
import os
from typing import Any, Dict

class Config:
    """Configuration management."""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
    
    def load(self):
        """Load configuration from environment."""
        self._config = {
            "api_key": os.environ.get("API_KEY"),
            "debug": os.environ.get("DEBUG", "false") == "true",
            "max_retries": int(os.environ.get("MAX_RETRIES", "3")),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
```

## Example 3: Logging Setup

```python
import logging
import sys

def setup_logging(level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger(__name__)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
