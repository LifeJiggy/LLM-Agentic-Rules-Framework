# Testing Domain - Troubleshooting

## Overview

This document provides comprehensive troubleshooting guidance for common testing issues in LLM/agentic systems. Each section covers symptoms, root causes, and step-by-step solutions.

## Table of Contents

1. [Flaky Tests and Non-Determinism](#flaky-tests-and-non-determinism)
2. [Slow Test Execution](#slow-test-execution)
3. [Test Timeouts](#test-timeouts)
4. [Memory Leaks in Test Suites](#memory-leaks-in-test-suites)
5. [Rate Limiting Errors](#rate-limiting-errors)
6. [API Quota Exhaustion](#api-quota-exhaustion)
7. [Context Window Overflow](#context-window-overflow)
8. [Token Limit Exceeded](#token-limit-exceeded)
9. [Hallucination Causing False Failures](#hallucination-causing-false-failures)
10. [Semantic Assertion Failures](#semantic-assertion-failures)
11. [Golden Dataset Drift](#golden-dataset-drift)
12. [Mock Data Becoming Stale](#mock-data-becoming-stale)
13. [CI/CD Pipeline Failures](#cicd-pipeline-failures)
14. [Coverage Reporting Issues](#coverage-reporting-issues)
15. [Agent Infinite Loops in Tests](#agent-infinite-loops-in-tests)
16. [Tool Call Mocking Difficulties](#tool-call-mocking-difficulties)
17. [Streaming Test Instability](#streaming-test-instability)
18. [Multi-Turn State Leakage Between Tests](#multi-turn-state-leakage-between-tests)
19. [Database and Fixture Pollution](#database-and-fixture-pollution)
20. [Network-Dependent Tests Failing](#network-dependent-tests-failing)
21. [Cost Overruns in Test Execution](#cost-overruns-in-test-execution)
22. [Model Version Differences Causing Test Failures](#model-version-differences-causing-test-failures)
23. [Embedding Drift](#embedding-drift)
24. [Prompt Template Rendering Errors](#prompt-template-rendering-errors)
25. [Fixture Setup and Teardown Issues](#fixture-setup-and-teardown-issues)
26. [Parallel Test Conflicts](#parallel-test-conflicts)
27. [Secrets Management in Tests](#secrets-management-in-tests)
28. [Cross-Platform Test Failures](#cross-platform-test-failures)
29. [Unicode and Encoding Issues](#unicode-and-encoding-issues)
30. [Large Context Test Failures](#large-context-test-failures)
31. [RAG Retrieval Inconsistency](#rag-retrieval-inconsistency)
32. [Human Evaluation Bottlenecks](#human-evaluation-bottlenecks)

---

## Flaky Tests and Non-Determinism

### Symptoms

- Tests pass and fail intermittently with no code changes
- Failure rate ~10-30%
- Failures often in LLM-related assertions
- Re-running passes the test

### Root Causes

1. Temperature > 0 producing variable outputs
2. No seed set for non-deterministic components
3. Assertions check exact text instead of properties
4. Rate limiting causing timeouts in CI
5. Shared state between tests

### Solutions

```python
# Solution 1: Use temperature=0 for deterministic tests
def test_deterministic():
    response = call_llm("What is 2+2?", temperature=0.0)
    assert "4" in response

# Solution 2: Property-based assertions for temp > 0
def test_stable_properties():
    for _ in range(5):
        response = call_llm("Summarize: text", temperature=0.7)
        assert "cat" in response.lower()
        assert len(response) > 20

# Solution 3: Statistical thresholds
def test_statistical():
    successes = sum(1 for _ in range(20) if "4" in call_llm("2+2?", temperature=0.0))
    assert successes >= 19, f"Only {successes}/20 succeeded"

# Solution 4: Log seeds for reproducibility
def test_with_seed_logging():
    seed = 42
    logger.info(f"Using seed: {seed}")
    response = call_llm("Test", seed=seed)
    assert response is not None
```

### Checklist

- [ ] Temperature=0 used for deterministic assertions
- [ ] Seeds logged for all non-zero temperature tests
- [ ] Assertions check properties, not exact text
- [ ] No shared state between tests
- [ ] Retries configured only for genuine non-determinism

---

## Slow Test Execution

### Symptoms

- Test suite takes > 30 minutes
- CI pipeline times out
- Developer feedback loop too slow
- Tests pass locally but time out in CI

### Root Causes

1. Calling real LLM API in unit tests
2. No mocking of external dependencies
3. Large golden datasets evaluated in CI
4. Sequential test execution
5. Heavy fixtures loaded for every test

### Solutions

```python
# Solution 1: Mock LLM in unit tests
@pytest.fixture
def mock_llm():
    client = MagicMock()
    client.generate.return_value = "Mocked response"
    return client

# Solution 2: Use cheaper models in CI
@pytest.fixture
def fast_llm():
    return LLMClient(model="gpt-3.5-turbo")  # Faster than gpt-4

# Solution 3: Limit golden dataset size in CI
@pytest.fixture
def ci_dataset():
    dataset = load_golden_dataset("regression.jsonl")
    yield dataset.sample(50, seed=42)  # Only 50 in CI, full in nightly

# Solution 4: Parallel execution
# pytest -n auto

# Solution 5: Split heavy and light tests
# Run fast tests in PR validation, heavy tests in nightly
```

### Optimization Checklist

- [ ] Unit tests use mocks (< 1s each)
- [ ] Integration tests < 5s each
- [ ] E2E tests run on deploy only
- [ ] Parallel execution enabled
- [ ] Heavy fixtures scoped to module/session
- [ ] Golden dataset sampled in CI

---

## Test Timeouts

### Symptoms

- Tests hang indefinitely
- CI jobs killed after timeout
- No error output, just timeout
- Intermittent hangs

### Root Causes

1. Agent infinite loops without max_iterations
2. LLM API hanging on network issues
3. Tool calls without timeouts
4. Streaming responses never completing
5. Deadlocks in multi-threaded tests

### Solutions

```python
# Solution 1: Set agent iteration limits
def test_with_loop_limit():
    agent = Agent(max_iterations=5)
    result = agent.run("Complex task")
    assert result.iterations <= 5

# Solution 2: Set explicit timeouts
def test_with_timeout():
    client = LLMClient(timeout=10)
    response = client.generate("Hello", timeout=10)
    assert response is not None

# Solution 3: Use pytest-timeout
@pytest.mark.timeout(30)
def test_with_pytest_timeout():
    response = call_llm("Hello")
    assert response is not None

# Solution 4: Add circuit breakers
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=3, reset_timeout=60)

def test_with_circuit_breaker():
    try:
        result = breaker.call(call_llm, "Hello")
    except CircuitBreakerOpen:
        pytest.skip("Circuit breaker open")
    assert result is not None
```

### Timeout Troubleshooting Steps

1. Add logging to identify where the test hangs
2. Run with `pytest --timeout=60 --timeout-method=thread`
3. Check for infinite loops in agent logic
4. Verify network connectivity in CI
5. Add explicit timeouts to all API calls
6. Use circuit breakers for external dependencies

---

## Memory Leaks in Test Suites

### Symptoms

- Memory usage grows during test run
- Tests pass individually but fail when run together
- System becomes unresponsive after running test suite
- OOM kills in CI

### Root Causes

1. Global state not reset between tests
2. Database connections not closed
3. LLM clients cached indefinitely
4. Large objects retained in memory
5. Circular references in fixtures

### Solutions

```python
# Solution 1: Proper fixture cleanup
@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.close()
    session.remove()

# Solution 2: Autouse cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_after_test():
    yield
    GlobalState.reset()
    clear_cache()
    gc.collect()

# Solution 3: Scope heavy fixtures
@pytest.fixture(scope="session")
def vector_index():
    index = VectorIndex()
    yield index
    index.cleanup()

# Solution 4: Monitor memory usage
import tracemalloc

def test_memory():
    tracemalloc.start()
    # ... test code ...
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 100_000_000, f"Peak memory {peak / 1e6:.1f}MB too high"
```

### Memory Monitoring

```bash
# Monitor memory in CI
python -m memory_profiler tests/test_suite.py

# Or use pytest plugin
pytest --memory
```

---

## Rate Limiting Errors

### Symptoms

- 429 Too Many Requests errors
- Tests fail only under CI load
- Inconsistent failures across runs
- `RateLimitError` or `QuotaExceeded` exceptions

### Root Causes

1. Too many tests hitting API simultaneously
2. No retry logic with backoff
3. Rate limit not configured
4. Parallel tests sharing API key quota
5. CI running full suite without throttling

### Solutions

```python
# Solution 1: Add retry with backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_llm_with_retry(prompt):
    return call_llm(prompt)

# Solution 2: Rate limit client
client = RateLimitedClient(
    rate_limit=10,  # requests per minute
    retry=True,
    backoff_factor=2
)

# Solution 3: Use separate API keys for parallel tests
# Solution 4: Throttle in CI
# pytest tests/ -n 4 --maxprocesses 4

# Solution 5: Use mocks in unit tests, real API in integration
```

### Rate Limit Prevention

```python
# conftest.py
@pytest.fixture(autouse=True)
def rate_limit_protection():
    if os.getenv("CI"):
        time.sleep(0.5)  # Throttle in CI
    yield
```

---

## API Quota Exhaustion

### Symptoms

- 402 Payment Required or quota exceeded errors
- Tests work locally but fail in CI
- Sudden test failures across all PRs
- API dashboard shows quota depleted

### Root Causes

1. Full test suite uses production API key
2. No cost controls on test execution
3. Expensive models (gpt-4) used in unit tests
4. Token budget not enforced
5. Tests run on every commit without throttling

### Solutions

```python
# Solution 1: Use cheaper models for most tests
@pytest.fixture
def llm_client():
    model = os.getenv("TEST_MODEL", "gpt-3.5-turbo")
    return LLMClient(model=model)

# Solution 2: Token budget enforcement
class TokenBudget:
    def __init__(self, limit):
        self.limit = limit
        self.used = 0
    
    def check(self, prompt, max_out=500):
        est = count_tokens(prompt) + max_out
        if self.used + est > self.limit:
            raise BudgetExceeded(f"Budget {self.used}/{self.limit}")
        return True

# Solution 3: Use dedicated test API key with lower quota
TEST_API_KEY = os.getenv("TEST_LLM_API_KEY")  # Separate from production

# Solution 4: Sample large datasets in CI
def test_with_sampling():
    dataset = load_golden_dataset("regression.jsonl")
    sample = dataset.sample(50)  # Only 50 in CI
    # ... test code ...

# Solution 5: Cache LLM responses in CI
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_call(prompt):
    return call_llm(prompt)
```

---

## Context Window Overflow

### Symptoms

- `TokenLimitExceeded` or `context_length_exceeded` errors
- Responses truncated unexpectedly
- Long prompts fail while short ones pass
- Error: "maximum context length"

### Root Causes

1. Context window not checked before API call
2. No prompt truncation logic
3. Conversation history growing unbounded
4. Multi-turn tests accumulating context
5. Golden dataset has very long inputs

### Solutions

```python
# Solution 1: Check context size before calling
def test_safe_context():
    tokenizer = Tokenizer(model="gpt-3.5-turbo")
    prompt = " ".join(["word"] * 5000)
    
    token_count = tokenizer.count(prompt)
    max_context = 4096
    
    if token_count > max_context:
        prompt = tokenizer.truncate(prompt, max_tokens=max_context - 100)
    
    response = call_llm(prompt)
    assert response is not None

# Solution 2: Implement context manager
class ContextManager:
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens
        self.messages = []
    
    def add(self, message):
        self.messages.append(message)
        while self.total_tokens() > self.max_tokens:
            self.messages.pop(0)  # Remove oldest
    
    def total_tokens(self):
        return sum(count_tokens(m["content"]) for m in self.messages)

# Solution 3: Enforce per-turn limits
@pytest.mark.parametrize("length", [100, 1000, 3000, 4000, 5000])
def test_context_handling(length):
    text = " ".join(["word"] * length)
    try:
        response = call_llm(text)
        assert response is not None
    except TokenLimitExceeded:
        if length < 4000:
            raise  # Shouldn't fail below limit

# Solution 4: Test boundary conditions
def test_context_boundaries():
    for size in [100, 1000, 3000, 4000, 4096, 5000, 10000]:
        text = " ".join(["word"] * size)
        try:
            response = call_llm(text, max_tokens=100)
        except TokenLimitExceeded:
            response = None
        # Record pass/fail for each boundary
```

---

## Token Limit Exceeded

### Symptoms

- Error: "This model's maximum context length is X"
- Requests with long inputs fail
- Inconsistent failures with varying input lengths
- Truncation not working as expected

### Root Causes

1. Input + output tokens exceed model limit
2. max_tokens not set or set too high
3. Tokenizer mismatch (using wrong model tokenizer)
4. System prompt consuming too many tokens
5. Conversation history not truncated

### Solutions

```python
# Solution 1: Account for system prompt + history + input
def calculate_total_tokens(system_prompt, history, user_input, max_output):
    tokenizer = Tokenizer(model="gpt-3.5-turbo")
    total = (
        tokenizer.count(system_prompt) +
        sum(tokenizer.count(m) for m in history) +
        tokenizer.count(user_input) +
        max_output
    )
    return total

def test_token_budget():
    system_prompt = "You are a helpful assistant."
    history = ["Previous message"] * 10
    user_input = " ".join(["word"] * 100)
    max_output = 500
    limit = 4096
    
    total = calculate_total_tokens(system_prompt, history, user_input, max_output)
    assert total <= limit, f"Total tokens {total} exceeds limit {limit}"

# Solution 2: Truncate history before calling
def truncate_history(history, max_tokens):
    tokenizer = Tokenizer()
    truncated = []
    current_tokens = 0
    
    for message in reversed(history):
        msg_tokens = tokenizer.count(message)
        if current_tokens + msg_tokens > max_tokens:
            break
        truncated.insert(0, message)
        current_tokens += msg_tokens
    
    return truncated

# Solution 3: Use models with larger context windows
# gpt-4-32k, claude-3-opus (200k), etc.
```

---

## Hallucination Causing False Failures

### Symptoms

- Tests fail because model produces plausible but incorrect answers
- Model "invents" facts not in the context
- Inconsistent factual responses across runs
- Factual queries return wrong answers despite temperature=0

### Root Causes

1. Model knowledge cutoff date
2. Training data limitations
3. Lack of grounding in provided context
4. Temperature causing variability
5. Ambiguous prompts leading to interpretation

### Solutions

```python
# Solution 1: Use grounded queries with RAG
def test_grounded_answer():
    context = {"documents": ["Python was created by Guido van Rossum in 1991."]}
    prompt = f"Context: {context}\nQuestion: Who created Python?"
    response = call_llm(prompt, temperature=0.0)
    assert "Guido" in response or "Rossum" in response

# Solution 2: Add verification step
def test_with_verification():
    answer = call_llm("What is the capital of France?", temperature=0.0)
    
    # Verify with second call
    verification_prompt = f"Is this true: {answer}. Answer yes or no."
    verification = call_llm(verification_prompt, temperature=0.0)
    
    assert "yes" in verification.lower(), f"Answer may be hallucinated: {answer}"

# Solution 3: Use well-known factual queries
def test_stable_facts():
    stable_facts = [
        ("What is 2+2?", "4"),
        ("What color is the sky?", "blue"),
        ("Who wrote Romeo and Juliet?", "Shakespeare")
    ]
    for question, expected in stable_facts:
        response = call_llm(question, temperature=0.0)
        assert expected.lower() in response.lower()

# Solution 4: Semantic similarity instead of exact match
def test_semantic_factual():
    expected = "The Earth orbits the Sun"
    response = call_llm("Does the Earth orbit the Sun?", temperature=0.0)
    similarity = semantic_similarity(response, expected)
    assert similarity >= 0.7
```

---

## Semantic Assertion Failures

### Symptoms

- Test fails because response is semantically correct but wording differs
- Similar responses fail assertions that should pass
- Assertions too strict for open-ended generation
- Frequent "expected keyword not found" failures

### Root Causes

1. Using exact match for open-ended responses
2. Keywords too specific or missing synonyms
3. Not accounting for paraphrase and reordering
4. Comparing against single expected output
5. Temperature > 0 with exact match assertions

### Solutions

```python
# Solution 1: Use semantic similarity
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def test_semantic():
    expected = "The capital of France is Paris."
    response = call_llm("What is the capital of France?", temperature=0.0)
    
    embeddings = model.encode([expected, response])
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    
    assert similarity >= 0.8, f"Semantic similarity {similarity:.2f} below threshold"

# Solution 2: Use multiple acceptable keywords
def test_with_alternatives():
    response = call_llm("What is the capital of France?")
    acceptable = ["paris", "france", "capital"]
    assert any(kw in response.lower() for kw in acceptable)

# Solution 3: Lower temperature for deterministic responses
def test_low_temperature():
    response = call_llm(
        "Classify sentiment: great product",
        temperature=0.0  # Deterministic
    )
    assert "positive" in response.lower()
```

---

## Golden Dataset Drift

### Symptoms

- Previously passing tests suddenly fail
- All failures related to factual queries
- Model hasn't changed but tests fail
- Failure cluster in specific categories

### Root Causes

1. Model updated by provider (no code change)
2. Dataset corrupted or modified
3. Evaluation criteria changed
4. Prompt templates changed without versioning
5. External knowledge updated (e.g., current events)

### Solutions

```python
# Solution 1: Version datasets
class VersionedDataset:
    def __init__(self, path, version):
        self.path = path
        self.version = version
        self.checksum = self._checksum()
    
    def _checksum(self):
        return hashlib.md5(open(self.path).read().encode()).hexdigest()[:8]

# Solution 2: Pin model versions in tests
def test_with_pinned_model():
    response = call_llm("What is 2+2?", model="gpt-3.5-turbo-0125")  # Specific version
    assert "4" in response

# Solution 3: Update golden dataset with review
def review_and_update_dataset():
    failures = run_regression_tests()
    for case in failures:
        print(f"Case: {case['id']}")
        print(f"Expected: {case['expected']}")
        print(f"Actual: {case['actual']}")
        # Human review needed

# Solution 4: Use time-invariant test cases
def test_stable_queries():
    stable_queries = [
        "What is 2+2?",
        "What is the chemical formula for water?",
        "Who wrote Romeo and Juliet?"
    ]
    # Avoid "current president", "today's date", etc.
```

---

## Mock Data Becoming Stale

### Symptoms

- Mocks return incorrect or outdated responses
- Tests pass but behavior differs from production
- API schema changes break mocks
- Mock responses don't match current model behavior

### Root Causes

1. Hardcoded mock responses not updated
2. API contract changed
3. Model behavior evolved
4. Mocks created for old schema
5. No regular mock validation

### Solutions

```python
# Solution 1: Validate mocks against real API periodically
def validate_mocks():
    for case in mock_test_cases:
        real_response = call_real_api(case["prompt"])
        mock_response = get_mock_response(case["prompt"])
        
        similarity = semantic_similarity(real_response, mock_response)
        if similarity < 0.7:
            logger.warning(f"Mock drift for {case['id']}: similarity={similarity:.2f}")

# Solution 2: Record real responses as fixture
def record_fixtures():
    client = LLMClient(model="gpt-3.5-turbo")
    prompts = load_test_prompts()
    
    fixtures = []
    for prompt in prompts:
        response = client.generate(prompt)
        fixtures.append({
            "prompt": prompt,
            "response": response,
            "model": "gpt-3.5-turbo",
            "timestamp": datetime.now().isoformat()
        })
    
    with open("fixtures/real_responses.json", "w") as f:
        json.dump(fixtures, f, indent=2)

# Solution 3: Pin mock to specific model version
@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.generate.return_value = load_fixture("gpt-3.5-turbo-0125/response.json")
    mock.model = "gpt-3.5-turbo-0125"
    return mock
```

---

## CI/CD Pipeline Failures

### Symptoms

- Tests pass locally but fail in CI
- Intermittent CI failures
- Pipeline times out or crashes
- Environment-specific errors
- Secrets not found errors

### Root Causes

1. Missing environment variables in CI
2. Different Python/library versions
3. Rate limiting in shared CI environment
4. Network issues in CI
5. Insufficient resources (memory, disk)
6. Order-dependent tests failing in parallel CI

### Solutions

```python
# Solution 1: Explicit environment checks
def test_environment():
    assert os.getenv("TEST_LLM_API_KEY"), "TEST_LLM_API_KEY not set"
    assert os.getenv("DATABASE_URL"), "DATABASE_URL not set"

# Solution 2: Skip tests requiring external resources
@pytest.fixture
def llm_client():
    if not os.getenv("TEST_LLM_API_KEY"):
        pytest.skip("LLM_API_KEY not set")
    return LLMClient(api_key=os.getenv("TEST_LLM_API_KEY"))

# Solution 3: Use GitHub Actions secrets
# .github/workflows/tests.yml
jobs:
  test:
    env:
      TEST_LLM_API_KEY: ${{ secrets.TEST_LLM_API_KEY }}
      TEST_DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

# Solution 4: Lock dependency versions
# requirements.txt
# pytest==7.4.0
# openai==1.3.0
# hypothesis==6.92.0

# Solution 5: Increase CI resources
# runs-on: ubuntu-latest-4-cores
# Or add more RAM/timeout
```

### CI Debug Steps

```yaml
# Add debug step to CI
- name: Debug environment
  run: |
    python --version
    pip list
    env | grep TEST
    nproc
    free -h
```

---

## Coverage Reporting Issues

### Symptoms

- Coverage report shows 0% or missing files
- Coverage drops after adding new tests
- Coverage thresholds block CI incorrectly
- Coverage HTML report empty

### Root Causes

1. Coverage not configured for source path
2. Tests and source in different directories
3. Running coverage on wrong Python interpreter
4. Dynamic imports or eval not tracked
5. Coverage configuration missing

### Solutions

```ini
# setup.cfg or pyproject.toml
[coverage:run]
source = src
omit = 
    */tests/*
    */migrations/*
    */__pycache__/*

[coverage:report]
precision = 2
show_missing = True
skip_covered = False

[coverage:html]
directory = htmlcov
```

```bash
# Run with correct configuration
pytest --cov=src --cov-report=html --cov-report=term

# Check coverage for specific file
pytest --cov=src/myapp/llm.py tests/test_llm.py
```

### Common Coverage Fixes

```python
# Problem: AI code uses dynamic imports
# Solution: Cover with pragma comments

def call_llm(prompt):  # pragma: no cover
    ...

# Or configure coverage to ignore
# setup.cfg
[coverage:run]
omit = */llm_client.py  # External, not testable
```

---

## Agent Infinite Loops in Tests

### Symptoms

- Test hangs until timeout
- CPU at 100% during test
- No output, just spinning
- CI kills test after timeout

### Root Causes

1. `max_iterations` not set or too high
2. Agent self-corrects indefinitely
3. Tool calls never complete
4. No termination condition
5. Agent enters error-retry loop

### Solutions

```python
# Solution 1: Always set max_iterations
def test_agent_with_limit():
    agent = Agent(max_iterations=3)
    result = agent.run("Complex task")
    assert result.iterations <= 3
    assert result.termination_reason == "max_iterations"

# Solution 2: Add timeout wrapper
import signal

class TimeoutAgent:
    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def run(self, agent, prompt):
        def handler(signum, frame):
            raise TimeoutError(f"Agent exceeded {self.timeout}s")
        
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.timeout)
        
        try:
            return agent.run(prompt)
        finally:
            signal.alarm(0)

# Solution 3: Mock tools for loop testing
def test_agent_loop_with_mock():
    mock_tool = MagicMock()
    mock_tool.invoke.return_value = "Result"
    
    agent = Agent(tools=[mock_tool], max_iterations=5)
    result = agent.run("Use tool multiple times")
    
    assert mock_tool.call_count <= 5
```

### Loop Detection

```python
def test_no_infinite_loop():
    agent = Agent(max_iterations=5)
    
    start = time.time()
    result = agent.run("Loop trigger")
    elapsed = time.time() - start
    
    assert elapsed < 5.0, f"Agent took {elapsed:.1f}s, likely infinite loop"
    assert result.iterations <= 5
```

---

## Tool Call Mocking Difficulties

### Symptoms

- Can't mock tool responses correctly
- Agent calls wrong tool
- Tool parameters not validated
- Mock tool not being called at all
- Tool call chain breaks in test

### Root Causes

1. Wrong mock target (mocking implementation instead of interface)
2. Tool registry not updated with mock
3. Agent bypassing tool abstraction
4. Complex tool chains hard to set up
5. Tool schemas not matched

### Solutions

```python
# Solution 1: Mock at tool interface
class TestToolMocks:
    def test_search_tool_mocked(self):
        mock_search = MagicMock()
        mock_search.invoke.return_value = [
            {"id": "1", "title": "Python Guide", "score": 0.95}
        ]
        
        agent = Agent(tools=[mock_search])
        result = agent.run("Search for Python")
        
        mock_search.invoke.assert_called_once()
        assert "Python" in result

    def test_tool_chain(self):
        mock_search = MagicMock(return_value=[{"id": "1", "content": "Python info"}])
        mock_summarize = MagicMock(return_value="Python is a programming language.")
        
        agent = Agent(tools=[mock_search, mock_summarize])
        result = agent.run("Search and summarize Python")
        
        mock_search.assert_called()
        mock_summarize.assert_called()

# Solution 2: Use tool fixture
@pytest.fixture
def mock_tools():
    return {
        "search": MagicMock(return_value=[{"id": "1", "content": "Result"}]),
        "calculator": MagicMock(return_value="42"),
        "save": MagicMock(return_value="Saved")
    }

def test_with_fixture_tools(mock_tools):
    agent = Agent(tools=list(mock_tools.values()))
    result = agent.run("Search and calculate")
    assert result is not None
```

---

## Streaming Test Instability

### Symptoms

- Streaming tests fail intermittently
- Incomplete chunks received
- Order of chunks inconsistent
- Timeout waiting for first token
- Tests pass on local but fail in CI

### Root Causes

1. Network jitter affecting chunk timing
2. No timeout on streaming read
3. Client buffering affecting chunk delivery
4. Load in CI affecting latency
5. Race condition in chunk collection

### Solutions

```python
# Solution 1: Add timeout to streaming
def test_streaming_with_timeout():
    chunks = []
    try:
        for chunk in call_llm_streaming("Hello", timeout=30):
            chunks.append(chunk)
    except StreamTimeout:
        pytest.fail("Streaming timed out")
    
    full = "".join(chunks)
    assert len(full) > 0

# Solution 2: Assert on final output, not chunk timing
def test_streaming_final():
    full_text = ""
    for chunk in call_llm_streaming("Tell me a story"):
        full_text += chunk
    
    assert "story" in full_text.lower()
    assert len(full_text) > 50

# Solution 3: Use mock for streaming in unit tests
def test_streaming_with_mock():
    mock_client = MagicMock()
    mock_client.stream.return_value = iter(["Hello", " world", "!"])
    
    chunks = list(mock_client.stream("test"))
    assert "".join(chunks) == "Hello world!"

# Solution 4: Test first token separately
def test_first_token():
    start = time.time()
    for chunk in call_llm_streaming("Hello"):
        first_token_time = time.time() - start
        break
    
    assert first_token_time < 2.0
```

---

## Multi-Turn State Leakage Between Tests

### Symptoms

- Tests fail when run together but pass individually
- Conversation context from one test appears in another
- Session IDs collide
- Memory leaks between tests

### Root Causes

1. Same session ID used across tests
2. Global conversation state not reset
3. In-memory session store shared
4. Fixture not providing isolated session
5. Class-scoped fixtures retaining state

### Solutions

```python
# Solution 1: Unique session per test
@pytest.fixture
def isolated_session():
    session_id = str(uuid.uuid4())
    chatbot = Chatbot(session_id=session_id)
    yield chatbot
    cleanup_session(session_id)

def test_session_1(isolated_session):
    isolated_session.send("Secret 1")

def test_session_2(isolated_session):
    # Fresh session, no leakage
    response = isolated_session.send("What is secret 1?")
    assert "Secret 1" not in response

# Solution 2: Autouse cleanup
@pytest.fixture(autouse=True)
def cleanup_sessions():
    yield
    SessionStore.clear_all()

# Solution 3: Verify isolation explicitly
def test_no_session_leakage():
    s1 = Chatbot(session_id="test-leak-1")
    s1.send("Private info")
    
    s2 = Chatbot(session_id="test-leak-2")
    response = s2.send("Retrieve private info")
    
    assert "Private info" not in response
```

---

## Database and Fixture Pollution

### Symptoms

- Tests fail when order changes
- Data from previous test appears in next test
- Database grows after each test
- Cleanup not happening

### Root Causes

1. Database transactions not rolled back
2. Fixtures not yielding cleanup
3. Shared database across tests
4. No teardown after test
5. Fixture setup failing silently

### Solutions

```python
# Solution 1: Transaction rollback
@pytest.fixture
def db_session():
    session = Session()
    transaction = session.begin()
    yield session
    transaction.rollback()
    session.close()

# Solution 2: Use separate databases
@pytest.fixture(scope="function")
def test_db():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.drop_all()

# Solution 3: Cleanup in fixture
@pytest.fixture
def temp_data():
    data = create_test_data()
    yield data
    cleanup_test_data(data)

# Solution 4: Verify cleanup
def test_with_verification():
    initial_count = db.session.query(User).count()
    # ... test creates user ...
    final_count = db.session.query(User).count()
    assert final_count == initial_count, "Fixture left data behind"
```

---

## Network-Dependent Tests Failing

### Symptoms

- Tests fail with connection errors
- Works locally but fails in CI
- Intermittent network failures
- DNS resolution failures
- Firewall blocking requests

### Root Causes

1. External API unreachable in CI
2. Network policies in CI/CD environment
3. VPN required for internal APIs
4. Rate limiting causing failures
5. DNS issues in containerized CI

### Solutions

```python
# Solution 1: Mock network calls in unit tests
@patch("myapp.api.requests.get")
def test_with_mocked_network(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "test"}
    
    result = fetch_data("http://api.example.com")
    assert result == {"data": "test"}

# Solution 2: Skip network tests when offline
@pytest.fixture
def network_check():
    try:
        requests.get("http://example.com", timeout=2)
        yield True
    except (requests.ConnectionError, requests.Timeout):
        pytest.skip("Network unavailable")

# Solution 3: Use local mock server
@pytest.fixture
def mock_server():
    server = MockHTTPServer()
    server.add_response("/api", json={"status": "ok"})
    server.start()
    yield server
    server.stop()

# Solution 4: Retry on transient failures
@pytest.mark.flaky(reruns=3)
def test_network_call():
    response = requests.get("http://internal-api")
    assert response.status_code == 200
```

---

## Cost Overruns in Test Execution

### Symptoms

- Monthly API bill unexpectedly high
- Tests using expensive models
- CI costs growing with test count
- No visibility into test costs

### Root Causes

1. Expensive models (gpt-4, claude-3) used in unit tests
2. Large context windows per test
3. No token budget enforcement
4. Tests run multiple times per day
5. No cost monitoring

### Solutions

```python
# Solution 1: Token budget per test run
class TestBudget:
    def __init__(self, daily_limit=50.00):
        self.daily_limit = daily_limit
        self.spent = 0
    
    def check(self, cost):
        if self.spent + cost > self.daily_limit:
            raise BudgetExceeded(f"Daily budget exceeded: ${self.spent:.2f}")
        self.spent += cost

# Solution 2: Route tests to cheaper models
@pytest.fixture
def model_router():
    def route(test_type):
        if test_type == "unit":
            return "gpt-3.5-turbo"  # Cheaper
        elif test_type == "safety":
            return "gpt-4"  # Better safety
        else:
            return os.getenv("TEST_MODEL", "gpt-3.5-turbo")
    return route

# Solution 3: Cache expensive calls
from cachetools import LRUCache

cache = LRUCache(maxsize=1000)

def cached_llm_call(prompt):
    if prompt in cache:
        return cache[prompt]
    response = call_llm(prompt)
    cache[prompt] = response
    return response

# Solution 4: Monitor costs in CI
def test_cost_tracking():
    start_cost = get_daily_cost()
    # ... run tests ...
    end_cost = get_daily_cost()
    test_cost = end_cost - start_cost
    
    assert test_cost < 0.50, f"Test cost ${test_cost:.2f} exceeds budget"
```

---

## Model Version Differences Causing Test Failures

### Symptoms

- Tests pass with one model but fail with another
- Different models produce different formats
- Behavior changes after model update
- No error, just different output

### Root Causes

1. Model auto-updated by provider
2. Tests hardcoded to specific model version
3. Different models have different capabilities
4. Model-specific formatting differences
5. Safety filters vary by model version

### Solutions

```python
# Solution 1: Pin model versions
MODEL_VERSION = "gpt-3.5-turbo-0125"  # Specific version

def test_with_pinned_model():
    response = call_llm("What is 2+2?", model=MODEL_VERSION)
    assert "4" in response

# Solution 2: Parameterize tests across models
@pytest.mark.parametrize("model", [
    "gpt-3.5-turbo-0125",
    "gpt-4-0125-preview"
])
def test_across_models(model):
    response = call_llm("What is 2+2?", model=model)
    assert "4" in response, f"Model {model} failed"

# Solution 3: Model-specific assertions
def test_model_specific():
    model = os.getenv("TEST_MODEL", "gpt-3.5-turbo")
    
    if "gpt-4" in model:
        expected_format = "JSON"
    else:
        expected_format = "text"
    
    response = call_llm(f"Output as {expected_format}")
    assert expected_format.lower() in response.lower() or True  # Flexible
```

### Model Version Matrix

```yaml
# CI matrix for multiple models
strategy:
  matrix:
    model: [gpt-3.5-turbo-0125, gpt-4-0125-preview, claude-3-opus]
```

---

## Embedding Drift

### Symptoms

- Similarity scores drop for semantically similar texts
- Vector search returns wrong results
- Embeddings not consistent across runs
- Model embeddings changed after update

### Root Causes

1. Embedding model updated
2. Embeddings computed with different model
3. Normalization not applied consistently
4. Dimensionality mismatch
5. Batch vs single embedding differences

### Solutions

```python
# Solution 1: Pin embedding model version
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def test_with_pinned_embedder():
    embedder = EmbeddingModel(model=EMBEDDING_MODEL)
    vec = embedder.embed("test")
    assert vec.shape[0] == 384

# Solution 2: Verify similarity stability
def test_embedding_consistency():
    embedder = EmbeddingModel(model=EMBEDDING_MODEL)
    
    pairs = [
        ("Cat sat on mat", "Feline on rug"),
        ("Python programming", "JavaScript web dev")
    ]
    
    for text1, text2 in pairs:
        sim = embedder.similarity(text1, text2)
        assert sim >= 0.5, f"Similarity dropped for: {text1} vs {text2}"

# Solution 3: Batch embedding consistency
def test_batch_vs_single():
    embedder = EmbeddingModel(model=EMBEDDING_MODEL)
    texts = ["Text A", "Text B", "Text C"]
    
    batch_embeddings = embedder.embed_batch(texts)
    
    for i, text in enumerate(texts):
        single = embedder.embed(text)
        np.testing.assert_array_almost_equal(batch_embeddings[i], single)
```

---

## Prompt Template Rendering Errors

### Symptoms

- `TemplateSyntaxError` or `KeyError` in tests
- Prompt renders differently than expected
- Variables not substituted correctly
- Whitespace or formatting issues

### Root Causes

1. Jinja2 syntax errors
2. Missing required variables
3. Variable name mismatch
4. Extra whitespace in template
5. Template inheritance issues

### Solutions

```python
# Solution 1: Validate templates at load time
def validate_prompt_template(template_str):
    from jinja2 import TemplateSyntaxError
    try:
        Template(template_str)
    except TemplateSyntaxError as e:
        raise ValueError(f"Invalid template: {e}")

# Solution 2: Test template rendering explicitly
class TestPromptTemplates:
    def test_render_complete(self):
        template = PromptTemplate("Q: {question}\nA: {answer}")
        result = template.render(question="What is AI?", answer="Artificial Intelligence")
        assert "What is AI?" in result
        assert "Artificial Intelligence" in result

    def test_render_missing_variable_fails(self):
        template = PromptTemplate("Q: {question}")
        with pytest.raises((KeyError, ValueError)):
            template.render()  # Missing 'question'

    def test_render_extra_variables_ignored(self):
        template = PromptTemplate("Hello {name}")
        result = template.render(name="World", extra="ignored")
        assert result == "Hello World"
```

---

## Fixture Setup and Teardown Issues

### Symptoms

- Tests fail with "fixture not found"
- State from previous test persists
- Cleanup code not running
- Fixture errors swallowed silently
- Tests pass in isolation but fail in suite

### Root Causes

1. Fixture scope too broad
2. Teardown code not in finally block
3. Fixture raising exception on cleanup
4. Missing yield in fixture
5. Autouse fixture interfering

### Solutions

```python
# Solution 1: Proper fixture with cleanup
@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test")
    yield file
    # Cleanup in finally
    try:
        file.unlink()
    except FileNotFoundError:
        pass

# Solution 2: Multiple yield fixtures
@pytest.fixture
def db_transaction():
    conn = connect()
    transaction = conn.begin()
    try:
        yield conn
    finally:
        transaction.rollback()
        conn.close()

# Solution 3: Debug fixture issues
@pytest.fixture
def debug_fixture():
    print("SETUP")
    yield "value"
    print("TEARDOWN")

# Solution 4: Fixture dependency order
@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def db(app):
    db = create_db()
    yield db
```

### Fixture Debug Checklist

- [ ] Fixture has yield statement
- [ ] Cleanup is in finally block
- [ ] Scope is appropriate (function vs session)
- [ ] No exceptions in teardown
- [ ] Fixture dependencies are clear

---

## Parallel Test Conflicts

### Symptoms

- Tests pass individually but fail together
- Random failures in CI with parallel execution
- Race conditions in shared resources
- Database constraint violations
- File access conflicts

### Root Causes

1. Shared database without isolation
2. Global state modified by parallel tests
3. Rate limiting hit by parallel requests
4. Same file/socket being used
5. Autouse fixtures creating conflicts

### Solutions

```python
# Solution 1: Use pytest-xdist with isolated fixtures
@pytest.fixture
def isolated_db():
    db = Database(f"test_{uuid.uuid4()}")
    yield db
    db.drop()

# Solution 2: Disable parallelism for specific tests
@pytest.mark.serial
def test_not_parallel():
    ...

# Solution 3: Use locks for shared resources
import threading

file_lock = threading.Lock()

def test_with_lock():
    with file_lock:
        # Safe file access
        write_shared_file("test_data")

# Solution 4: Separate resources per worker
@pytest.fixture
def worker_id(request):
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    return "master"

@pytest.fixture
def unique_resource(worker_id):
    return create_resource(f"resource_{worker_id}")
```

### Running with Parallelism

```bash
# Run with 4 workers
pytest tests/ -n 4

# Auto-detect CPU count
pytest tests/ -n auto

# Exclude serial tests from parallel
pytest tests/ -n auto -m "not serial"
```

---

## Secrets Management in Tests

### Symptoms

- Hardcoded credentials in test files
- Tests fail with auth errors
- Different credentials needed per environment
- Secrets leaked in test output/logs

### Root Causes

1. API keys committed to repository
2. Environment variables not set in CI
3. Secrets in test fixtures
4. No separation of test/prod credentials

### Solutions

```python
# Solution 1: Use environment variables
def get_api_key():
    key = os.environ.get("TEST_API_KEY")
    if not key:
        pytest.skip("TEST_API_KEY not set")
    return key

# Solution 2: CI secrets
# .github/workflows/tests.yml
env:
  TEST_API_KEY: ${{ secrets.TEST_API_KEY }}

# Solution 3: Vault for complex setups
import hvac

def get_secret(path):
    client = hvac.Client(url=os.getenv("VAULT_URL"))
    return client.secrets.kv.v2.read_secret_version(path=path)

# Solution 4: Prevent secret leakage
def test_no_secrets_in_logs(caplog):
    with caplog.at_level(logging.DEBUG):
        call_llm("test")
    
    assert "sk-proj-" not in caplog.text
    assert "api_key" not in caplog.text
```

---

## Cross-Platform Test Failures

### Symptoms

- Tests pass on macOS but fail on Linux (or vice versa)
- Path separator issues (`\` vs `/`)
- Line ending differences (`\n` vs `\r\n`)
- Case-sensitive filesystem issues
- Encoding differences

### Root Causes

1. Hardcoded path separators
2. Case-sensitive filename assumptions
3. OS-specific file paths
4. Different default encodings
5. Line ending mismatches

### Solutions

```python
# Solution 1: Use pathlib for cross-platform paths
from pathlib import Path

def test_with_pathlib():
    data_path = Path("tests") / "fixtures" / "data.json"
    data = json.loads(data_path.read_text())

# Solution 2: Normalize line endings
def normalize_line_endings(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")

# Solution 3: Case-insensitive checks on Windows
@pytest.mark.skipif(sys.platform == "win32", reason="Case-sensitive")
def test_case_sensitive():
    assert "File.txt" != "file.txt"

# Solution 4: UTF-8 encoding explicitly
def test_unicode():
    with open("test.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "日本語" in content
```

### CI Matrix for Cross-Platform

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/
```

---

## Unicode and Encoding Issues

### Symptoms

- `UnicodeDecodeError` or `UnicodeEncodeError`
- Emoji or special characters garbled
- Tests pass with ASCII but fail with Unicode
- Encoding mismatch between test data and code

### Root Causes

1. File opened without specifying encoding
2. Mixed encodings in test data
3. Terminal/console encoding mismatch
4. Python 2/3 encoding differences
5. JSON/CSV files with BOM

### Solutions

```python
# Solution 1: Always specify encoding
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Solution 2: Handle encoding errors gracefully
with open("file.txt", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Solution 3: Normalize Unicode
import unicodedata

def normalize_unicode(text):
    return unicodedata.normalize("NFKC", text)

# Solution 4: Test with diverse Unicode
@pytest.mark.parametrize("text", [
    "Hello 世界",
    "Привет мир",
    "مرحبا بالعالم",
    "🌍🌎🌏",
    "café résumé naïve"
])
def test_unicode_handling(text):
    response = call_llm(f"Process: {text}")
    assert response is not None
```

---

## Large Context Test Failures

### Symptoms

- Tests fail with inputs > 1000 tokens
- Memory errors in test
- Context window exceeded
- Slow tests with large inputs

### Root Causes

1. Large golden dataset entries
2. Long conversation histories in fixtures
3. Large documents in RAG tests
4. No input size limits in tests
5. Generating large synthetic data

### Solutions

```python
# Solution 1: Enforce size limits in fixtures
@pytest.fixture
def limited_context():
    max_chars = 5000
    text = generate_context(max_chars=max_chars)
    assert len(text) <= max_chars
    return text

# Solution 2: Test with stratified sizes
@pytest.mark.parametrize("size", [100, 1000, 3000, 5000, 8000])
def test_context_scaling(size):
    text = " ".join(["word"] * (size // 5))
    try:
        response = call_llm(text)
        assert response is not None
    except TokenLimitExceeded:
        assert size >= 4000  # Only fail near limit

# Solution 3: Sample large datasets
def test_large_dataset_sample():
    full_dataset = load_dataset("large.jsonl")  # 100k entries
    sample = random.sample(full_dataset, 100)
    
    for case in sample:
        response = call_llm(case["prompt"])
        assert response is not None
```

---

## RAG Retrieval Inconsistency

### Symptoms

- Same query returns different results
- Document ranking unstable
- Retrieval fails intermittently
- Embedding not found errors

### Root Causes

1. Vector index not seeded consistently
2. Embedding model non-determinism
3. Top-k randomness in retrieval
4. Index updates during test
5. Concurrent index modifications

### Solutions

```python
# Solution 1: Seed vector store in fixture
@pytest.fixture
def seeded_index():
    index = VectorIndex(dim=384)
    docs = load_test_documents(seed=42)
    index.add_documents(docs)
    index.commit()
    return index

# Solution 2: Deterministic embeddings
@pytest.fixture
def deterministic_embedder():
    return EmbeddingModel(model="all-MiniLM-L6-v2", device="cpu", normalize=True)

# Solution 3: Freeze index during tests
@pytest.fixture
def frozen_index():
    index = VectorIndex.load("tests/fixtures/index")
    index.read_only = True
    return index

# Solution 4: Test with fixed embedding
def test_retrieval_consistent():
    embedder = EmbeddingModel(model="all-MiniLM-L6-v2")
    query_vec = embedder.embed("Python programming")
    
    results_1 = index.search(query_vec, top_k=5)
    results_2 = index.search(query_vec, top_k=5)
    
    assert [r["id"] for r in results_1] == [r["id"] for r in results_2]
```

---

## Human Evaluation Bottlenecks

### Symptoms

- Human eval queue backing up
- Evaluators unavailable for testing
- Long wait times for human feedback
- Inconsistent evaluation quality

### Root Causes

1. Too many items queued for human review
2. Limited evaluator pool
3. No automated pre-filtering
4. Evaluation criteria unclear
5. Low inter-rater reliability

### Solutions

```python
# Solution 1: Pre-filter with automated checks
def pre_filter_for_human_eval(responses):
    filtered = []
    for response in responses:
        if automated_safety_check(response) and automated_quality_check(response):
            filtered.append(response)
        else:
            # Auto-reject, don't queue for human
            mark_as_failed(response)
    return filtered

# Solution 2: Sample strategically
def sample_for_human_eval(total, budget=100):
    if total <= budget:
        return list(range(total))
    
    # Prioritize high-risk cases
    high_risk = get_high_risk_cases()
    remaining = budget - len(high_risk)
    
    random_sample = random.sample(
        [i for i in range(total) if i not in high_risk],
        remaining
    )
    
    return high_risk + random_sample

# Solution 3: Clear evaluation criteria
EVALUATION_CRITERIA = {
    "accuracy": "Is the information factually correct? (1-5)",
    "safety": "Is the response safe and appropriate? (1-5)",
    "helpfulness": "Does this help the user? (1-5)",
    "relevance": "Is the response relevant to the query? (1-5)"
}

# Solution 4: Automated confidence scoring
def auto_evaluate(response):
    confidence = 0
    
    if response and len(response) > 10:
        confidence += 1
    if "cannot" not in response.lower():
        confidence += 1
    if len(set(response.lower().split())) > 5:
        confidence += 1
    
    return confidence >= 2  # Only pass high-confidence to human
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
