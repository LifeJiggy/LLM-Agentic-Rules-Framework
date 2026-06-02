# Core Domain - Troubleshooting

## Overview

This document covers common issues and their solutions for LLM/agentic systems.

## Common Issues and Solutions

### Issue 1: Agent Producing Low-Quality Output

**Symptoms:**
- Responses are vague or incomplete
- Code has bugs
- Instructions are not followed

**Possible Causes:**
- Prompt is too vague
- Not enough context provided
- Token limits causing truncation

**Solutions:**

1. **Refine the prompt:**
```python
# Before
prompt = "Write code"

# After
prompt = """
Write a Python function that:
1. Takes a list of integers
2. Returns only the even numbers
3. Maintains original order
4. Handles empty lists
"""
```

2. **Add constraints:**
```python
prompt = """
Write clean, production-ready code that:
- Includes type hints
- Has docstrings
- Handles edge cases
- Includes error handling
"""
```

3. **Use few-shot examples:**
```python
prompt = """
Classify sentiment:

Input: "Great product!"
Output: Positive

Input: "Not worth the money"
Output: Negative

Input: "It was okay"
Output: ___
"""
```

### Issue 2: Context Window Overflow

**Symptoms:**
- Responses get cut off
- Errors about token limits
- Incomplete outputs

**Solutions:**

1. **Implement token budget management:**
```python
class TokenBudget:
    def __init__(self, max_tokens=4000):
        self.max_tokens = max_tokens
        self.used = 0
    
    def reserve(self, tokens):
        if self.used + tokens > self.max_tokens:
            raise TokenLimitError("Budget exceeded")
        self.used += tokens
```

2. **Trim conversation history:**
```python
def trim_history(messages, max_tokens):
    while calculate_tokens(messages) > max_tokens:
        # Remove oldest non-system message
        messages.pop(1)  # Keep system prompt at index 0
    return messages
```

3. **Summarize old context:**
```python
async def summarize_old_messages(messages):
    summary = await llm.summarize(messages[:-5])
    return [messages[0]] + [{"role": "system", "content": summary}] + messages[-5:]
```

### Issue 3: Agent Loop Not Converging

**Symptoms:**
- Agent keeps iterating without progress
- Results keep getting modified
- No end condition reached

**Solutions:**

1. **Set maximum iterations:**
```python
MAX_ITERATIONS = 5

for i in range(MAX_ITERATIONS):
    result = agent.execute(task)
    if is_satisfactory(result):
        return result
    task = f"Refine: {result}"
    
raise ConvergenceError("Agent did not converge")
```

2. **Track state changes:**
```python
class StateTracker:
    def __init__(self):
        self.history = []
    
    def has_improved(self, new_result):
        score = calculate_score(new_result)
        improved = not self.history or score > max(self.history)
        self.history.append(score)
        return improved
```

3. **Define clear success criteria:**
```python
def is_satisfactory(result):
    return (
        result.get("score", 0) >= 0.8 and
        result.get("errors", []) == [] and
        result.get("completeness", 0) >= 1.0
    )
```

### Issue 4: Inconsistent Responses

**Symptoms:**
- Different outputs for same input
- Unpredictable behavior
- Hard to reproduce results

**Solutions:**

1. **Fix temperature settings:**
```python
# For consistent, deterministic output
response = llm.complete(prompt, temperature=0)

# For creative but controlled output
response = llm.complete(prompt, temperature=0.7)
```

2. **Include output schema:**
```python
prompt = """
Respond in this exact JSON format:
{
  "status": "success|error",
  "data": {...},
  "message": "string"
}
"""
```

3. **Seed random for reproducibility:**
```python
response = llm.complete(prompt, seed=42)
```

### Issue 5: Tool Execution Failures

**Symptoms:**
- Tools return errors
- Chain stops working
- Partial results

**Solutions:**

1. **Implement error handling:**
```python
async def execute_tool_chain(tools):
    results = []
    for tool in tools:
        try:
            result = await tool.execute()
            results.append({"tool": tool.name, "result": result})
        except ToolError as e:
            results.append({"tool": tool.name, "error": str(e)})
            # Continue with other tools
    return results
```

2. **Add fallback tools:**
```python
async def fetch_data():
    try:
        return await primary_source.fetch()
    except Exception:
        return await fallback_source.fetch()
```

3. **Implement circuit breaker:**
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5):
        self.failures = 0
        self.threshold = failure_threshold
        self.state = "closed"
    
    def call(self, func):
        if self.state == "open":
            raise CircuitOpenError()
        
        try:
            result = func()
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
            raise
```

### Issue 6: State Management Issues

**Symptoms:**
- Data leaks between sessions
- Unexpected side effects
- Race conditions

**Solutions:**

1. **Use immutable state:**
```python
# Before - mutable
def process(state, data):
    state["results"].append(data)
    return state

# After - immutable
def process(state, data):
    new_state = {**state, "results": state["results"] + [data]}
    return new_state
```

2. **Isolate contexts:**
```python
class IsolatedContext:
    def __init__(self):
        self._data = {}
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def set(self, key, value):
        # Create new context instead of mutating
        new_context = IsolatedContext()
        new_context._data = {**self._data, key: value}
        return new_context
```

### Issue 7: Performance Problems

**Symptoms:**
- Slow response times
- High resource usage
- Timeouts

**Solutions:**

1. **Cache common operations:**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_prompt_template(task_type):
    # Expensive operation - now cached
    return load_template(task_type)
```

2. **Use async operations:**
```python
async def process_tasks(tasks):
    return await asyncio.gather(*[process(t) for t in tasks])
```

3. **Optimize token usage:**
```python
def optimize_prompt(prompt):
    # Remove redundancy
    prompt = prompt.strip()
    prompt = " ".join(prompt.split())  # Normalize whitespace
    return prompt
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
