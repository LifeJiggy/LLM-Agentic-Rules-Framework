# Testing Domain - Fundamentals

## Overview

This document covers the fundamental concepts of testing for LLM/agentic systems. Understanding these principles is essential for building reliable, maintainable, and production-ready test suites.

## Table of Contents

1. [What Makes AI Testing Different](#what-makes-ai-testing-different)
2. [Testing Pyramid for AI Systems](#testing-pyramid-for-ai-systems)
3. [Unit Testing Fundamentals](#unit-testing-fundamentals)
4. [Integration Testing Fundamentals](#integration-testing-fundamentals)
5. [End-to-End Testing Fundamentals](#end-to-end-testing-fundamentals)
6. [Mocking Strategies](#mocking-strategies)
7. [Test Fixtures and Setup](#test-fixtures-and-setup)
8. [Assertions](#assertions)
9. [Determinism and Seeding](#determinism-and-seeding)
10. [Non-Determinism Handling](#non-determinism-handling)
11. [Test Data Management](#test-data-management)
12. [Evaluation Metrics](#evaluation-metrics)
13. [Property-Based Testing Basics](#property-based-testing-basics)
14. [Contract Testing Basics](#contract-testing-basics)
15. [Mutation Testing Basics](#mutation-testing-basics)
16. [Continuous Integration for AI](#continuous-integration-for-ai)
17. [Test Coverage for Non-Deterministic Systems](#test-coverage-for-non-deterministic-systems)
18. [Test Flakiness](#test-flakiness)
19. [Test Naming Conventions](#test-naming-conventions)
20. [Test Organization and Structure](#test-organization-and-structure)
21. [Fixture Scoping and Cleanup](#fixture-scoping-and-cleanup)
22. [Environment Setup](#environment-setup)
23. [Secrets and Credentials](#secrets-and-credentials)
24. [Parallel Test Execution](#parallel-test-execution)
25. [Test Reporting and Diagnostics](#test-reporting-and-diagnostics)
26. [Debugging Failing Tests](#debugging-failing-tests)

---

## What Makes AI Testing Different

### Description

Testing LLM and agentic systems introduces challenges not present in traditional software testing. Outputs are non-deterministic, evaluation requires semantic understanding, and system behavior evolves with model updates.

### Key Differences

Traditional software tests exact outputs. AI tests must evaluate:
- Semantic correctness rather than exact string matches
- Statistical properties across many generations
- Safety and alignment properties
- Behavioral consistency under non-determinism
- Performance under variable latency

### Traditional vs AI Testing

```python
# Traditional test
def test_add():
    assert add(2, 3) == 5  # Deterministic, exact match

# AI test
def test_summarization():
    response = call_llm("Summarize: The cat sat on the mat.")
    assert "cat" in response.lower()
    assert len(response) < len("The cat sat on the mat.")
    # Semantic evaluation, not exact match
```

### Implications

1. **Assertions are softer**: Keyword, semantic similarity, or probabilistic assertions replace exact equality.
2. **Tests are statistical**: Single runs are insufficient; aggregate metrics over many trials.
3. **Flakiness is inherent**: Non-determinism must be managed, not eliminated.
4. **Golden datasets are critical**: Stable benchmarks enable regression detection.
5. **Safety is first-class**: Alignment and safety testing are mandatory, not optional.

---

## Testing Pyramid for AI Systems

### Description

The classic testing pyramid applies to AI systems with important modifications. Unit tests remain the foundation, but integration and safety tests carry more weight than in traditional systems.

### AI Testing Pyramid

```
           /\
          /E2E\           <- Fewest: full agent flows, multi-turn conversations
         /-----\          <- Some: RAG pipelines, tool integration, safety tests
        /Integration\     <- More: API contracts, prompt evaluation, model benchmarks
       /------------\
      /   Unit Tests \    <- Many: component logic, prompt validation, token counting
     /________________\
```

### Layer Breakdown

```python
# Unit: Fast, deterministic, mocked
def test_tokenizer_counts_tokens():
    tokenizer = Tokenizer()
    assert tokenizer.count("Hello world") == 2

# Integration: Moderate speed, real components
def test_rag_pipeline():
    response = rag.query("What is Python?")
    assert "programming" in response.lower()

# E2E: Slow, full system
def test_agent_booking_flow():
    agent = Agent(tools=["search", "book"])
    result = agent.run("Book a flight from NYC to London")
    assert "confirmation" in result.lower()
```

### Production Consideration

Maintain the pyramid shape. Too many E2E tests make suites slow; too few unit tests reduce defect detection speed.

---

## Unit Testing Fundamentals

### Description

Unit tests validate individual components in isolation. For AI systems, this means testing wrappers, utils, prompt templates, and business logic with mocked LLMs.

### Core Principles

- Test one behavior per test function
- Use mocks for external dependencies
- Keep tests fast (< 1ms each)
- Make tests deterministic
- Follow Arrange-Act-Assert

### Example: Testing a Prompt Template

```python
# test_prompts.py
import pytest
from myapp.prompts import PromptTemplate

class TestPromptTemplate:
    def test_render_with_all_variables(self):
        template = PromptTemplate("Q: {question}\nA: {answer}")
        result = template.render(question="What is AI?", answer="Artificial Intelligence")
        assert "What is AI?" in result
        assert "Artificial Intelligence" in result

    def test_render_missing_variable_raises(self):
        template = PromptTemplate("Q: {question}")
        with pytest.raises(KeyError):
            template.render()  # Missing required 'question'

    def test_render_with_defaults(self):
        template = PromptTemplate("Hello {name}", defaults={"name": "World"})
        result = template.render()
        assert result == "Hello World"

    def test_multiple_renders(self):
        template = PromptTemplate("Process: {text}")
        r1 = template.render(text="First")
        r2 = template.render(text="Second")
        assert r1 != r2
```

### Example: Testing Tokenizer Wrapper

```python
# test_tokenizer.py
import pytest
from myapp.tokenizer import TokenizerWrapper

class TestTokenizerWrapper:
    def test_count_tokens(self):
        tokenizer = TokenizerWrapper(model="gpt-3.5-turbo")
        count = tokenizer.count("Hello world")
        assert count >= 2

    def test_count_empty_string(self):
        tokenizer = TokenizerWrapper(model="gpt-3.5-turbo")
        count = tokenizer.count("")
        assert count == 0

    def test_truncate_to_limit(self):
        tokenizer = TokenizerWrapper(model="gpt-3.5-turbo")
        long_text = " ".join(["word"] * 1000)
        truncated = tokenizer.truncate(long_text, max_tokens=50)
        assert tokenizer.count(truncated) <= 50

    def test_encode_decode_roundtrip(self):
        tokenizer = TokenizerWrapper(model="gpt-3.5-turbo")
        text = "Hello world"
        tokens = tokenizer.encode(text)
        decoded = tokenizer.decode(tokens)
        assert decoded == text
```

---

## Integration Testing Fundamentals

### Description

Integration tests verify that components work together. For AI systems, this includes testing wrappers around APIs, prompt chains, and tool integrations.

### Core Principles

- Test real integrations, not mocks
- Use test doubles for external services when necessary
- Clean up shared state between tests
- Run integration tests less frequently than unit tests

### Example: Testing LLM API Wrapper

```python
# test_llm_integration.py
import pytest
from myapp.llm import LLMClient

class TestLLMIntegration:
    @pytest.fixture
    def client(self):
        return LLMClient(
            model=os.getenv("TEST_MODEL", "gpt-3.5-turbo"),
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def test_chat_completion(self, client):
        response = client.chat("What is 2+2?")
        assert "4" in response

    def test_streaming_completion(self, client):
        chunks = list(client.stream("Tell me a story"))
        full = "".join(chunks)
        assert len(full) > 50

    def test_token_usage_reported(self, client):
        response = client.chat("Hello")
        assert response.prompt_tokens > 0
        assert response.completion_tokens > 0
```

### Example: Testing RAG Integration

```python
# test_rag_integration.py
import pytest
from myapp.rag import RAGPipeline
from myapp.vector_store import VectorStore

class TestRAGIntegration:
    @pytest.fixture
    def rag(self):
        vector_store = VectorStore(dim=384)
        vector_store.add_documents(load_test_documents())
        return RAGPipeline(vector_store=vector_store)

    def test_query_returns_response(self, rag):
        response = rag.query("What is Python?")
        assert response is not None
        assert len(response) > 0

    def test_query_uses_retrieved_context(self, rag):
        response = rag.query("What is Python?")
        assert "programming" in response.lower()
```

---

## End-to-End Testing Fundamentals

### Description

E2E tests validate complete user workflows. They are slowest but most valuable for catching real issues.

### Core Principles

- Test critical user journeys
- Use production-like data
- Clean up state after tests
- Run E2E tests on deploy, not on every commit

### Example: E2E Chat Flow

```python
# test_e2e_chat.py
import pytest
from myapp.chat import Chatbot

class TestE2EChat:
    @pytest.fixture
    def chatbot(self):
        return Chatbot()

    def test_full_conversation(self, chatbot):
        r1 = chatbot.send("My name is Bob")
        assert "Bob" in r1
        
        r2 = chatbot.send("What is my name?")
        assert "Bob" in r2
        
        r3 = chatbot.send("What did I just tell you?")
        assert "name" in r3.lower()
```

### Example: E2E Agent Workflow

```python
# test_e2e_agent.py
import pytest
from myapp.agent import Agent

class TestE2EAgent:
    def test_research_workflow(self):
        agent = Agent(tools=["search", "summarize", "save"])
        result = agent.run("Research Python and save a summary")
        
        assert result is not None
        assert len(result.final_output) > 0
        assert result.file_saved is True

    def test_error_recovery_workflow(self):
        agent = Agent(tools=["search", "calculate", "email"])
        result = agent.run("Search for data, calculate results, and email report")
        
        assert result is not None
        assert "error" not in result.final_output.lower() or "handled" in result.final_output.lower()
```

---

## Mocking Strategies

### Description

Mocking replaces real implementations with test doubles. Choosing the right mocking level is critical for test speed and reliability.

### Mocking Levels

1. **LLM client mock**: Replace the entire LLM API client
2. **HTTP mock**: Mock at the network layer (responses, httpretty)
3. **Response fixtures**: Pre-recorded LLM responses
4. **Partial mocks**: Mock specific methods, keep others real

### Example: Mocking LLM Client

```python
# test_mocking.py
import pytest
from unittest.mock import MagicMock, patch
from myapp.llm import OpenAIClient
from myapp.agent import Agent

class TestMocking:
    def test_mock_llm_client(self):
        mock_client = MagicMock()
        mock_client.chat.return_value = "The capital of France is Paris."
        
        agent = Agent(llm_client=mock_client)
        response = agent.run("What is the capital of France?")
        
        assert "Paris" in response
        mock_client.chat.assert_called_once()

    def test_mock_with_side_effect(self):
        mock_client = MagicMock()
        mock_client.chat.side_effect = [
            "I will search for that.",
            "Found 3 results.",
            "Here is the summary."
        ]
        
        agent = Agent(llm_client=mock_client, tools=[SearchTool()])
        result = agent.run("Search for Python and summarize")
        
        assert mock_client.chat.call_count == 3

    @patch("myapp.llm.OpenAI")
    def test_patch_openai(self, mock_openai):
        mock_openai.return_value.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Mocked"))]
        )
        
        client = OpenAIClient(api_key="sk-test")
        response = client.chat("Hello")
        assert "Mocked" in response

    def test_mock_streaming(self):
        mock_client = MagicMock()
        mock_client.stream.return_value = iter(["Hello", " world", "!"])
        
        chunks = list(mock_client.stream("Test"))
        assert "".join(chunks) == "Hello world!"
```

### When to Mock vs Use Real

| Scenario | Mock | Real |
|----------|------|------|
| Unit test logic | Yes | No |
| Prompt template rendering | Yes | No |
| Integration test | No | Yes |
| CI pipeline | Mostly mock | Sample |
| Nightly regression | Mocks + real subset | Yes |

---

## Test Fixtures and Setup

### Description

Fixtures provide reusable test setup and teardown. Proper fixture design reduces duplication and improves test isolation.

### Example: Common Fixtures

```python
# conftest.py
import pytest
from myapp import create_app, db
from myapp.llm import LLMClient

@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_llm():
    client = MagicMock()
    client.generate.return_value = "Mocked response"
    return client

@pytest.fixture
def sample_documents():
    return [
        {"id": "1", "content": "Python is a programming language.", "metadata": {"source": "test"}},
        {"id": "2", "content": "JavaScript is used for web development.", "metadata": {"source": "test"}},
    ]

@pytest.fixture(autouse=True)
def reset_global_state():
    # Reset any global state before each test
    GlobalState.reset()
    yield
    GlobalState.reset()
```

### Using Fixtures

```python
# test_with_fixtures.py
def test_with_app(client):
    response = client.get("/api/health")
    assert response.status_code == 200

def test_with_mock_llm(mock_llm):
    from myapp.chat import Chatbot
    bot = Chatbot(llm_client=mock_llm)
    response = bot.send("Hello")
    assert response is not None

def test_with_documents(sample_documents):
    index = VectorIndex()
    index.add_documents(sample_documents)
    results = index.search("Python", top_k=1)
    assert len(results) == 1
```

---

## Assertions

### Description

AI tests require different assertion strategies than traditional software. Exact string equality is replaced with semantic checks, keyword matching, or similarity metrics.

### Assertion Types

| Type | Use Case | Example |
|------|----------|---------|
| Exact match | Deterministic outputs, temperature=0 | `assert response == "4"` |
| Contains | Required keywords present | `assert "Paris" in response` |
| Semantic similarity | Meaning preservation | `assert similarity(response, expected) > 0.8` |
| Probabilistic | Non-deterministic behavior | `assert success_rate > 0.9` |
| Schema validation | Structured output | `assert validate_json(response)` |
| Length bounds | Response size | `assert 10 <= len(response) <= 500` |

### Example: Multi-Type Assertions

```python
# test_assertions.py
import pytest
from myapp.evaluation import semantic_similarity, validate_json_schema

class TestAssertions:
    def test_exact_match(self):
        response = call_llm("What is 2+2? Answer with just the number.", temperature=0.0)
        assert response.strip() == "4"

    def test_contains(self):
        response = call_llm("What is the capital of France?")
        assert "Paris" in response

    def test_semantic_similarity(self):
        expected = "The capital of France is Paris."
        response = call_llm("What is the capital of France?", temperature=0.0)
        sim = semantic_similarity(response, expected)
        assert sim >= 0.8

    def test_schema_validation(self):
        response = call_llm("Output JSON with name and age", temperature=0.0)
        schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}}}
        assert validate_json_schema(response, schema)

    def test_length_bounds(self):
        response = call_llm("Summarize this article", temperature=0.7)
        assert 20 <= len(response) <= 500
```

---

## Determinism and Seeding

### Description

Non-determinism is fundamental to LLMs. Seeds help manage this by making outputs reproducible when needed.

### Setting Seeds

```python
# test_determinism.py
import pytest
import random
import numpy as np

class TestDeterminism:
    def test_deterministic_with_seed(self):
        r1 = call_llm("What is 2+2?", seed=42)
        r2 = call_llm("What is 2+2?", seed=42)
        assert r1 == r2, "Same seed should produce same output"

    def test_different_seeds_produce_different_outputs(self):
        r1 = call_llm("Write a haiku", seed=1)
        r2 = call_llm("Write a haiku", seed=2)
        # With different seeds, outputs may differ
        # We just verify both are valid
        assert len(r1) > 0
        assert len(r2) > 0

@pytest.fixture(autouse=True)
def seed_all():
    random.seed(42)
    np.random.seed(42)
```

### Production Consideration

Always log the seed used for each test run. This enables replay for debugging.

---

## Non-Determinism Handling

### Description

When tests must tolerate non-determinism, use statistical methods and property-based assertions.

### Strategies

1. **Temperature=0**: Force determinism for critical assertions
2. **Property testing**: Assert invariants, not values
3. **Statistical thresholds**: Require N successful runs out of M
4. **Semantic similarity**: Check meaning, not wording

### Example: Handling Non-Determinism

```python
# test_non_determinism.py
import pytest
from statistics import mean

class TestNonDeterminism:
    def test_stable_properties(self):
        for _ in range(5):
            response = call_llm("Summarize: The cat sat on the mat.", temperature=0.7)
            assert "cat" in response.lower()
            assert "mat" in response.lower()
            assert len(response) < 100

    def test_average_length_stable(self):
        lengths = [len(call_llm("Write a sentence", temperature=0.7)) for _ in range(20)]
        avg = mean(lengths)
        assert 10 <= avg <= 100, f"Average length {avg:.1f} out of expected range"

    def test_success_rate(self):
        successes = 0
        for _ in range(50):
            response = call_llm("What is 2+2?", temperature=0.0)
            if "4" in response:
                successes += 1
        assert successes >= 45, f"Success rate {successes/50:.0%} below 90%"
```

---

## Test Data Management

### Description

Effective test data management ensures reproducibility, avoids data leakage, and keeps tests fast.

### Golden Datasets

```python
class GoldenDataset:
    def __init__(self, path):
        self.path = path
        self.data = self._load()
    
    def _load(self):
        import json
        with open(self.path) as f:
            return [json.loads(line) for line in f]
    
    def sample(self, n, seed=42):
        import random
        rng = random.Random(seed)
        return rng.sample(self.data, min(n, len(self.data)))

    def filter(self, **conditions):
        return [
            case for case in self.data
            if all(case.get(k) == v for k, v in conditions.items())
        ]
```

### Synthetic Data

```python
class SyntheticDataGenerator:
    def __init__(self, llm_client):
        self.client = llm_client
    
    def generate_prompts(self, domain, n=100):
        prompts = []
        for _ in range(n):
            prompt = self.client.generate(f"Generate a unique question about {domain}")
            prompts.append(prompt.strip())
        return prompts

    def generate_adversarial(self, base_prompt, n=20):
        variants = []
        for _ in range(n):
            variant = self.client.generate(f"Paraphrase: {base_prompt}")
            variants.append(variant.strip())
        return variants
```

### Data Versioning

```python
class DatasetVersion:
    def __init__(self, path, version):
        self.path = path
        self.version = version
        self.checksum = self._compute_checksum()

    def _compute_checksum(self):
        import hashlib
        return hashlib.md5(open(self.path, "rb").read()).hexdigest()[:8]

    def manifest(self):
        return {
            "version": self.version,
            "path": self.path,
            "checksum": self.checksum,
            "size": len(self.data)
        }
```

---

## Evaluation Metrics

### Description

Quantitative metrics enable objective comparison of model outputs. Choose metrics aligned with your task.

### Common Metrics

| Metric | Use Case | Implementation |
|--------|----------|-----------------|
| Exact Match | Factual queries, JSON output | `response == expected` |
| F1 Score | Classification, extraction | Token-level F1 |
| BLEU | Translation, paraphrasing | `sentence_bleu` |
| ROUGE | Summarization | `rouge_scorer` |
| Semantic Similarity | Open-ended generation | Embedding cosine |
| Perplexity | Language modeling | GPT-2 scorer |
| BERTScore | Semantic evaluation | `bert_score` |

### Example: Metric Computation

```python
# test_metrics.py
import pytest
from myapp.metrics import (
    exact_match, f1_score, semantic_similarity, 
    rouge_score, bleu_score
)

class TestMetrics:
    def test_exact_match(self):
        assert exact_match("Paris", "Paris") is True
        assert exact_match("Paris", "London") is False

    def test_f1_score(self):
        pred = "The cat sat on the mat"
        ref = "The cat sat on the mat"
        assert f1_score(pred, ref) == 1.0

    def test_semantic_similarity(self):
        text1 = "The capital of France is Paris."
        text2 = "Paris is the capital of France."
        sim = semantic_similarity(text1, text2)
        assert sim >= 0.9, f"Similarity {sim:.2f} too low for equivalent statements"

    def test_rouge_score(self):
        pred = "The cat sat on the mat"
        ref = "The cat sat on the mat"
        scores = rouge_score(pred, ref)
        assert scores["rouge1"]["fmeasure"] == 1.0

    def test_bleu_score(self):
        pred = "The cat sat on the mat"
        ref = "The cat sat on the mat"
        score = bleu_score(pred, ref)
        assert score == 1.0
```

---

## Property-Based Testing Basics

### Description

Property-based testing generates many inputs from strategies and verifies invariants hold for all cases.

### Core Concepts

- **Strategies** define how to generate inputs
- **Properties** are invariants that must always hold
- **Shrinking** finds minimal failing cases automatically

### Example: Basic Properties

```python
# test_properties.py
import pytest
from hypothesis import given, strategies as st
from myapp.utils import truncate_prompt, count_tokens

class TestProperties:
    @given(st.text(min_size=0, max_size=1000))
    def test_truncate_never_expands(self, text):
        truncated = truncate_prompt(text, max_tokens=50)
        assert len(truncated) <= len(text)

    @given(st.integers(min_value=1, max_value=100))
    def test_sort_preserves_elements(self, n):
        numbers = list(range(1, n + 1))
        shuffled = numbers.copy()
        random.shuffle(shuffled)
        
        response = call_llm(f"Sort: {shuffled}")
        for num in numbers:
            assert str(num) in response

    @given(st.dictionaries(
        keys=st.text(min_size=1, max_size=10),
        values=st.text(),
        min_size=1,
        max_size=5
    ))
    def test_prompt_rendering_never_crashes(self, variables):
        template = PromptTemplate("Data: {data}")
        try:
            result = template.render(**variables)
            assert isinstance(result, str)
        except Exception as e:
            pytest.fail(f"Crashed on {variables}: {e}")
```

---

## Contract Testing Basics

### Description

Contract testing verifies that integrations between services adhere to agreed-upon interfaces. For AI systems, this ensures tool calls, APIs, and model outputs conform to schemas.

### Core Concepts

- **Consumer** defines expectations
- **Provider** fulfills the contract
- **Pact** is the agreement between them

### Example: Simple Contract

```python
# test_contracts.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Contract:
    name: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    max_latency_ms: int = 1000

class TestContracts:
    def test_search_tool_contract(self):
        contract = Contract(
            name="search",
            input_schema={"query": str, "top_k": int},
            output_schema=[{"id": str, "score": float, "content": str}],
            max_latency_ms=500
        )
        
        start = time.time()
        result = call_tool("search", {"query": "Python", "top_k": 5})
        latency = (time.time() - start) * 1000
        
        assert isinstance(result, list)
        assert len(result) <= 5
        assert latency <= contract.max_latency_ms
```

---

## Mutation Testing Basics

### Description

Mutation testing evaluates test suite effectiveness by introducing small changes (mutants) and checking if tests catch them.

### Core Concepts

- **Mutant**: A small change to source code
- **Killed**: Test fails on mutant (good)
- **Survived**: Test passes on mutant (bad - test gap)
- **Mutation score**: Killed / Total mutants

### Example: Running Mutation Tests

```bash
# Install
pip install mutmut

# Run
mutmut run --paths-to-mutate src/

# View results
mutmut show
```

### Example: Custom Mutations

```python
class PromptMutator:
    def __init__(self, templates):
        self.templates = templates
    
    def mutate_temperature(self):
        mutations = []
        for t in self.templates:
            if "temperature" in t.get("params", {}):
                m = t.copy()
                m["params"]["temperature"] = 1.0
                mutations.append(m)
        return mutations

    def mutate_max_tokens(self):
        mutations = []
        for t in self.templates:
            if "max_tokens" in t.get("params", {}):
                m = t.copy()
                m["params"]["max_tokens"] = 1
                mutations.append(m)
        return mutations
```

---

## Continuous Integration for AI

### Description

CI pipelines for AI systems must include more than traditional tests. They should validate model performance, safety, and cost.

### Typical AI CI Pipeline

```yaml
# .github/workflows/ai-tests.yml
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest tests/unit/ --cov=src

  integration:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/integration/

  safety:
    runs-on: ubuntu-latest
    steps:
      - run: pytest tests/safety/

  regression:
    runs-on: ubuntu-latest
    steps:
      - run: python scripts/regression_test.py --threshold 0.85

  cost-check:
    runs-on: ubuntu-latest
    steps:
      - run: python scripts/cost_check.py --max-cost 10.00
```

### Quality Gates

```python
def ci_quality_gate():
    checks = {
        "unit_coverage": (get_coverage(), 0.85, ">="),
        "safety_score": (run_safety_tests(), 0.95, ">="),
        "latency_p95": (measure_p95_latency(), 2.0, "<="),
        "accuracy": (evaluate_accuracy(), 0.90, ">="),
        "mutation_score": (get_mutation_score(), 0.80, ">=")
    }
    
    passed = True
    for name, (value, threshold, op) in checks.items():
        if op == ">=" and value < threshold:
            print(f"FAIL: {name} = {value:.3f} (threshold: {threshold})")
            passed = False
        elif op == "<=" and value > threshold:
            print(f"FAIL: {name} = {value:.3f} (threshold: {threshold})")
            passed = False
        else:
            print(f"PASS: {name} = {value:.3f}")
    
    return passed
```

---

## Test Coverage for Non-Deterministic Systems

### Description

Traditional code coverage metrics don't capture AI test effectiveness. Use complementary metrics.

### Coverage Types

| Metric | Description | Target |
|--------|-------------|--------|
| Code coverage | Lines/branches executed | > 85% |
| Input coverage | Unique prompts tested | > 1000 |
| Tool coverage | All tools exercised | 100% |
| Error path coverage | Error branches tested | > 80% |
| Safety coverage | Safety cases tested | 100% critical |

### Example: Measuring AI Coverage

```python
def measure_ai_coverage():
    coverage = {
        "code_coverage": get_code_coverage(),
        "prompts_tested": count_unique_prompts(),
        "tools_covered": count_tools_in_tests() / total_tools(),
        "error_paths": count_error_paths_tested() / total_error_paths(),
        "safety_cases": len(run_safety_tests())
    }
    
    return coverage

def test_coverage_report():
    coverage = measure_ai_coverage()
    
    assert coverage["code_coverage"] >= 0.85
    assert coverage["prompts_tested"] >= 1000
    assert coverage["tools_covered"] == 1.0
    assert coverage["error_paths"] >= 0.8
```

---

## Test Flakiness

### Description

Flaky tests pass and fail intermittently without code changes. In AI systems, non-determinism is a common cause.

### Causes

- Non-deterministic LLM outputs
- Timing-dependent assertions
- Shared state between tests
- Network-dependent tests
- Rate limiting in shared environments

### Example: Detecting Flakiness

```python
# test_flakiness.py
import pytest
from collections import Counter

class TestFlakiness:
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_with_retry(self):
        response = call_llm("Say hello exactly: HELLO", temperature=0.0)
        assert response.strip().upper() == "HELLO"

    def test_deterministic_invariant(self):
        for _ in range(10):
            response = call_llm("What is 2+2?", seed=42)
            assert "4" in response

    def test_statistical_property(self):
        results = [call_llm("Write a sentence", temperature=0.7) for _ in range(20)]
        lengths = [len(r.split()) for r in results]
        avg = sum(lengths) / len(lengths)
        assert 5 <= avg <= 30, f"Average length {avg:.1f} out of range"
```

### Mitigation Strategies

```python
# 1. Use temperature=0 for deterministic assertions
response = call_llm(prompt, temperature=0.0)

# 2. Run multiple times for statistical properties
results = [call_llm(prompt) for _ in range(20)]
assert mean([len(r) for r in results]) > 10

# 3. Use semantic similarity instead of exact match
from sentence_transformers import util
emb1 = embed(expected)
emb2 = embed(actual)
assert util.cos_sim(emb1, emb2) > 0.8

# 4. Add retries for flaky external dependencies
@pytest.mark.flaky(reruns=3)
def test_api_call():
    response = call_api()
    assert response is not None
```

---

## Test Naming Conventions

### Description

Clear test names document intent and make failures easy to understand.

### Naming Patterns

```python
# Pattern: test_<unit>_<behavior>_when_<condition>

def test_chatbot_returns_greeting_when_prompted():
    """Chatbot returns greeting when user says hello."""
    chatbot = Chatbot()
    response = chatbot.send("Hello")
    assert "hello" in response.lower()

def test_search_returns_empty_when_no_results():
    """Search returns empty list when query matches nothing."""
    results = search("nonexistent query xyz123")
    assert results == []

def test_agent_retries_tool_call_when_timeout():
    """Agent retries tool call up to 3 times on timeout."""
    agent = Agent(tools=["search"], max_retries=3)
    agent.tools["search"].fail_count = 2
    result = agent.run("Search for Python")
    assert result is not None

def test_context_manager_evicts_oldest_when_full():
    """Context manager evicts oldest messages when at capacity."""
    manager = ContextManager(max_messages=3)
    for i in range(5):
        manager.add(f"Message {i}")
    assert len(manager.messages) == 3
    assert "Message 0" not in manager.messages[0]
```

### Naming Checklist

- [ ] Name describes what is tested
- [ ] Condition is clear (when_, should_, with_)
- [ ] Uses snake_case
- [ ] Test class names are descriptive
- [ ] Parametrized tests have clear IDs

---

## Test Organization and Structure

### Description

Organize tests to mirror source structure and make navigation intuitive.

### Directory Structure

```
project/
├── src/
│   ├── llm/
│   ├── agent/
│   ├── rag/
│   └── tools/
├── tests/
│   ├── unit/
│   │   ├── test_llm.py
│   │   ├── test_agent.py
│   │   └── test_rag.py
│   ├── integration/
│   │   ├── test_rag_integration.py
│   │   └── test_tool_integration.py
│   ├── e2e/
│   │   ├── test_chat_flow.py
│   │   └── test_agent_workflow.py
│   ├── safety/
│   │   ├── test_harmful_content.py
│   │   └── test_jailbreaks.py
│   ├── fixtures/
│   │   ├── golden_dataset.jsonl
│   │   └── llm_responses.py
│   └── conftest.py
├── scripts/
│   ├── regression_test.py
│   └── evaluate_model.py
└── pyproject.toml
```

### Import Conventions

```python
# tests/unit/test_llm.py
from myapp.llm import LLMClient, Tokenizer

# tests/integration/test_rag.py
from myapp.rag import RAGPipeline

# Use absolute imports within tests/
```

---

## Fixture Scoping and Cleanup

### Description

Choose fixture scopes to balance speed and isolation. Always clean up resources.

### Fixture Scopes

```python
# Function: fresh for every test (most isolated)
@pytest.fixture(scope="function")
def db_session():
    session = Session()
    yield session
    session.close()

# Class: shared within test class
@pytest.fixture(scope="class")
def search_index():
    index = SearchIndex()
    index.add_documents(load_test_docs())
    yield index
    index.cleanup()

# Module: shared within test module
@pytest.fixture(scope="module")
def llm_client():
    client = LLMClient(model="gpt-3.5-turbo")
    yield client
    client.close()

# Session: shared across all tests (fastest)
@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

### Cleanup Patterns

```python
@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test content")
    yield file
    if file.exists():
        file.unlink()

@pytest.fixture
def mock_api():
    server = MockAPIServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(autouse=True)
def cleanup_globals():
    original = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original)
```

---

## Environment Setup

### Description

Test environments must be reproducible and consistent across CI and local development.

### Environment Configuration

```python
# conftest.py
import os
import pytest

def pytest_configure(config):
    os.environ["ENV"] = "test"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["LLM_API_KEY"] = os.getenv("TEST_LLM_API_KEY", "sk-test-key")
    os.environ["LOG_LEVEL"] = "WARNING"

@pytest.fixture(scope="session")
def env():
    return {
        "model": os.getenv("TEST_MODEL", "gpt-3.5-turbo"),
        "api_key": os.getenv("TEST_LLM_API_KEY"),
        "database_url": "sqlite:///:memory:",
        "redis_url": os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")
    }
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "safety: marks safety tests",
    "regression: marks regression tests"
]
addopts = "-v --tb=short --strict-markers"
```

---

## Secrets and Credentials

### Description

Never hardcode secrets in tests. Use environment variables, vault, or CI secrets.

### Bad Practices

```python
# BAD: Hardcoded credentials
api_key = "sk-proj-1234567890abcdef"

# BAD: Credentials in test files
client = LLMClient(api_key="sk-live-secret")
```

### Good Practices

```python
# GOOD: Environment variables
api_key = os.environ["TEST_LLM_API_KEY"]
assert api_key, "TEST_LLM_API_KEY not set"

# GOOD: CI secrets
# In GitHub Actions:
# env:
#   TEST_LLM_API_KEY: ${{ secrets.TEST_LLM_API_KEY }}

# GOOD: Dedicated test credentials
TEST_CREDS = {
    "api_key": os.getenv("TEST_API_KEY"),
    "db_password": os.getenv("TEST_DB_PASSWORD")
}

def get_test_client():
    return LLMClient(api_key=TEST_CREDS["api_key"])
```

### Example: Secure Credential Handling

```python
# conftest.py
import os
import pytest

@pytest.fixture(scope="session")
def credentials():
    creds = {
        "llm_api_key": os.getenv("TEST_LLM_API_KEY"),
        "db_url": os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:"),
        "redis_url": os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")
    }
    
    missing = [k for k, v in creds.items() if not v]
    if missing:
        pytest.skip(f"Missing credentials: {', '.join(missing)}")
    
    return creds
```

---

## Parallel Test Execution

### Description

Parallelize tests to reduce CI time, but ensure isolation.

### pytest-xdist

```bash
# Run tests across 4 CPUs
pytest tests/ -n 4

# Auto-detect CPU count
pytest tests/ -n auto
```

### Ensuring Isolation

```python
# Bad: Shared state causes conflicts
db_connection = connect()

def test_a():
    db_connection.execute("INSERT ...")

def test_b():
    db_connection.execute("INSERT ...")  # Conflicts with test_a

# Good: Isolated fixtures
@pytest.fixture
def db():
    conn = connect()
    yield conn
    conn.close()

def test_a(db):
    db.execute("INSERT ...")

def test_b(db):
    db.execute("INSERT ...")  # Independent fixture
```

### AI-Specific Considerations

```python
# AI tests may need isolation due to:
# 1. Rate limiting
# 2. Session state
# 3. Global models

@pytest.fixture
def isolated_llm_client():
    client = LLMClient(api_key=os.getenv("TEST_LLM_API_KEY"))
    yield client
    client.reset_rate_limit()

@pytest.fixture
def isolated_session():
    session_id = str(uuid.uuid4())
    yield session_id
    cleanup_session(session_id)
```

---

## Test Reporting and Diagnostics

### Description

Rich test reports accelerate debugging. Configure pytest for detailed output.

### pytest Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = 
    -v
    --tb=short
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=xml
markers =
    slow: slow tests
    integration: integration tests
    safety: safety tests
```

### Example: Detailed Failure Output

```python
def test_with_detailed_message():
    response = call_llm("What is the capital of France?")
    
    expected = ["Paris", "France"]
    actual = response.lower()
    
    missing = [e for e in expected if e not in actual]
    
    assert not missing, f"Missing keywords {missing} in response: {response}"
```

### Custom Reporters

```python
class LLMTestReporter:
    def __init__(self):
        self.results = []
    
    def add_result(self, test_name, passed, details):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed/total:.1%}" if total > 0 else "N/A",
            "results": self.results
        }
```

---

## Debugging Failing Tests

### Description

AI test failures require specialized debugging approaches.

### Common Issues and Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Non-determinism | Test passes sometimes | Use temperature=0, check seeds |
| Flaky assertions | Intermittent failures | Use statistical thresholds |
| Slow tests | CI timeouts | Profile, mock, or skip |
| API errors | 429/500 responses | Check rate limits, add retries |
| Hallucinations | Wrong factual answers | Use exact match for facts |
| Context overflow | Token limit errors | Check max_tokens settings |

### Example: Debug Helper

```python
def debug_llm_test(prompt, expected, actual):
    print("=== LLM Test Debug ===")
    print(f"Prompt: {prompt}")
    print(f"Expected (contains): {expected}")
    print(f"Actual: {actual}")
    print(f"Match: {expected.lower() in actual.lower()}")
    print(f"Length: {len(actual)}")
    print(f"First 200 chars: {actual[:200]}")
    print("=" * 40)

def test_with_debug():
    response = call_llm("What is the capital of France?")
    expected = "Paris"
    
    if expected.lower() not in response.lower():
        debug_llm_test("What is the capital of France?", expected, response)
    
    assert expected.lower() in response.lower(), "Expected 'Paris' in response"
```

### Example: Logging for Debugging

```python
import logging

logger = logging.getLogger(__name__)

def test_with_logging():
    logger.info("Starting test")
    response = call_llm("Test prompt")
    logger.info(f"Response: {response[:200]}")
    
    assert "expected" in response.lower()
```

### Debug Checklist

- [ ] Check API key is set and valid
- [ ] Verify model name is correct
- [ ] Check for rate limiting
- [ ] Inspect full error tracebacks
- [ ] Review recent prompt changes
- [ ] Run test with `pytest -s` to see prints
- [ ] Use `pytest --pdb` to drop into debugger on failure
- [ ] Check model version (gpt-3.5 vs gpt-4)

---

## Related Files

- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Examples](./examples.md)
- [Advanced](./advanced.md)
- [Troubleshooting](./troubleshooting.md)
