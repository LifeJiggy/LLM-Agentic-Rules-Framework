# Core Domain - Examples

## Overview

This document provides real-world examples demonstrating core principles and best practices for LLM/agentic systems. Each example is production-ready and includes complete implementation code.

## Table of Contents

1. [Example 1: Simple Agent Implementation](#example-1-simple-agent-implementation)
2. [Example 2: Tool-Chaining Pattern](#example-2-tool-chaining-pattern)
3. [Example 3: Context Management](#example-3-context-management)
4. [Example 4: Error Handling with Retry](#example-4-error-handling-with-retry)
5. [Example 5: Output Validation](#example-5-output-validation)
6. [Example 6: Multi-Agent Orchestration](#example-6-multi-agent-orchestration)
7. [Example 7: RAG Pipeline](#example-7-rag-pipeline)
8. [Example 8: Memory-Augmented Agent](#example-8-memory-augmented-agent)
9. [Example 9: Streaming Response Handler](#example-9-streaming-response-handler)
10. [Example 10: Cost-Tracked Agent](#example-10-cost-tracked-agent)
11. [Example 11: Safety-First Agent](#example-11-safety-first-agent)
12. [Example 12: Evaluation Framework](#example-12-evaluation-framework)

---

## Example 1: Simple Agent Implementation

### Basic Agent Structure

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging
from dataclasses import dataclass, field
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

@dataclass
class AgentMessage:
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResult:
    success: bool
    output: Any
    error: Optional[str] = None
    steps: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Base class for all agents with lifecycle management."""
    
    def __init__(self, name: str, description: str, config: Dict = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.config = config or {}
        self.tools: List[callable] = []
        self.message_history: List[AgentMessage] = []
        self.metrics = {"executions": 0, "successes": 0, "failures": 0}
    
    @abstractmethod
    def execute(self, task: str, context: Optional[Dict] = None) -> AgentResult:
        """Execute the given task."""
        pass
    
    def add_tool(self, tool: callable):
        """Add a tool to the agent."""
        self.tools.append(tool)
        return self
    
    def add_message(self, role: str, content: str):
        """Add message to history."""
        self.message_history.append(AgentMessage(role=role, content=content))
        self._trim_history()
    
    def _trim_history(self, max_messages: int = 50):
        """Trim message history to prevent context overflow."""
        if len(self.message_history) > max_messages:
            self.message_history = self.message_history[-max_messages:]
    
    def get_history(self) -> List[AgentMessage]:
        """Get message history."""
        return self.message_history.copy()
    
    def clear_history(self):
        """Clear message history."""
        self.message_history = []


class SpecializedAgent(BaseAgent):
    """Concrete agent specialized for specific task types."""
    
    def __init__(self, specialty: str, llm_client, **kwargs):
        super().__init__(
            name=f"{specialty}Agent",
            description=f"Handles {specialty} tasks",
            **kwargs
        )
        self.specialty = specialty
        self.llm = llm_client
    
    def can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task."""
        keywords = {
            "code": ["code", "program", "function", "debug", "implement"],
            "analysis": ["analyze", "summarize", "report", "data"],
            "writing": ["write", "draft", "compose", "edit"]
        }
        task_lower = task.lower()
        return any(
            kw in task_lower
            for kw in keywords.get(self.specialty, [])
        )
    
    def execute(self, task: str, context: Optional[Dict] = None) -> AgentResult:
        """Execute task with logging and error handling."""
        self.metrics["executions"] += 1
        self.add_message("user", task)
        
        try:
            prompt = self._build_prompt(task, context)
            response = self.llm.generate(prompt)
            
            self.add_message("assistant", response)
            self.metrics["successes"] += 1
            
            return AgentResult(
                success=True,
                output=response,
                steps=["received_task", "built_prompt", "generated_response"]
            )
            
        except Exception as e:
            self.metrics["failures"] += 1
            logger.error(f"Agent {self.name} failed: {e}")
            return AgentResult(
                success=False,
                output=None,
                error=str(e),
                steps=["received_task", "failed_execution"]
            )
    
    def _build_prompt(self, task: str, context: Optional[Dict]) -> str:
        """Build prompt with context."""
        prompt = f"You are a {self.specialty} specialist.\nTask: {task}\n"
        
        if context:
            prompt += f"\nContext: {context}\n"
        
        if self.message_history:
            prompt += "\nPrevious conversation:\n"
            for msg in self.message_history[-5:]:
                prompt += f"{msg.role}: {msg.content}\n"
        
        return prompt


class AgentOrchestrator:
    """Routes tasks to appropriate specialized agents."""
    
    def __init__(self):
        self.agents: Dict[str, SpecializedAgent] = {}
    
    def register_agent(self, agent: SpecializedAgent):
        """Register an agent by specialty."""
        self.agents[agent.specialty] = agent
    
    def route(self, task: str) -> Optional[SpecializedAgent]:
        """Find the best agent for a task."""
        for agent in self.agents.values():
            if agent.can_handle(task):
                return agent
        return None
    
    def execute(self, task: str, context: Optional[Dict] = None) -> AgentResult:
        """Route and execute task."""
        agent = self.route(task)
        
        if not agent:
            return AgentResult(
                success=False,
                output=None,
                error="No suitable agent found"
            )
        
        logger.info(f"Routing to agent: {agent.name}")
        return agent.execute(task, context)


# Usage
orchestrator = AgentOrchestrator()
orchestrator.register_agent(SpecializedAgent("code", llm_client=openai_client))
orchestrator.register_agent(SpecializedAgent("analysis", llm_client=openai_client))

result = orchestrator.execute("Write a Python function to sort a list")
print(result.output)
```

---

## Example 2: Tool-Chaining Pattern

```python
from typing import List, Dict, Any, Optional
import asyncio
from dataclasses import dataclass

@dataclass
class ToolResult:
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0.0


class Tool:
    """Base tool class."""
    
    def __init__(self, name: str, timeout: int = 30):
        self.name = name
        self.timeout = timeout
    
    async def execute(self, **kwargs) -> ToolResult:
        start = time.time()
        try:
            output = await self._run(**kwargs)
            return ToolResult(
                tool_name=self.name,
                success=True,
                output=output,
                duration_ms=(time.time() - start) * 1000
            )
        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=(time.time() - start) * 1000
            )
    
    async def _run(self, **kwargs) -> Any:
        raise NotImplementedError


class ToolChain:
    """Chain multiple tools together."""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.tools: List[Tool] = []
    
    def add(self, tool: Tool, condition: Optional[callable] = None) -> 'ToolChain':
        """Add a tool with optional condition."""
        self.tools.append({"tool": tool, "condition": condition})
        return self
    
    async def execute(self, input_data: Any) -> List[ToolResult]:
        """Execute all tools in sequence."""
        results = []
        current_data = input_data
        
        for tool_config in self.tools:
            tool = tool_config["tool"]
            condition = tool_config["condition"]
            
            # Check condition
            if condition and not condition(current_data):
                results.append(ToolResult(
                    tool_name=tool.name,
                    success=True,
                    output=current_data,
                    error="Condition not met, skipped"
                ))
                continue
            
            # Execute tool
            result = await tool.execute(input_data=current_data)
            results.append(result)
            
            if not result.success:
                logger.error(f"Tool {tool.name} failed: {result.error}")
                break
            
            current_data = result.output
        
        return results


class FileReader(Tool):
    async def _run(self, filepath: str) -> str:
        with open(filepath) as f:
            return f.read()


class CodeAnalyzer(Tool):
    async def _run(self, code: str) -> Dict:
        return {
            "lines": len(code.split("\n")),
            "functions": code.count("def "),
            "classes": code.count("class ")
        }


class Formatter(Tool):
    async def _run(self, analysis: Dict) -> str:
        return f"Lines: {analysis['lines']}, Functions: {analysis['functions']}"


# Usage
async def main():
    chain = ToolChain("analyze_and_format")
    chain.add(FileReader("main.py"))
    chain.add(CodeAnalyzer())
    chain.add(Formatter())
    
    results = await chain.execute("input_data")
    
    for result in results:
        if result.success:
            print(f"{result.tool_name}: {result.output}")
        else:
            print(f"{result.tool_name} failed: {result.error}")

asyncio.run(main())
```

---

## Example 3: Context Management

```python
import tiktoken
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ContextWindow:
    """Manages conversation context with token awareness."""
    max_tokens: int = 4000
    model: str = "gpt-3.5-turbo"
    messages: List[Dict[str, str]] = field(default_factory=list)
    system_prompt: str = ""
    
    def __post_init__(self):
        self.encoder = tiktoken.encoding_for_model(self.model)
    
    def set_system_prompt(self, prompt: str):
        """Set system prompt."""
        self.system_prompt = prompt
    
    def add_user_message(self, content: str):
        """Add user message and manage context."""
        self.messages.append({"role": "user", "content": content})
        self._trim_to_fit()
    
    def add_assistant_message(self, content: str):
        """Add assistant message."""
        self.messages.append({"role": "assistant", "content": content})
    
    def _trim_to_fit(self):
        """Remove oldest messages until within token limit."""
        while self._total_tokens() > self.max_tokens and len(self.messages) > 1:
            # Find first non-system message to remove
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(i)
                    break
    
    def _total_tokens(self) -> int:
        """Calculate total tokens in context."""
        total = len(self.encoder.encode(self.system_prompt))
        for msg in self.messages:
            total += len(self.encoder.encode(msg["content"]))
        return total
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get messages formatted for API."""
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.messages)
        return messages
    
    def summarize(self, llm) -> str:
        """Summarize conversation to save tokens."""
        if not self.messages:
            return ""
        
        conversation = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        )
        
        summary_prompt = f"Summarize this conversation briefly:\n{conversation}"
        return llm.complete(summary_prompt)


# Usage
context = ContextWindow(max_tokens=4000)
context.set_system_prompt("You are a helpful assistant.")

context.add_user_message("What is Python?")
context.add_assistant_message("Python is a high-level programming language.")
context.add_user_message("What are its main uses?")

messages = context.get_messages()
response = llm.chat(messages)
```

---

## Example 4: Error Handling with Retry

```python
import asyncio
import time
import random
from typing import TypeVar, Callable, Any, Optional
from functools import wraps
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
):
    """Retry decorator with exponential backoff."""
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_attempts - 1:
                        delay = min(
                            base_delay * (exponential_base ** attempt),
                            max_delay
                        )
                        if jitter:
                            delay *= (0.5 + random.random())
                        
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed. "
                            f"Last error: {e}"
                        )
            
            raise last_exception
        
        return wrapper
    return decorator


class AgentExecutionError(Exception):
    """Custom exception for agent execution errors."""
    pass


class ResilientAgent:
    """Agent with built-in retry logic."""
    
    def __init__(self, llm_client, retry_config: RetryConfig = None):
        self.llm = llm_client
        self.retry_config = retry_config or RetryConfig()
    
    @retry_with_backoff()
    async def execute_with_retry(self, task: str) -> Dict[str, Any]:
        """Execute task with automatic retry on transient failures."""
        try:
            result = await self._execute_task(task)
            
            if not self._is_valid(result):
                raise AgentExecutionError("Invalid output received")
            
            return result
            
        except RateLimitError:
            logger.warning("Rate limited, will retry...")
            raise
        except TimeoutError:
            logger.warning("Request timed out, will retry...")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise AgentExecutionError(f"Task execution failed: {e}")
    
    async def _execute_task(self, task: str) -> Dict:
        """Actual task execution logic."""
        response = await self.llm.generate(task)
        return {"task": task, "result": response}
    
    def _is_valid(self, result: Dict) -> bool:
        """Validate task result."""
        return (
            isinstance(result, dict)
            and "result" in result
            and result["result"] is not None
        )


# Usage
agent = ResilientAgent(llm_client=openai_client)
result = await agent.execute_with_retry("Write a hello world function")
```

---

## Example 5: Output Validation

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
import json
import re


class TaskStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"
    TIMEOUT = "timeout"


class CodeReviewOutput(BaseModel):
    """Schema for code review output."""
    bugs: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    score: int = Field(ge=1, le=10)
    summary: str
    
    @validator('score')
    def validate_score(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("Score must be between 1 and 10")
        return v


class AgentOutput(BaseModel):
    """Schema for agent output."""
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tokens_used: Optional[int] = None
    
    @validator('result')
    def validate_result_for_status(cls, v, values):
        if values.get('status') == TaskStatus.ERROR and v is not None:
            raise ValueError("Result should be None when status is error")
        return v


class OutputValidator:
    """Validates agent outputs against schemas."""
    
    def __init__(self):
        self.parsers = {
            "json": self._parse_json,
            "code": self._parse_code,
            "text": self._parse_text
        }
    
    def validate(self, output: str, schema: type) -> Dict[str, Any]:
        """Validate output against Pydantic schema."""
        try:
            # Try direct parse
            return schema.parse_raw(output)
        except Exception:
            # Try to extract JSON from output
            json_match = re.search(r'\{.*\}', output, re.DOTALL)
            if json_match:
                try:
                    return schema.parse_raw(json_match.group())
                except Exception:
                    pass
        
        raise ValidationError(f"Could not parse output as {schema.__name__}")
    
    def _parse_json(self, output: str) -> Dict:
        return json.loads(output)
    
    def _parse_code(self, output: str) -> Dict:
        """Extract code from markdown blocks."""
        match = re.search(r'```(?:\w+)?\n(.*?)\n```', output, re.DOTALL)
        return {"code": match.group(1) if match else output}
    
    def _parse_text(self, output: str) -> Dict:
        """Parse plain text output."""
        return {"text": output.strip()}


def validate_and_process(agent_output: str) -> AgentOutput:
    """Validate and process agent output."""
    validator = OutputValidator()
    
    try:
        parsed = validator.validate(agent_output, AgentOutput)
        logger.info(f"Valid output: {parsed.status}")
        return parsed
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        return AgentOutput(
            status=TaskStatus.ERROR,
            error=f"Output validation failed: {e}"
        )


# Usage
raw_output = '{"status": "success", "result": {"key": "value"}, "tokens_used": 150}'
validated = validate_and_process(raw_output)
print(f"Status: {validated.status}, Result: {validated.result}")
```

---

## Example 6: Multi-Agent Orchestration

```python
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import asyncio
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class TaskPriority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass
class Task:
    id: str
    description: str
    required_skills: List[str]
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = None
    max_retries: int = 3
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class Agent(ABC):
    """Base agent class."""
    
    def __init__(self, name: str, skills: List[str]):
        self.name = name
        self.skills = skills
        self.tasks_completed = 0
        self.tasks_failed = 0
    
    @abstractmethod
    async def execute(self, task: Task) -> Any:
        pass
    
    def can_handle(self, task: Task) -> bool:
        """Check if agent has required skills."""
        return any(skill in self.skills for skill in task.required_skills)


class Orchestrator:
    """Coordinates multiple agents to complete complex tasks."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.task_queue: List[Task] = []
        self.completed: Dict[str, Any] = {}
        self.failed: Dict[str, str] = {}
    
    def register_agent(self, agent: Agent):
        """Register an agent."""
        self.agents[agent.name] = agent
    
    def submit_task(self, task: Task):
        """Submit task to orchestrator."""
        self.task_queue.append(task)
    
    async def execute_all(self) -> Dict[str, Any]:
        """Execute all tasks respecting dependencies."""
        pending = {t.id: t for t in self.task_queue}
        
        while pending:
            # Find tasks with no pending dependencies
            ready = [
                task for task in pending.values()
                if all(dep in self.completed for dep in task.dependencies)
                and task.id not in self.failed
            ]
            
            if not ready:
                raise CircularDependencyError("No ready tasks - possible circular dependency")
            
            # Execute ready tasks
            results = await asyncio.gather(*[
                self._execute_task(task)
                for task in ready
            ], return_exceptions=True)
            
            # Update pending
            for task, result in zip(ready, results):
                if isinstance(result, Exception):
                    self.failed[task.id] = str(result)
                else:
                    self.completed[task.id] = result
                del pending[task.id]
        
        return self.completed
    
    async def _execute_task(self, task: Task) -> Any:
        """Find and execute task with appropriate agent."""
        for agent in self.agents.values():
            if agent.can_handle(task):
                for attempt in range(task.max_retries):
                    try:
                        result = await agent.execute(task)
                        agent.tasks_completed += 1
                        return result
                    except Exception as e:
                        if attempt == task.max_retries - 1:
                            agent.tasks_failed += 1
                            raise
                        await asyncio.sleep(2 ** attempt)
        
        raise NoAgentFoundError(f"No agent for task: {task.id}")


# Usage
class CodeAgent(Agent):
    async def execute(self, task: Task) -> str:
        return f"Code result for: {task.description}"

class TestAgent(Agent):
    async def execute(self, task: Task) -> str:
        return f"Test result for: {task.description}"

orchestrator = Orchestrator()
orchestrator.register_agent(CodeAgent("Coder", ["coding", "implementation"]))
orchestrator.register_agent(TestAgent("Tester", ["testing", "validation"]))

orchestrator.submit_task(Task("1", "Write login function", ["coding"]))
orchestrator.submit_task(Task("2", "Test login function", ["testing"], dependencies=["1"]))

results = asyncio.run(orchestrator.execute_all())
```

---

## Example 7: RAG Pipeline

```python
from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    content: str
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None


class VectorStore:
    """Simple in-memory vector store."""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.documents: List[Document] = []
    
    def add_documents(self, documents: List[Document]):
        """Add documents to store."""
        self.documents.extend(documents)
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Document]:
        """Search for similar documents."""
        if not self.documents:
            return []
        
        scores = []
        for doc in self.documents:
            if doc.embedding is not None:
                score = np.dot(query_embedding, doc.embedding)
                scores.append((score, doc))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scores[:top_k]]


class EmbeddingModel:
    """Embedding model wrapper."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
    
    def embed(self, text: str) -> np.ndarray:
        """Generate embedding for text."""
        # In production, use actual model
        return np.random.randn(384)  # Placeholder
    
    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for batch."""
        return np.array([self.embed(text) for text in texts])


class RAGPipeline:
    """Complete RAG pipeline."""
    
    def __init__(self, vector_store: VectorStore, embedding_model: EmbeddingModel, llm):
        self.store = vector_store
        self.embedder = embedding_model
        self.llm = llm
    
    def add_documents(self, documents: List[Document]):
        """Add documents to knowledge base."""
        for doc in documents:
            doc.embedding = self.embedder.embed(doc.content)
        self.store.add_documents(documents)
    
    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Query the RAG system."""
        # Embed question
        query_emb = self.embedder.embed(question)
        
        # Retrieve relevant documents
        relevant_docs = self.store.search(query_emb, top_k=top_k)
        
        if not relevant_docs:
            return {
                "answer": "I don't have information on that topic.",
                "sources": []
            }
        
        # Build context
        context = "\n\n".join([
            f"[{i+1}] {doc.content}"
            for i, doc in enumerate(relevant_docs)
        ])
        
        # Generate answer
        prompt = f"""
        Context:
        {context}
        
        Question: {question}
        
        Answer the question based on the context above. Cite sources with [1], [2], etc.
        If the context doesn't contain the answer, say so explicitly.
        """
        
        answer = self.llm.generate(prompt)
        
        return {
            "answer": answer,
            "sources": [{"id": doc.id, "content": doc.content[:200]} for doc in relevant_docs]
        }


# Usage
embedder = EmbeddingModel()
store = VectorStore(dimension=384)

# Add documents
docs = [
    Document(id="1", content="Python is a high-level programming language."),
    Document(id="2", content="JavaScript is used for web development."),
    Document(id="3", content="Machine learning uses Python extensively.")
]

rag = RAGPipeline(store, embedder, llm_client=openai_client)
rag.add_documents(docs)

result = rag.query("What is Python used for?")
print(result["answer"])
```

---

## Example 8: Memory-Augmented Agent

```python
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np


class MemoryItem:
    content: Any
    importance: float
    timestamp: datetime
    access_count: int
    
    def __init__(self, content: Any, importance: float = 0.5):
        self.content = content
        self.importance = importance
        self.timestamp = datetime.now()
        self.access_count = 0
    
    def access(self):
        self.access_count += 1
        self.timestamp = datetime.now()


class AgentMemory:
    """Agent memory with importance-based retrieval."""
    
    def __init__(self, max_items: int = 100):
        self.memories: List[MemoryItem] = []
        self.max_items = max_items
        self.index: Dict[str, int] = {}
    
    def store(self, content: Any, importance: float = 0.5, key: str = None):
        """Store new memory."""
        if len(self.memories) >= self.max_items:
            # Remove least important, least accessed memory
            self.memories.sort(key=lambda m: (m.importance, m.access_count))
            removed = self.memories.pop(0)
            if removed.content in self.index:
                del self.index[removed.content]
        
        item = MemoryItem(content, importance)
        self.memories.append(item)
        
        if key:
            self.index[key] = len(self.memories) - 1
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        """Retrieve relevant memories (simple keyword matching for demo)."""
        query_words = set(query.lower().split())
        
        scored = []
        for item in self.memories:
            content_words = set(str(item.content).lower().split())
            overlap = len(query_words & content_words)
            
            recency = 1.0 / (1 + (datetime.now() - item.timestamp).total_seconds() / 3600)
            score = overlap * 0.5 + item.importance * 0.3 + recency * 0.2
            
            scored.append((score, item))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        results = [item.content for _, item in scored[:top_k]]
        for _, item in scored[:top_k]:
            item.access()
        
        return results


class MemoryAugmentedAgent:
    """Agent that uses memory for context."""
    
    def __init__(self, llm, memory: AgentMemory):
        self.llm = llm
        self.memory = memory
    
    async def execute(self, task: str, use_memory: bool = True) -> str:
        """Execute task with memory augmentation."""
        context_parts = []
        
        if use_memory:
            relevant_memories = self.memory.retrieve(task, top_k=3)
            if relevant_memories:
                context_parts.append("Relevant memories:\n" + "\n".join(
                    f"- {mem}" for mem in relevant_memories
                ))
        
        prompt = "\n\n".join(context_parts + [f"Task: {task}"])
        response = await self.llm.generate(prompt)
        
        # Store interaction in memory
        self.memory.store(
            content=f"Task: {task} -> {response[:100]}",
            importance=0.6
        )
        
        return response


# Usage
memory = AgentMemory(max_items=100)
agent = MemoryAugmentedAgent(llm_client, memory)

# Store some memories
memory.store("User prefers Python over JavaScript", importance=0.8, key="preference")
memory.store("Previous task involved database optimization", importance=0.7)

# Execute task
result = asyncio.run(agent.execute("Help me optimize my code"))
```

---

## Example 9: Streaming Response Handler

```python
from typing import AsyncIterator, Optional
import asyncio
from dataclasses import dataclass

@dataclass
class StreamChunk:
    content: str
    index: int
    is_final: bool = False
    metadata: Dict[str, Any] = None


class StreamingHandler:
    """Handle streaming LLM responses."""
    
    def __init__(self, buffer_size: int = 4096):
        self.buffer_size = buffer_size
        self.buffer = ""
        self.chunks_received = 0
    
    async def stream_response(
        self,
        llm_stream: AsyncIterator[str],
        on_chunk: Optional[callable] = None,
        on_complete: Optional[callable] = None
    ) -> str:
        """Process streaming response."""
        full_response = ""
        
        async for chunk in llm_stream:
            self.chunks_received += 1
            self.buffer += chunk
            full_response += chunk
            
            if on_chunk:
                await on_chunk(StreamChunk(
                    content=chunk,
                    index=self.chunks_received
                ))
            
            # Handle buffer overflow
            if len(self.buffer) > self.buffer_size:
                self.buffer = self.buffer[-self.buffer_size:]
        
        if on_complete:
            await on_complete(StreamChunk(
                content=full_response,
                index=self.chunks_received,
                is_final=True
            ))
        
        return full_response


class BufferedStreamWriter:
    """Buffer and batch stream writes."""
    
    def __init__(self, flush_interval: float = 0.1):
        self.flush_interval = flush_interval
        self.buffer = ""
        self.last_flush = time.time()
    
    async def write(self, content: str):
        """Write content to buffer."""
        self.buffer += content
        
        if time.time() - self.last_flush > self.flush_interval:
            await self.flush()
    
    async def flush(self):
        """Flush buffer."""
        if self.buffer:
            # In real implementation, write to socket/file
            print(self.buffer, end="", flush=True)
            self.buffer = ""
            self.last_flush = time.time()


# Usage
async def stream_chat(prompt: str):
    handler = StreamingHandler()
    
    async def on_chunk(chunk: StreamChunk):
        print(chunk.content, end="", flush=True)
    
    stream = llm_client.stream(prompt)
    response = await handler.stream_response(stream, on_chunk=on_chunk)
    print()  # New line after streaming
    return response

response = asyncio.run(stream_chat("Tell me a story"))
```

---

## Example 10: Cost-Tracked Agent

```python
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    model: str
    timestamp: datetime = field(default_factory=datetime.now)


class CostTracker:
    """Track costs across sessions."""
    
    MODEL_PRICING = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
        "claude-3-opus": {"prompt": 0.015, "completion": 0.075}
    }
    
    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.usage_log: List[TokenUsage] = []
        self.load_usage()
    
    def record(self, usage: TokenUsage):
        """Record token usage."""
        self.usage_log.append(usage)
        self._persist()
    
    def calculate_cost(self, usage: TokenUsage) -> float:
        """Calculate cost for a usage record."""
        pricing = self.MODEL_PRICING.get(usage.model, {})
        prompt_cost = (usage.prompt_tokens / 1000) * pricing.get("prompt", 0)
        completion_cost = (usage.completion_tokens / 1000) * pricing.get("completion", 0)
        return prompt_cost + completion_cost
    
    def get_daily_cost(self, date: Optional[datetime] = None) -> float:
        """Get total cost for a day."""
        date = date or datetime.now()
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        daily_usage = [
            u for u in self.usage_log
            if day_start <= u.timestamp < day_end
        ]
        
        return sum(self.calculate_cost(u) for u in daily_usage)
    
    def is_budget_available(self, estimated_tokens: int, model: str) -> bool:
        """Check if budget allows new request."""
        pricing = self.MODEL_PRICING.get(model, {})
        estimated_cost = (estimated_tokens / 1000) * max(
            pricing.get("prompt", 0),
            pricing.get("completion", 0)
        )
        
        remaining = self.daily_budget - self.get_daily_cost()
        return estimated_cost <= remaining
    
    def _persist(self):
        """Persist usage to disk."""
        with open("cost_usage.json", "w") as f:
            json.dump([
                {
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "model": u.model,
                    "timestamp": u.timestamp.isoformat()
                }
                for u in self.usage_log
            ], f)
    
    def load_usage(self):
        """Load usage from disk."""
        try:
            with open("cost_usage.json") as f:
                data = json.load(f)
                self.usage_log = [
                    TokenUsage(
                        prompt_tokens=d["prompt_tokens"],
                        completion_tokens=d["completion_tokens"],
                        model=d["model"],
                        timestamp=datetime.fromisoformat(d["timestamp"])
                    )
                    for d in data
                ]
        except FileNotFoundError:
            self.usage_log = []


class CostAwareAgent:
    """Agent with cost tracking."""
    
    def __init__(self, llm, cost_tracker: CostTracker):
        self.llm = llm
        self.cost_tracker = cost_tracker
    
    async def execute(self, task: str, model: str = "gpt-3.5-turbo") -> str:
        """Execute with cost awareness."""
        estimated_tokens = len(task.split()) * 2
        
        if not self.cost_tracker.is_budget_available(estimated_tokens, model):
            raise BudgetExceededError("Daily token budget exceeded")
        
        response = await self.llm.generate(task, model=model)
        
        self.cost_tracker.record(TokenUsage(
            prompt_tokens=estimated_tokens,
            completion_tokens=len(response.split()),
            model=model
        ))
        
        return response
```

---

## Example 11: Safety-First Agent

```python
from typing import List, Dict, Any
import re
from enum import Enum

class SafetyLevel(Enum):
    PERMISSIVE = "permissive"
    BALANCED = "balanced"
    STRICT = "strict"


class SafetyFilter:
    """Safety filter for agent inputs and outputs."""
    
    def __init__(self, level: SafetyLevel = SafetyLevel.BALANCED):
        self.level = level
        self.blocked_patterns = self._load_patterns()
    
    def _load_patterns(self) -> List[re.Pattern]:
        """Load safety patterns based on level."""
        base_patterns = [
            r"(?i)(how to|instructions for).*(?:bomb|explosive|weapon)",
            r"(?i)(how to|instructions for).*(?:hack|attack|exploit)",
            r"(?i)(buy|acquire|get).*(?:drugs|illegal substances)",
        ]
        
        if self.level == SafetyLevel.STRICT:
            base_patterns.extend([
                r"(?i)(?:secret|confidential|private).*(?:password|key|credential)",
                r"(?i)personal.?(?:information|data|details)"
            ])
        
        return [re.compile(p) for p in base_patterns]
    
    def check_input(self, user_input: str) -> Dict[str, Any]:
        """Check if input is safe."""
        violations = []
        for pattern in self.blocked_patterns:
            if pattern.search(user_input):
                violations.append(pattern.pattern)
        
        return {
            "safe": len(violations) == 0,
            "violations": violations,
            "action": "block" if violations else "allow"
        }
    
    def check_output(self, output: str) -> Dict[str, Any]:
        """Check if output is safe."""
        violations = []
        for pattern in self.blocked_patterns:
            if pattern.search(output):
                violations.append(pattern.pattern)
        
        return {
            "safe": len(violations) == 0,
            "violations": violations
        }


class SafeAgent:
    """Agent with built-in safety checks."""
    
    def __init__(self, llm, safety_level: SafetyLevel = SafetyLevel.BALANCED):
        self.llm = llm
        self.safety = SafetyFilter(safety_level)
    
    async def execute(self, user_input: str) -> Dict[str, Any]:
        """Execute with safety checks."""
        # Check input
        input_check = self.safety.check_input(user_input)
        if not input_check["safe"]:
            return {
                "status": "blocked",
                "reason": "Input violates safety policies",
                "violations": input_check["violations"]
            }
        
        # Execute
        try:
            response = await self.llm.generate(user_input)
            
            # Check output
            output_check = self.safety.check_output(response)
            if not output_check["safe"]:
                logger.warning(f"Unsafe output generated: {output_check['violations']}")
                return {
                    "status": "filtered",
                    "response": "I cannot provide that information.",
                    "reason": "Output was filtered for safety"
                }
            
            return {
                "status": "success",
                "response": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }


# Usage
safe_agent = SafeAgent(llm_client, safety_level=SafetyLevel.STRICT)
result = await safe_agent.execute("Tell me about Python programming")
print(result["response"])
```

---

## Example 12: Evaluation Framework

```python
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from statistics import mean, stdev

@dataclass
class TestCase:
    id: str
    input: str
    expected: Any
    category: str = "general"
    weight: float = 1.0
    metadata: Dict[str, Any] = None


@dataclass
class EvaluationResult:
    test_id: str
    passed: bool
    score: float
    actual: Any
    expected: Any
    error: Optional[str] = None
    latency_ms: float = 0.0


class Metric:
    """Evaluation metric calculator."""
    
    @staticmethod
    def exact_match(actual: str, expected: str) -> float:
        """Exact string match."""
        return 1.0 if actual.strip().lower() == expected.strip().lower() else 0.0
    
    @staticmethod
    def contains(actual: str, expected: str) -> float:
        """Check if expected substring in actual."""
        return 1.0 if expected.lower() in actual.lower() else 0.0
    
    @staticmethod
    def keyword_match(actual: str, keywords: List[str]) -> float:
        """Check if any keyword present."""
        actual_lower = actual.lower()
        matches = sum(1 for kw in keywords if kw.lower() in actual_lower)
        return matches / len(keywords) if keywords else 0.0


class EvaluationFramework:
    """Comprehensive evaluation framework."""
    
    def __init__(self):
        self.metrics = {
            "exact_match": Metric.exact_match,
            "contains": Metric.contains,
            "keyword_match": Metric.keyword_match
        }
        self.results: List[EvaluationResult] = []
    
    def evaluate(
        self,
        test_cases: List[TestCase],
        model_fn: Callable,
        metric_names: List[str]
    ) -> Dict[str, Any]:
        """Run evaluation on test cases."""
        self.results = []
        
        for case in test_cases:
            start = time.time()
            
            try:
                actual = model_fn(case.input)
                latency = (time.time() - start) * 1000
                
                # Calculate score across metrics
                scores = []
                for metric_name in metric_names:
                    metric_fn = self.metrics[metric_name]
                    if metric_name == "keyword_match":
                        score = metric_fn(actual, case.expected)
                    else:
                        score = metric_fn(actual, case.expected)
                    scores.append(score)
                
                final_score = mean(scores)
                passed = final_score >= 0.5  # Threshold
                
                self.results.append(EvaluationResult(
                    test_id=case.id,
                    passed=passed,
                    score=final_score,
                    actual=actual,
                    expected=case.expected,
                    latency_ms=latency
                ))
                
            except Exception as e:
                self.results.append(EvaluationResult(
                    test_id=case.id,
                    passed=False,
                    score=0.0,
                    actual=None,
                    expected=case.expected,
                    error=str(e)
                ))
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate evaluation report."""
        if not self.results:
            return {}
        
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]
        
        scores = [r.score for r in self.results]
        latencies = [r.latency_ms for r in self.results]
        
        return {
            "total_tests": len(self.results),
            "passed": len(passed),
            "failed": len(failed),
            "pass_rate": len(passed) / len(self.results),
            "avg_score": mean(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "avg_latency_ms": mean(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "results_by_category": self._group_by_category()
        }
    
    def _group_by_category(self) -> Dict[str, Dict]:
        categories = {}
        for result in self.results:
            category = result.test_id.split("-")[0]  # Extract category from ID
            if category not in categories:
                categories[category] = {"passed": 0, "total": 0}
            categories[category]["total"] += 1
            if result.passed:
                categories[category]["passed"] += 1
        return categories


# Usage
def dummy_model(input_text: str) -> str:
    """Replace with actual model."""
    return f"Response to: {input_text}"

framework = EvaluationFramework()

test_cases = [
    TestCase("g1-q1", "What is Python?", "programming language", "general", keywords=["python", "language"]),
    TestCase("g1-q2", "What is AI?", "artificial intelligence", "general", keywords=["artificial", "intelligence"]),
]

report = framework.evaluate(
    test_cases=test_cases,
    model_fn=dummy_model,
    metric_names=["contains", "keyword_match"]
)

print(f"Pass rate: {report['pass_rate']:.1%}")
print(f"Average score: {report['avg_score']:.2f}")
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)
- [Advanced](./advanced.md)
