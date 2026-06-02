# Core Domain - Advanced Concepts

## Overview

This document covers advanced concepts and techniques for building sophisticated LLM/agentic systems. These patterns enable production-grade agent orchestration, memory systems, planning, and multi-agent coordination.

## Table of Contents

1. [Multi-Agent Orchestration](#multi-agent-orchestration)
2. [Reflection and Self-Correction](#reflection-and-self-correction)
3. [Planning with Tree Search](#planning-with-tree-search)
4. [Memory Systems](#memory-systems)
5. [Chain of Thought Reasoning](#chain-of-thought-reasoning)
6. [ReAct Pattern](#react-pattern)
7. [Plan-and-Solve](#plan-and-solve)
8. [Few-Shot Prompting Strategies](#few-shot-prompting-strategies)
9. [Tree of Thoughts](#tree-of-thoughts)
10. [Constitutional AI](#constitutional-ai)
11. [Multi-Modal Agent Design](#multi-modal-agent-design)
12. [Agent Communication Protocols](#agent-communication-protocols)
13. [Hierarchical Agent Systems](#hierarchical-agent-systems)
14. [Self-Ask and Search](#self-ask-and-search)
15. [Automatic Prompt Engineering](#automatic-prompt-engineering)
16. [Retrieval-Augmented Generation](#retrieval-augmented-generation)
17. [Tool Composition and Abstraction](#tool-composition-and-abstraction)
18. [Stateful vs Stateless Agents](#stateful-vs-stateless-agents)
19. [Memory-Augmented Agents](#memory-augmented-agents)
20. [Evaluation and Benchmarking](#evaluation-and-benchmarking)

---

## Multi-Agent Orchestration

Multi-agent systems coordinate specialized agents to solve complex tasks. This pattern distributes work across agents with different capabilities.

### Core Architecture

```python
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AgentTask:
    """Represents a task to be executed by an agent."""
    description: str
    required_skills: List[str]
    result: Any = None
    status: str = "pending"
    priority: int = 0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AgentCapability:
    """Defines what an agent can do."""
    name: str
    skills: List[str]
    max_concurrent_tasks: int = 1
    cost_per_token: float = 0.0
    latency_model: Optional[callable] = None


class Orchestrator:
    """Coordinates multiple specialized agents."""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.capabilities: Dict[str, AgentCapability] = {}
        self.task_history: List[AgentTask] = []
        self.failure_counts: Dict[str, int] = {}
    
    def register_agent(self, agent: BaseAgent, capability: AgentCapability):
        """Register an agent with its capability profile."""
        self.agents[capability.name] = agent
        self.capabilities = {**self.capabilities, **{skill: capability for skill in capability.skills}}
    
    async def execute_task(self, task: AgentTask) -> Any:
        """Execute task using appropriate agent(s)."""
        suitable_agents = [
            (name, self.agents[name])
            for name, cap in self.capabilities.items()
            if any(skill in task.required_skills for skill in cap.skills)
            and name in self.agents
        ]
        
        if not suitable_agents:
            raise NoAgentFoundError(f"No agent found for skills: {task.required_skills}")
        
        primary_name, primary_agent = suitable_agents[0]
        result = await primary_agent.execute(task.description)
        
        if len(suitable_agents) > 1:
            validation_tasks = [
                self.agents[name].validate(result)
                for name, _ in suitable_agents[1:]
            ]
            validations = await asyncio.gather(*validation_tasks, return_exceptions=True)
            result = self._merge_results(result, validations)
        
        task.result = result
        task.status = "completed"
        self.task_history.append(task)
        return result
    
    def _merge_results(self, primary: Any, validations: List[Any]) -> Any:
        """Merge validation results with primary result."""
        if isinstance(primary, dict):
            merged = primary.copy()
            merged["validations"] = validations
            return merged
        return {"primary": primary, "validations": validations}


class MetaAgent(ABC):
    """Agent that can reason about and coordinate other agents."""
    
    @abstractmethod
    def decompose_task(self, task: str) -> List[AgentTask]:
        """Break down complex task into subtasks."""
        pass
    
    @abstractmethod
    def compose_results(self, results: List[Any]) -> Any:
        """Combine results from subtasks."""
        pass
    
    async def execute_complex_task(self, task: str, orchestrator: Orchestrator) -> Any:
        """Decompose, execute, and compose a complex task."""
        subtasks = self.decompose_task(task)
        
        # Check dependencies
        pending = [t for t in subtasks if not t.dependencies]
        completed = {}
        
        while pending:
            results = await asyncio.gather(*[
                orchestrator.execute_task(task)
                for task in pending
            ], return_exceptions=True)
            
            for task, result in zip(pending, results):
                if isinstance(result, Exception):
                    task.status = "failed"
                    task.metadata["error"] = str(result)
                else:
                    task.status = "completed"
                    task.result = result
                    completed[task.description] = result
            
            # Find next batch
            pending = [
                t for t in subtasks
                if t.status == "pending"
                and all(dep in completed for dep in t.dependencies)
            ]
        
        successful = [t.result for t in subtasks if t.status == "completed"]
        return self.compose_results(successful)
```

### Production Orchestration Patterns

```python
class ProductionOrchestrator:
    """Orchestrator with retry, fallback, and monitoring."""
    
    def __init__(self, retry_policy: Dict[str, int] = None):
        self.retry_policy = retry_policy or {"max_attempts": 3, "backoff_factor": 2}
    
    async def execute_with_fallback(
        self,
        primary_agent: BaseAgent,
        fallback_agent: BaseAgent,
        task: str
    ) -> Any:
        """Try primary agent, fall back on failure."""
        for attempt in range(self.retry_policy["max_attempts"]):
            try:
                return await primary_agent.execute(task)
            except Exception as e:
                if attempt == self.retry_policy["max_attempts"] - 1:
                    return await fallback_agent.execute(task)
                await asyncio.sleep(self.retry_policy["backoff_factor"] ** attempt)
    
    def route_by_complexity(self, task: str) -> BaseAgent:
        """Route tasks to appropriate agent based on complexity."""
        complexity = self._estimate_complexity(task)
        if complexity > 0.7:
            return self.agents["advanced"]
        elif complexity > 0.3:
            return self.agents["standard"]
        else:
            return self.agents["fast"]
```

---

## Reflection and Self-Correction

Reflective agents iteratively improve outputs through self-evaluation. This pattern is essential for high-quality task completion.

### Reflective Agent Implementation

```python
class ReflectiveAgent:
    """Agent with self-reflection capabilities."""
    
    def __init__(self, llm, max_reflections: int = 3, improvement_threshold: float = 0.1):
        self.llm = llm
        self.max_reflections = max_reflections
        self.improvement_threshold = improvement_threshold
        self.reflection_history: List[Dict] = []
    
    async def execute_with_reflection(self, task: str) -> Dict[str, Any]:
        """Execute task with iterative refinement."""
        result = await self._execute(task)
        initial_score = await self._evaluate(task, result)
        
        best_result = result
        best_score = initial_score
        
        for i in range(self.max_reflections):
            reflection = await self._reflect(task, best_result, best_score)
            
            self.reflection_history.append({
                "iteration": i + 1,
                "score": best_score,
                "issues": reflection["issues"],
                "improvements": reflection["suggestions"]
            })
            
            if not reflection["needs_improvement"]:
                break
            
            improved_task = self._improve_task(task, best_result, reflection)
            result = await self._execute(improved_task)
            score = await self._evaluate(task, result)
            
            if score - best_score < self.improvement_threshold:
                break
            
            best_result = result
            best_score = score
        
        return {
            "result": best_result,
            "initial_score": initial_score,
            "final_score": best_score,
            "reflections": self.reflection_history,
            "converged": i < self.max_reflections - 1
        }
    
    async def _execute(self, task: str) -> Any:
        """Execute the task."""
        prompt = self._build_execution_prompt(task)
        return await self.llm.complete(prompt)
    
    async def _reflect(self, task: str, result: Any, score: float) -> Dict:
        """Reflect on the result quality."""
        prompt = f"""
        Task: {task}
        Result: {result}
        Quality Score: {score}/10
        
        Analyze the result:
        1. Does it fully address the task requirements?
        2. Are there any errors, omissions, or issues?
        3. How could it be significantly improved?
        
        Return JSON:
        {{
            "needs_improvement": boolean,
            "issues": ["list of specific issues"],
            "suggestions": ["list of concrete improvements"],
            "priority": "high|medium|low"
        }}
        """
        return await self.llm.complete_json(prompt)
    
    def _improve_task(self, original_task: str, result: Any, reflection: Dict) -> str:
        """Create improved task based on reflection."""
        improvements = "\n".join(f"- {s}" for s in reflection["suggestions"])
        return f"""
        Original task: {original_task}
        Previous attempt: {result}
        
        Issues to address:
        {chr(10).join(f"- {issue}" for issue in reflection["issues"])}
        
        Improvements to apply:
        {improvements}
        
        Generate a significantly improved result addressing all issues above.
        """
    
    async def _evaluate(self, task: str, result: Any) -> float:
        """Evaluate result quality."""
        prompt = f"Rate this result 1-10 for task: {task}\nResult: {result}\nScore:"
        response = await self.llm.complete(prompt)
        try:
            return float(response.strip())
        except ValueError:
            return 5.0
```

### Production Reflection Pattern

```python
class ProductionReflectiveAgent:
    """Production-ready reflective agent with caching and monitoring."""
    
    def __init__(self, llm, cache_dir: str = "./reflection_cache"):
        self.llm = llm
        self.cache_dir = cache_dir
        self.reflection_stats = {
            "total_executions": 0,
            "total_reflections": 0,
            "improvement_rate": 0.0
        }
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        cache_key = self._cache_key(task, context)
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await self.execute_with_reflection(task)
        self._cache_result(cache_key, result)
        
        self.reflection_stats["total_executions"] += 1
        self.reflection_stats["total_reflections"] += result.get("reflection_count", 0)
        
        return result
```

---

## Planning with Tree Search

Advanced agents use planning algorithms to generate and evaluate action sequences before execution.

### A* Planning Agent

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
import heapq
import json

@dataclass
class PlanNode:
    """Node in the planning tree."""
    state: Dict[str, Any]
    action: Optional[str]
    cost: float
    parent: Optional['PlanNode']
    depth: int = 0
    
    def __lt__(self, other):
        return self.cost < other.cost


class PlanningAgent:
    """Agent that uses A* search for planning."""
    
    def __init__(self, llm, max_depth: int = 5, heuristic_weight: float = 1.0):
        self.llm = llm
        self.max_depth = max_depth
        self.heuristic_weight = heuristic_weight
    
    async def plan(self, goal: Dict, initial_state: Dict) -> List[str]:
        """Generate a plan using A* search."""
        frontier = []
        heapq.heappush(frontier, PlanNode(
            state=initial_state,
            action=None,
            cost=0,
            parent=None,
            depth=0
        ))
        
        explored = set()
        nodes_explored = 0
        
        while frontier and nodes_explored < 100:
            node = heapq.heappop(frontier)
            nodes_explored += 1
            
            if self._is_goal(node.state, goal):
                return self._extract_plan(node)
            
            if node.depth >= self.max_depth:
                continue
            
            state_hash = self._hash_state(node.state)
            if state_hash in explored:
                continue
            explored.add(state_hash)
            
            actions = await self._generate_actions(node.state, goal)
            
            for action in actions:
                new_state = await self._apply_action(node.state, action)
                g_cost = node.cost + action.get("cost", 1.0)
                h_cost = self._heuristic(new_state, goal)
                f_cost = g_cost + self.heuristic_weight * h_cost
                
                heapq.heappush(frontier, PlanNode(
                    state=new_state,
                    action=action["name"],
                    cost=f_cost,
                    parent=node,
                    depth=node.depth + 1
                ))
        
        return []  # No plan found
    
    async def _generate_actions(self, state: Dict, goal: Dict) -> List[Dict]:
        """Use LLM to generate possible actions with cost estimates."""
        prompt = f"""
        Current state: {json.dumps(state, indent=2)}
        Goal: {json.dumps(goal, indent=2)}
        
        List up to 5 possible actions to progress toward the goal.
        For each action, provide:
        1. name: short action name
        2. description: what it does
        3. cost: estimated cost (1-10)
        4. preconditions: required state
        
        Return as JSON array.
        """
        response = await self.llm.complete_json(prompt)
        return response if isinstance(response, list) else []
    
    async def _apply_action(self, state: Dict, action: Dict) -> Dict:
        """Apply action to state (simulated or real)."""
        new_state = state.copy()
        for key, value in action.get("effects", {}).items():
            new_state[key] = value
        return new_state
    
    def _heuristic(self, state: Dict, goal: Dict) -> float:
        """Estimate cost to reach goal from state."""
        if not goal:
            return 0.0
        
        common_keys = set(state.keys()) & set(goal.keys())
        if not common_keys:
            return 10.0
        
        differences = sum(
            1 for key in common_keys
            if state[key] != goal[key]
        )
        return differences / len(common_keys)
    
    def _is_goal(self, state: Dict, goal: Dict) -> bool:
        """Check if state satisfies goal."""
        return all(state.get(k) == v for k, v in goal.items())
    
    def _hash_state(self, state: Dict) -> str:
        """Hash state for duplicate detection."""
        return json.dumps(state, sort_keys=True)
    
    def _extract_plan(self, node: PlanNode) -> List[str]:
        """Extract plan from goal node."""
        plan = []
        current = node
        while current.parent:
            if current.action:
                plan.append(current.action)
            current = current.parent
        return list(reversed(plan))
```

### MCTS Planning

```python
class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.value = 0.0
    
    def ucb1(self, exploration=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration * (2 * (self.parent.visits if self.parent else 0) / self.visits) ** 0.5


class MCTSPlanner:
    def __init__(self, llm, simulations: int = 100):
        self.llm = llm
        self.simulations = simulations
    
    async def search(self, initial_state: Dict, goal: Dict) -> List[str]:
        root = MCTSNode(initial_state)
        
        for _ in range(self.simulations):
            node = self._select(root)
            child = await self._expand(node)
            reward = await self._simulate(child.state, goal)
            self._backpropagate(child, reward)
        
        if not root.children:
            return []
        
        best = max(root.children, key=lambda c: c.visits)
        return self._extract_path(best)
    
    def _select(self, node: MCTSNode) -> MCTSNode:
        while node.children and not self._is_terminal(node):
            node = max(node.children, key=lambda c: c.ucb1())
        return node
    
    async def _expand(self, node: MCTSNode) -> MCTSNode:
        if not node.children:
            actions = await self._get_actions(node.state)
            for action in actions:
                new_state = await self._apply_action(node.state, action)
                child = MCTSNode(new_state, parent=node, action=action["name"])
                node.children.append(child)
        return node.children[0] if node.children else node
    
    async def _simulate(self, state: Dict, goal: Dict) -> float:
        """Rollout simulation to estimate value."""
        return self._heuristic(state, goal) / 10.0
    
    def _backpropagate(self, node: MCTSNode, reward: float):
        current = node
        while current:
            current.visits += 1
            current.value += reward
            current = current.parent
```

---

## Memory Systems

Sophisticated memory systems enable agents to learn from experience and maintain context across interactions.

### Comprehensive Memory Architecture

```python
from typing import Any, Dict, List, Optional, Tuple
import time
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

class MemoryType(Enum):
    EPISODIC = "episodic"      # Specific experiences
    SEMANTIC = "semantic"      # General knowledge
    WORKING = "working"        # Current context
    PROCEDURAL = "procedural"  # How-to knowledge


@dataclass
class MemoryItem:
    """Single memory entry with metadata."""
    content: Any
    memory_type: MemoryType
    importance: float = 0.5
    embedding: Optional[np.ndarray] = None
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    decay_factor: float = 0.95
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_access(self):
        self.access_count += 1
        self.last_accessed = time.time()
        self.importance = min(1.0, self.importance * 1.1)


class AgentMemory:
    """Comprehensive memory system for agents."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.episodic: List[MemoryItem] = []
        self.semantic: Dict[str, MemoryItem] = {}
        self.working: Dict[str, MemoryItem] = {}
        self.procedural: List[MemoryItem] = []
        
        self.max_episodic = config.get("max_episodic", 1000)
        self.max_working = config.get("max_working", 7)
        self.consolidation_threshold = config.get("consolidation_threshold", 100)
        self.importance_threshold = config.get("importance_threshold", 0.3)
        
        self.embedder = config.get("embedder")
    
    def store(
        self,
        content: Any,
        memory_type: MemoryType = MemoryType.EPISODIC,
        importance: float = 0.5,
        tags: List[str] = None,
        metadata: Dict = None
    ) -> str:
        """Store new memory and return memory ID."""
        embedding = None
        if self.embedder and isinstance(content, str):
            embedding = self.embedder(content)
        
        item = MemoryItem(
            content=content,
            memory_type=memory_type,
            importance=importance,
            embedding=embedding,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        if memory_type == MemoryType.EPISODIC:
            self.episodic.append(item)
            self._consolidate_if_needed()
        elif memory_type == MemoryType.SEMANTIC:
            key = self._generate_key(content)
            self.semantic[key] = item
        elif memory_type == MemoryType.WORKING:
            key = metadata.get("key", str(id(item)))
            self.working[key] = item
            self._trim_working()
        elif memory_type == MemoryType.PROCEDURAL:
            self.procedural.append(item)
        
        return str(id(item))
    
    def retrieve(
        self,
        query: Any,
        memory_type: Optional[MemoryType] = None,
        top_k: int = 5,
        min_similarity: float = 0.5
    ) -> List[MemoryItem]:
        """Retrieve relevant memories."""
        query_embedding = None
        if self.embedder and isinstance(query, str):
            query_embedding = self.embedder(query)
        
        candidates = self._get_candidates(memory_type)
        
        if query_embedding is not None:
            scored = []
            for item in candidates:
                if item.embedding is not None:
                    similarity = self._cosine_similarity(query_embedding, item.embedding)
                    recency = self._calculate_recency(item)
                    score = similarity * 0.7 + recency * 0.2 + item.importance * 0.1
                    scored.append((score, item))
            
            scored.sort(reverse=True)
            results = [item for score, item in scored[:top_k] if score >= min_similarity]
        else:
            results = candidates[:top_k]
        
        for item in results:
            item.update_access()
        
        return results
    
    def _get_candidates(self, memory_type: Optional[MemoryType]) -> List[MemoryItem]:
        if memory_type == MemoryType.EPISODIC:
            return self.episodic
        elif memory_type == MemoryType.SEMANTIC:
            return list(self.semantic.values())
        elif memory_type == MemoryType.WORKING:
            return list(self.working.values())
        elif memory_type == MemoryType.PROCEDURAL:
            return self.procedural
        return self.episodic + list(self.semantic.values()) + list(self.working.values())
    
    def _consolidate_if_needed(self):
        """Consolidate memories when episodic store is full."""
        if len(self.episodic) >= self.max_episodic:
            important = [m for m in self.episodic if m.importance > self.importance_threshold]
            self.episodic = important[:self.max_episodic // 2]
    
    def _trim_working(self):
        """Keep only most important working memories."""
        if len(self.working) > self.max_working:
            sorted_items = sorted(
                self.working.items(),
                key=lambda x: x[1].importance,
                reverse=True
            )
            self.working = dict(sorted_items[:self.max_working])
    
    @staticmethod
    def _generate_key(content: Any) -> str:
        return str(hash(str(content)))
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    @staticmethod
    def _calculate_recency(item: MemoryItem) -> float:
        age_seconds = time.time() - item.last_accessed
        age_hours = age_seconds / 3600
        return max(0.0, 1.0 - (age_hours / 24.0))
```

### Memory-Augmented Agent

```python
class MemoryAugmentedAgent:
    """Agent that uses memory for improved performance."""
    
    def __init__(self, llm, memory: AgentMemory):
        self.llm = llm
        self.memory = memory
    
    async def execute(self, task: str, context: Dict = None) -> Dict:
        """Execute task with memory augmentation."""
        relevant_memories = self.memory.retrieve(
            query=task,
            top_k=5,
            min_similarity=0.6
        )
        
        prompt = self._build_prompt_with_memories(task, relevant_memories, context)
        result = await self.llm.complete(prompt)
        
        self.memory.store(
            content={"task": task, "result": result},
            memory_type=MemoryType.EPISODIC,
            importance=0.7,
            tags=["execution", task[:50]]
        )
        
        return result
    
    def _build_prompt_with_memories(
        self,
        task: str,
        memories: List[MemoryItem],
        context: Dict = None
    ) -> str:
        prompt = "You are a helpful assistant with access to past experiences.\n\n"
        
        if memories:
            prompt += "Relevant past experiences:\n"
            for mem in memories:
                prompt += f"- {mem.content}\n"
            prompt += "\n"
        
        if context:
            prompt += f"Context: {context}\n\n"
        
        prompt += f"Task: {task}"
        return prompt
```

---

## Chain of Thought Reasoning

Chain of Thought (CoT) prompting encourages step-by-step reasoning for complex problems.

### CoT Implementation

```python
class CoTAgent:
    """Agent using Chain of Thought reasoning."""
    
    def __init__(self, llm, examples: List[Dict] = None):
        self.llm = llm
        self.examples = examples or []
        self.reasoning_templates = {
            "math": "Let's solve this step by step:\n{steps}\n\nAnswer: {answer}",
            "logic": "Let me analyze this logically:\n{steps}\n\nConclusion: {answer}",
            "code": "Let me trace through this:\n{steps}\n\nSolution: {answer}"
        }
    
    async def reason(self, problem: str, domain: str = "general") -> Dict[str, Any]:
        """Perform chain of thought reasoning."""
        prompt = self._build_cot_prompt(problem, domain)
        response = await self.llm.complete(prompt)
        
        reasoning = self._parse_reasoning(response)
        
        return {
            "reasoning_chain": reasoning["steps"],
            "final_answer": reasoning["answer"],
            "confidence": reasoning.get("confidence", 1.0),
            "raw_response": response
        }
    
    def _build_cot_prompt(self, problem: str, domain: str) -> str:
        template = self.reasoning_templates.get(domain, "{steps}\n\nAnswer: {answer}")
        
        prompt = "Think step by step to solve the following problem.\n\n"
        
        if self.examples:
            prompt += "Examples:\n\n"
            for example in self.examples:
                prompt += f"Problem: {example['problem']}\n"
                prompt += "Reasoning:\n"
                for step in example["steps"]:
                    prompt += f"- {step}\n"
                prompt += f"Answer: {example['answer']}\n\n"
        
        prompt += f"Problem: {problem}\n\nReasoning:\n"
        return prompt
    
    def _parse_reasoning(self, response: str) -> Dict:
        """Parse reasoning chain from response."""
        lines = response.strip().split("\n")
        steps = []
        answer = ""
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("-", "•", "Step", "1.", "2.", "3.")):
                steps.append(stripped)
            elif "answer" in stripped.lower() or "conclusion" in stripped.lower():
                parts = stripped.split(":", 1)
                if len(parts) > 1:
                    answer = parts[1].strip()
        
        if not answer and lines:
            answer = lines[-1]
        
        return {"steps": steps, "answer": answer}


class ZeroShotCoT:
    """Zero-shot Chain of Thought using magic phrase."""
    
    def __init__(self, llm):
        self.llm = llm
        self.trigger_phrase = "Let's think step by step."
    
    async def solve(self, problem: str) -> str:
        prompt = f"{problem}\n{self.trigger_phrase}"
        return await self.llm.complete(prompt)
```

### CoT with Verification

```python
class VerifiedCoT:
    """Chain of Thought with self-verification."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def solve_with_verification(self, problem: str) -> Dict:
        reasoning_result = await self._cot_reason(problem)
        
        verification = await self._verify_reasoning(problem, reasoning_result)
        
        if not verification["correct"]:
            refined = await self._refine_reasoning(problem, reasoning_result, verification)
            return {
                "answer": refined["answer"],
                "reasoning": refined["steps"],
                "verification": verification["issues"],
                "refined": True
            }
        
        return {
            "answer": reasoning_result["answer"],
            "reasoning": reasoning_result["steps"],
            "verification": "passed",
            "refined": False
        }
    
    async def _verify_reasoning(self, problem: str, reasoning: Dict) -> Dict:
        prompt = f"""
        Problem: {problem}
        Proposed solution: {reasoning['answer']}
        Reasoning: {reasoning['steps']}
        
        Verify each step. Are there any logical errors or inconsistencies?
        
        Return JSON:
        {{
            "correct": boolean,
            "issues": ["list of errors if any"],
            "confidence": 0-10
        }}
        """
        return await self.llm.complete_json(prompt)
```

---

## ReAct Pattern

ReAct interleaves reasoning and action taking for interactive tasks.

### ReAct Agent

```python
class ReActAgent:
    """Reasoning + Acting agent."""
    
    def __init__(self, llm, tools: Dict[str, callable], max_iterations: int = 10):
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations
        self.thought_history: List[str] = []
        self.action_history: List[Dict] = []
    
    async def execute(self, task: str) -> Dict[str, Any]:
        """Execute task using ReAct pattern."""
        context = f"Task: {task}\n"
        
        for i in range(self.max_iterations):
            thought, action = await self._think_and_act(context)
            
            self.thought_history.append(thought)
            
            if action["type"] == "finish":
                return {
                    "answer": action["content"],
                    "thoughts": self.thought_history,
                    "actions": self.action_history,
                    "iterations": i + 1
                }
            
            result = await self._execute_tool(action)
            self.action_history.append({"action": action, "result": result})
            
            context += f"Thought: {thought}\n"
            context += f"Action: {action['tool']}({action.get('args', {})})\n"
            context += f"Observation: {result}\n"
        
        return {
            "answer": None,
            "thoughts": self.thought_history,
            "actions": self.action_history,
            "iterations": self.max_iterations,
            "termination_reason": "max_iterations"
        }
    
    async def _think_and_act(self, context: str) -> Tuple[str, Dict]:
        """Generate thought and decide action."""
        prompt = f"""
        {context}
        
        Think about what to do next. Then choose an action.
        
        Available tools: {list(self.tools.keys())}
        
        Format:
        Thought: [your reasoning]
        Action: [tool_name]
        Action Input: {{"arg": "value"}}
        
        Or to finish:
        Thought: [final reasoning]
        Action: finish
        Action Input: {{"answer": "final answer"}}
        """
        
        response = await self.llm.complete(prompt)
        return self._parse_thought_action(response)
    
    def _parse_thought_action(self, response: str) -> Tuple[str, Dict]:
        """Parse thought and action from response."""
        lines = response.strip().split("\n")
        thought = ""
        action = {"type": "finish", "content": response}
        
        for line in lines:
            if line.startswith("Thought:"):
                thought = line[len("Thought:"):].strip()
            elif line.startswith("Action:"):
                action_str = line[len("Action:"):].strip()
                if action_str.lower() == "finish":
                    action = {"type": "finish", "content": response}
                else:
                    action = {"type": "tool", "tool": action_str}
            elif line.startswith("Action Input:"):
                try:
                    import json
                    args = json.loads(line[len("Action Input:"):].strip())
                    if isinstance(action, dict) and "tool" in action:
                        action["args"] = args
                except:
                    pass
        
        return thought, action
    
    async def _execute_tool(self, action: Dict) -> str:
        """Execute the chosen tool."""
        tool_name = action.get("tool")
        if tool_name not in self.tools:
            return f"Error: Unknown tool {tool_name}"
        
        try:
            result = await self.tools[tool_name](**action.get("args", {}))
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
```

---

## Plan-and-Solve

Plan-and-Solve separates planning from execution for complex multi-step tasks.

### Plan-and-Solve Agent

```python
class PlanAndSolveAgent:
    """Agent that separates planning and execution phases."""
    
    def __init__(self, llm, tools: Dict[str, callable]):
        self.llm = llm
        self.tools = tools
    
    async def execute(self, task: str) -> Dict[str, Any]:
        """Execute task using plan-and-solve."""
        plan = await self._create_plan(task)
        
        execution_results = []
        for step in plan["steps"]:
            result = await self._execute_step(step, execution_results)
            execution_results.append({
                "step": step,
                "result": result
            })
            
            if self._should_replan(result):
                new_plan = await self._replan(task, execution_results)
                plan = new_plan
                execution_results = []
                continue
        
        final_answer = await self._synthesize_answer(task, execution_results)
        
        return {
            "plan": plan,
            "execution_results": execution_results,
            "final_answer": final_answer
        }
    
    async def _create_plan(self, task: str) -> Dict:
        """Create execution plan."""
        prompt = f"""
        Task: {task}
        Available tools: {list(self.tools.keys())}
        
        Create a step-by-step plan to complete this task.
        
        Return JSON:
        {{
            "steps": ["step 1", "step 2", ...],
            "rationale": "why this plan",
            "estimated_steps": 5
        }}
        """
        return await self.llm.complete_json(prompt)
    
    async def _execute_step(self, step: str, previous_results: List[Dict]) -> str:
        """Execute a single plan step."""
        context = "\n".join([
            f"Step {i+1}: {r['step']}\nResult: {r['result']}"
            for i, r in enumerate(previous_results)
        ])
        
        prompt = f"""
        {context}
        
        Current step: {step}
        Tools available: {list(self.tools.keys())}
        
        Execute this step and provide the result.
        """
        return await self.llm.complete(prompt)
    
    def _should_replan(self, result: str) -> bool:
        """Check if result indicates need for replanning."""
        error_indicators = ["error", "failed", "cannot", "unable", "missing"]
        return any(ind in result.lower() for ind in error_indicators)
    
    async def _replan(self, original_task: str, previous_results: List[Dict]) -> Dict:
        """Create new plan based on current progress."""
        failed_steps = [r for r in previous_results if self._should_replan(r["result"])]
        
        prompt = f"""
        Original task: {original_task}
        Failed steps: {failed_steps}
        
        Create an adjusted plan that works around the failures.
        """
        return await self.llm.complete_json(prompt)
    
    async def _synthesize_answer(self, task: str, results: List[Dict]) -> str:
        """Synthesize final answer from execution results."""
        prompt = f"""
        Task: {task}
        
        Execution results:
        {json.dumps(results, indent=2)}
        
        Synthesize a final answer based on all results.
        """
        return await self.llm.complete(prompt)
```

---

## Few-Shot Prompting Strategies

Effective few-shot examples guide model behavior through demonstration.

### Dynamic Example Selection

```python
class FewShotSelector:
    """Select optimal few-shot examples for a given task."""
    
    def __init__(self, examples: List[Dict], embedder=None):
        self.examples = examples
        self.embedder = embedder
    
    def select(
        self,
        query: str,
        n: int = 3,
        diversity: bool = True
    ) -> List[Dict]:
        """Select most relevant examples."""
        if self.embedder:
            query_emb = self.embedder(query)
            scored = [
                (self._similarity(query_emb, self.embedder(ex["input"])), ex)
                for ex in self.examples
            ]
            scored.sort(key=lambda x: x[0], reverse=True)
            selected = [ex for _, ex in scored[:n]]
        else:
            selected = self.examples[:n]
        
        if diversity:
            selected = self._ensure_diversity(selected, n)
        
        return selected
    
    def _ensure_diversity(self, selected: List[Dict], n: int) -> List[Dict]:
        """Ensure selected examples are diverse."""
        if len(selected) <= 1:
            return selected
        
        diverse = [selected[0]]
        for candidate in selected[1:]:
            if len(diverse) >= n:
                break
            diverse.append(candidate)
        return diverse
    
    @staticmethod
    def _similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class FewShotPromptBuilder:
    """Build few-shot prompts with optimal examples."""
    
    def __init__(self, selector: FewShotSelector):
        self.selector = selector
    
    def build(self, task: str, query: str, n: int = 3) -> str:
        examples = self.selector.select(query, n=n)
        
        prompt = ""
        for i, ex in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Input: {ex['input']}\n"
            prompt += f"Output: {ex['output']}\n\n"
        
        prompt += f"Now complete this task:\nInput: {query}\nOutput:"
        return prompt
```

---

## Tree of Thoughts

Tree of Thoughts explores multiple reasoning paths simultaneously.

### ToT Implementation

```python
class ToTNode:
    def __init__(self, thought: str, parent=None, depth: int = 0):
        self.thought = thought
        self.parent = parent
        self.children: List['ToTNode'] = []
        self.depth = depth
        self.value: float = 0.0
        self.visits: int = 0
    
    def uct(self, exploration: float = 1.41) -> float:
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration * (2 * (self.parent.visits if self.parent else 0) / self.visits) ** 0.5


class TreeOfThoughts:
    """Tree of Thoughts reasoning agent."""
    
    def __init__(self, llm, max_depth: int = 3, branching_factor: int = 3):
        self.llm = llm
        self.max_depth = max_depth
        self.branching_factor = branching_factor
    
    async def solve(self, problem: str) -> Dict:
        """Solve problem using tree search over thoughts."""
        root = ToTNode(thought=f"Problem: {problem}", depth=0)
        
        for depth in range(self.max_depth):
            leaves = self._get_leaves(root)
            
            for leaf in leaves:
                if self._is_solution(leaf):
                    return self._extract_solution(leaf)
                
                candidates = await self._generate_thoughts(leaf, problem)
                for thought in candidates[:self.branching_factor]:
                    child = ToTNode(thought=thought, parent=leaf, depth=depth + 1)
                    leaf.children.append(child)
                    
                    value = await self._evaluate_thought(thought, problem)
                    child.value = value
                    child.visits = 1
        
        best_leaf = max(self._get_leaves(root), key=lambda n: n.value, default=root)
        return {"solution": best_leaf.thought, "confidence": best_leaf.value}
    
    async def _generate_thoughts(self, node: ToTNode, problem: str) -> List[str]:
        prompt = f"""
        Problem: {problem}
        Current reasoning: {node.thought}
        
        Generate {self.branching_factor} possible next thoughts to progress.
        Return as JSON array of strings.
        """
        result = await self.llm.complete_json(prompt)
        return result if isinstance(result, list) else []
    
    async def _evaluate_thought(self, thought: str, problem: str) -> float:
        prompt = f"Rate this reasoning step 1-10 for problem '{problem}':\n{thought}\nScore:"
        try:
            return float(await self.llm.complete(prompt))
        except:
            return 5.0
    
    def _get_leaves(self, node: ToTNode) -> List[ToTNode]:
        if not node.children:
            return [node]
        return [leaf for child in node.children for leaf in self._get_leaves(child)]
    
    def _is_solution(self, node: ToTNode) -> bool:
        return "answer:" in node.thought.lower() or "solution:" in node.thought.lower()
    
    def _extract_solution(self, node: ToTNode) -> Dict:
        return {"solution": node.thought, "confidence": node.value}
```

---

## Constitutional AI

Constitutional AI guides model behavior through explicit principles.

### Constitutional Agent

```python
class ConstitutionalPrinciple:
    def __init__(self, name: str, description: str, weight: float = 1.0):
        self.name = name
        self.description = description
        self.weight = weight


class ConstitutionalAgent:
    """Agent guided by constitutional principles."""
    
    def __init__(self, llm, principles: List[ConstitutionalPrinciple]):
        self.llm = llm
        self.principles = principles
    
    async def generate(self, prompt: str) -> str:
        """Generate response respecting constitutional principles."""
        response = await self.llm.complete(prompt)
        
        for principle in self.principles:
            critique = await self._critique(response, principle)
            if critique["violates"]:
                revision = await self._revise(response, critique, principle)
                response = revision
        
        return response
    
    async def _critique(self, response: str, principle: ConstitutionalPrinciple) -> Dict:
        prompt = f"""
        Principle: {principle.description}
        Response: {response}
        
        Does this response violate the principle?
        Return JSON: {{"violates": boolean, "reasoning": "..."}}
        """
        return await self.llm.complete_json(prompt)
    
    async def _revise(self, response: str, critique: Dict, principle: ConstitutionalPrinciple) -> str:
        prompt = f"""
        Original response: {response}
        Principle: {principle.description}
        Violation: {critique['reasoning']}
        
        Revise the response to comply with the principle while preserving meaning.
        """
        return await self.llm.complete(prompt)
```

---

## Multi-Modal Agent Design

Agents that process and reason across text, image, audio, and other modalities.

### Multi-Modal Agent

```python
from abc import ABC, abstractmethod
from typing import Union
from PIL import Image
import numpy as np

class ModalityHandler(ABC):
    @abstractmethod
    def process(self, input_data) -> str:
        pass

class TextHandler(ModalityHandler):
    def process(self, input_data: str) -> str:
        return input_data

class ImageHandler(ModalityHandler):
    def __init__(self, vision_model):
        self.model = vision_model
    
    def process(self, input_data: Image.Image) -> str:
        return self.model.describe(input_data)

class AudioHandler(ModalityHandler):
    def __init__(self, transcriber):
        self.transcriber = transcriber
    
    def process(self, input_data: bytes) -> str:
        return self.transcriber(input_data)


class MultiModalAgent:
    """Agent handling multiple input modalities."""
    
    def __init__(self, llm, handlers: Dict[str, ModalityHandler]):
        self.llm = llm
        self.handlers = handlers
    
    async def execute(self, inputs: Dict[str, Any]) -> str:
        """Process multi-modal inputs."""
        processed = {}
        for modality, handler in self.handlers.items():
            if modality in inputs:
                processed[modality] = handler.process(inputs[modality])
        
        prompt = self._build_multimodal_prompt(processed)
        return await self.llm.complete(prompt)
    
    def _build_multimodal_prompt(self, processed_inputs: Dict) -> str:
        prompt = ""
        if "text" in processed_inputs:
            prompt += f"Text: {processed_inputs['text']}\n"
        if "image" in processed_inputs:
            prompt += f"Image description: {processed_inputs['image']}\n"
        if "audio" in processed_inputs:
            prompt += f"Audio transcript: {processed_inputs['audio']}\n"
        return prompt
```

---

## Agent Communication Protocols

Standardized protocols for agent-to-agent communication.

### Message Protocol

```python
from dataclasses import dataclass
from typing import Any, Dict, Optional
from enum import Enum
import uuid

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"

@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: MessageType
    payload: Dict[str, Any]
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    ttl: int = 300
    
    def is_expired(self) -> bool:
        return time.time() - self.timestamp > self.ttl
    
    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.message_type.value,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp
        }


class MessageBus:
    """Message bus for agent communication."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = {}
        self.message_queue: List[AgentMessage] = []
    
    def subscribe(self, agent_id: str, handler: callable):
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(handler)
    
    def publish(self, message: AgentMessage):
        if message.is_expired():
            return
        self.message_queue.append(message)
    
    def dispatch(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            handlers = self.subscribers.get(message.receiver, [])
            for handler in handlers:
                try:
                    handler(message)
                except Exception as e:
                    logger.error(f"Handler error: {e}")
```

---

## Hierarchical Agent Systems

Organize agents in hierarchies for complex organizational structures.

### Hierarchical Agent

```python
class HierarchicalAgent:
    """Agent that can delegate to sub-agents."""
    
    def __init__(self, name: str, llm, sub_agents: Dict[str, 'HierarchicalAgent'] = None):
        self.name = name
        self.llm = llm
        self.sub_agents = sub_agents or {}
        self.capabilities: List[str] = []
    
    def add_sub_agent(self, name: str, agent: 'HierarchicalAgent'):
        self.sub_agents[name] = agent
    
    async def execute(self, task: str) -> Dict:
        """Execute task, delegating to sub-agents if needed."""
        if self._can_handle(task):
            return await self._execute_directly(task)
        
        subtasks = await self._decompose_for_sub_agents(task)
        results = {}
        
        for subtask in subtasks:
            agent_name = subtask["agent"]
            if agent_name in self.sub_agents:
                result = await self.sub_agents[agent_name].execute(subtask["task"])
                results[agent_name] = result
        
        return await self._synthesize(task, results)
    
    def _can_handle(self, task: str) -> bool:
        """Check if this agent can handle the task directly."""
        return not self.sub_agents or len(self.sub_agents) == 0
    
    async def _decompose_for_sub_agents(self, task: str) -> List[Dict]:
        prompt = f"""
        Task: {task}
        Available sub-agents: {list(self.sub_agents.keys())}
        
        Break down task and assign to appropriate sub-agents.
        Return JSON list: [{{"agent": "name", "task": "description"}}]
        """
        return await self.llm.complete_json(prompt)
    
    async def _synthesize(self, original_task: str, results: Dict) -> Dict:
        prompt = f"""
        Original task: {original_task}
        Sub-agent results: {json.dumps(results)}
        
        Synthesize final result.
        """
        return {"result": await self.llm.complete(prompt), "sub_results": results}
```

---

## Self-Ask and Search

Self-Ask breaks complex questions into simpler sub-questions.

### Self-Ask Agent

```python
class SelfAskAgent:
    """Agent that decomposes questions into sub-questions."""
    
    def __init__(self, llm, search_tool: callable = None):
        self.llm = llm
        self.search_tool = search_tool
    
    async def answer(self, question: str) -> Dict:
        """Answer question by decomposing into sub-questions."""
        decomposition = await self._decompose(question)
        
        answers = {}
        for sub_q in decomposition["sub_questions"]:
            if sub_q.startswith("yes/no") or sub_q.startswith("Is ") or sub_q.startswith("Are "):
                answers[sub_q] = await self._answer_direct(sub_q)
            elif self.search_tool and self._should_search(sub_q):
                answers[sub_q] = await self.search_tool(sub_q)
            else:
                answers[sub_q] = await self._answer_direct(sub_q)
        
        final_answer = await self._compose_answer(question, decomposition, answers)
        
        return {
            "question": question,
            "sub_questions": decomposition["sub_questions"],
            "answers": answers,
            "final_answer": final_answer
        }
    
    async def _decompose(self, question: str) -> Dict:
        prompt = f"""
        Question: {question}
        
        Break this into simpler sub-questions. Mark factual questions with "search:" prefix.
        
        Return JSON:
        {{
            "sub_questions": ["q1", "q2", ...]
        }}
        """
        return await self.llm.complete_json(prompt)
    
    def _should_search(self, question: str) -> bool:
        search_keywords = ["what is", "who is", "when did", "where is", "how many"]
        return any(kw in question.lower() for kw in search_keywords)
    
    async def _answer_direct(self, question: str) -> str:
        """Answer question directly with LLM."""
        return await self.llm.complete(question)
    
    async def _compose_answer(self, original: str, decomposition: Dict, answers: Dict) -> str:
        prompt = f"""
        Original question: {original}
        Sub-questions and answers:
        {json.dumps(answers, indent=2)}
        
        Compose a final answer.
        """
        return await self.llm.complete(prompt)
```

---

## Automatic Prompt Engineering

Use LLMs to automatically optimize prompts.

### APE Implementation

```python
class AutomaticPromptEngineer:
    """Automatically optimize prompts using LLM."""
    
    def __init__(self, llm, eval_fn: callable):
        self.llm = llm
        self.eval_fn = eval_fn
    
    async def optimize(
        self,
        base_prompt: str,
        training_inputs: List[str],
        training_outputs: List[str],
        generations: int = 5,
        population_size: int = 8
    ) -> str:
        """Optimize prompt through evolutionary search."""
        population = await self._seed_population(base_prompt, population_size)
        
        for gen in range(generations):
            scores = []
            for prompt in population:
                score = await self._evaluate_prompt(prompt, training_inputs, training_outputs)
                scores.append((score, prompt))
            
            scores.sort(key=lambda x: x[0], reverse=True)
            best_score, best_prompt = scores[0]
            
            if best_score > 0.95:
                return best_prompt
            
            population = await self._evolve_population(scores, population_size)
        
        return best_prompt
    
    async def _seed_population(self, base_prompt: str, size: int) -> List[str]:
        prompt = f"""
        Base prompt: {base_prompt}
        
        Generate {size} variations of this prompt that might improve performance.
        Return as JSON array of strings.
        """
        result = await self.llm.complete_json(prompt)
        return [base_prompt] + (result if isinstance(result, list) else [base_prompt] * (size - 1))
    
    async def _evaluate_prompt(self, prompt: str, inputs: List[str], outputs: List[str]) -> float:
        correct = 0
        for inp, expected in zip(inputs, outputs):
            response = await self.llm.complete(f"{prompt}\n\nInput: {inp}\nOutput:")
            if self.eval_fn(response, expected):
                correct += 1
        return correct / len(inputs) if inputs else 0
    
    async def _evolve_population(self, scored: List[Tuple[float, str]], size: int) -> List[str]:
        top_performers = [p for _, p in scored[:max(2, size // 4)]]
        
        prompt = f"""
        Current best prompts:
        {chr(10).join(f'- {p}' for p in top_performers)}
        
        Generate {size - len(top_performers)} new variations combining and improving these.
        Return as JSON array.
        """
        new_variations = await self.llm.complete_json(prompt)
        
        return top_performers + (new_variations if isinstance(new_variations, list) else [])
```

---

## Retrieval-Augmented Generation

RAG enhances LLM outputs with external knowledge retrieval.

### Advanced RAG Pipeline

```python
class AdvancedRAGPipeline:
    """Production-grade RAG with hybrid retrieval and reranking."""
    
    def __init__(self, vector_store, llm, reranker=None):
        self.vector_store = vector_store
        self.llm = llm
        self.reranker = reranker
    
    async def query(self, question: str, top_k: int = 5) -> Dict:
        """Execute full RAG pipeline."""
        query_embedding = self._embed(question)
        
        hybrid_results = self._hybrid_retrieve(question, query_embedding, top_k * 3)
        
        if self.reranker:
            reranked = await self.reranker.rerank(question, hybrid_results)
            contexts = reranked[:top_k]
        else:
            contexts = hybrid_results[:top_k]
        
        prompt = self._build_prompt(question, contexts)
        answer = await self.llm.complete(prompt)
        
        return {
            "answer": answer,
            "sources": contexts,
            "confidence": self._calculate_confidence(contexts)
        }
    
    def _hybrid_retrieve(self, question: str, embedding: np.ndarray, top_k: int) -> List[Dict]:
        """Combine vector and keyword search."""
        vector_results = self.vector_store.search(embedding, top_k=top_k)
        keyword_results = self.vector_store.keyword_search(question, top_k=top_k)
        
        seen = set()
        combined = []
        for result in vector_results + keyword_results:
            if result["id"] not in seen:
                seen.add(result["id"])
                combined.append(result)
        
        return combined
    
    def _build_prompt(self, question: str, contexts: List[Dict]) -> str:
        context_text = "\n\n".join([
            f"[{i+1}] {c['content']}"
            for i, c in enumerate(contexts)
        ])
        return f"""
        Context:
        {context_text}
        
        Question: {question}
        
        Answer based on the context above. Cite sources with [1], [2], etc.
        If the context doesn't contain the answer, say so explicitly.
        """
    
    def _calculate_confidence(self, contexts: List[Dict]) -> float:
        if not contexts:
            return 0.0
        scores = [c.get("score", 0.0) for c in contexts[:3]]
        return sum(scores) / len(scores)
```

---

## Tool Composition and Abstraction

Build complex tools from simpler primitives.

### Tool Composition Framework

```python
class ComposableTool:
    """Tool that composes other tools."""
    
    def __init__(self, name: str, tools: List[callable], composition_fn: callable):
        self.name = name
        self.tools = {t.__name__: t for t in tools}
        self.compose = composition_fn
    
    async def execute(self, **kwargs) -> Any:
        results = {}
        for tool_name, tool in self.tools.items():
            if tool_name in kwargs.get("required_tools", []):
                results[tool_name] = await tool(**kwargs.get(tool_name, {}))
        return self.compose(results)


class ToolRegistry:
    """Registry for tool composition and discovery."""
    
    def __init__(self):
        self.tools: Dict[str, callable] = {}
        self.compositions: Dict[str, ComposableTool] = {}
    
    def register(self, name: str, tool: callable):
        self.tools[name] = tool
        return self
    
    def compose(self, name: str, tool_names: List[str], composition_fn: callable):
        tools = [self.tools[t] for t in tool_names if t in self.tools]
        self.compositions[name] = ComposableTool(name, tools, composition_fn)
        return self
    
    def get(self, name: str) -> callable:
        if name in self.compositions:
            return self.compositions[name].execute
        return self.tools.get(name)
```

---

## Stateful vs Stateless Agents

Understanding when to use stateful or stateless designs.

### Stateful Agent

```python
class StatefulAgent:
    """Maintains state across interactions."""
    
    def __init__(self, state_store: callable):
        self.state_store = state_store
    
    async def execute(self, session_id: str, input_data: str) -> str:
        state = await self.state_store.get(session_id)
        
        updated_input = self._merge_with_history(input_data, state)
        response = await self.llm.complete(updated_input)
        
        await self.state_store.update(session_id, {
            "last_input": input_data,
            "last_output": response,
            "history": state.get("history", []) + [{"input": input_data, "output": response}]
        })
        
        return response
```

### Stateless Agent

```python
class StatelessAgent:
    """No persistent state - pure function style."""
    
    async def execute(self, input_data: str, context: Dict = None) -> str:
        prompt = self._build_prompt(input_data, context)
        return await self.llm.complete(prompt)
    
    def _build_prompt(self, input_data: str, context: Dict = None) -> str:
        if context:
            return f"Context:\n{context}\n\nQuery: {input_data}"
        return input_data
```

---

## Evaluation and Benchmarking

Systematic evaluation of agent and LLM performance.

### Evaluation Framework

```python
class AgentEvaluator:
    """Comprehensive agent evaluation framework."""
    
    def __init__(self, agent, metrics: List[str] = None):
        self.agent = agent
        self.metrics = metrics or ["accuracy", "latency", "cost", "safety"]
    
    async def evaluate(self, test_cases: List[Dict]) -> Dict:
        results = {metric: [] for metric in self.metrics}
        
        for case in test_cases:
            start = time.time()
            response = await self.agent.execute(case["input"])
            latency = time.time() - start
            
            if "accuracy" in self.metrics:
                results["accuracy"].append(
                    self._score_accuracy(response, case["expected"])
                )
            if "latency" in self.metrics:
                results["latency"].append(latency)
            if "cost" in self.metrics:
                results["cost"].append(self._estimate_cost(case["input"], response))
            if "safety" in self.metrics:
                results["safety"].append(self._check_safety(response))
        
        return self._aggregate_results(results)
    
    def _aggregate_results(self, results: Dict) -> Dict:
        aggregated = {}
        for metric, scores in results.items():
            if scores:
                aggregated[f"{metric}_mean"] = sum(scores) / len(scores)
                aggregated[f"{metric}_min"] = min(scores)
                aggregated[f"{metric}_max"] = max(scores)
                if len(scores) > 1:
                    aggregated[f"{metric}_std"] = (sum((s - aggregated[f"{metric}_mean"]) ** 2 for s in scores) / (len(scores) - 1)) ** 0.5
        return aggregated
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Troubleshooting](./troubleshooting.md)
