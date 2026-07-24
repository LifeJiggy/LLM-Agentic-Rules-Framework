# Cost Management Fundamentals for LLM & Agentic Systems

## Table of Contents

1. [Introduction](#introduction)
2. [Core Cost Drivers](#core-cost-drivers)
3. [Cost Attribution](#cost-attribution)
4. [Budgeting Framework](#budgeting-framework)
5. [Cost Forecasting](#cost-forecasting)
6. [Cost Optimization Strategies](#cost-optimization-strategies)
7. [Cost Monitoring Architecture](#cost-monitoring-architecture)
8. [Key Metrics and KPIs](#key-metrics-and-kpis)
9. [Cost Governance](#cost-governance)
10. [Summary](#summary)

---

## Introduction

Cost management for LLM (Large Language Model) and agentic AI systems represents a critical operational discipline that directly impacts the sustainability, scalability, and profitability of AI-powered applications. Unlike traditional software systems where costs are primarily compute-bound, LLM systems introduce unique cost dimensions including token-based pricing, inference latency costs, and multi-model orchestration expenses.

### Why Cost Management Matters

The economics of LLM systems differ fundamentally from traditional cloud workloads:

| Traditional Cloud Workloads | LLM/Agentic Workloads |
|---------------------------|------------------------|
| Predictable compute cycles | Variable token consumption |
| Linear scaling | Non-linear cost growth |
| Infrastructure-based pricing | API-based + infrastructure pricing |
| One-time deployment costs | Ongoing inference costs |
| Limited external service dependencies | Multiple API dependencies |

### The Cost Challenge

LLM costs can escalate rapidly due to several factors:

1. **Token Economics**: Every input and output token incurs costs, and agentic systems may consume thousands of tokens per user interaction
2. **Multi-Model Orchestration**: Complex workflows may invoke multiple models (GPT-4, Claude, specialized fine-tuned models) in sequence
3. **Retry and Error Costs**: Failed requests and retries add to baseline costs without delivering value
4. **Context Window Management**: Large context windows consume more tokens but may be necessary for accuracy
5. **Real-Time Requirements**: Streaming responses and low-latency requirements may necessitate premium pricing tiers

### Cost Management Principles

Effective cost management follows these core principles:

```
Principle 1: Visibility - You cannot manage what you cannot measure
Principle 2: Attribution - Every cost must be traceable to a source
Principle 3: Accountability - Costs must be owned by responsible teams
Principle 4: Optimization - Continuous improvement in cost efficiency
Principle 5: Governance - Policies and controls to prevent cost overruns
```

---

## Core Cost Drivers

Understanding cost drivers is essential for effective cost management. LLM and agentic systems have multiple interconnected cost dimensions.

### 1. Model API Costs

Model API costs are typically the largest cost component for LLM systems. These costs are driven by token consumption.

#### Token Pricing Models

```yaml
# Token Pricing Structure
token_pricing:
  providers:
    openai:
      models:
        gpt-4:
          input_per_1k_tokens: 0.03
          output_per_1k_tokens: 0.06
        gpt-4-turbo:
          input_per_1k_tokens: 0.01
          output_per_1k_tokens: 0.03
        gpt-3.5-turbo:
          input_per_1k_tokens: 0.0005
          output_per_1k_tokens: 0.0015
        gpt-4o:
          input_per_1k_tokens: 0.005
          output_per_1k_tokens: 0.015
    anthropic:
      models:
        claude-3-opus:
          input_per_1k_tokens: 0.015
          output_per_1k_tokens: 0.075
        claude-3-sonnet:
          input_per_1k_tokens: 0.003
          output_per_1k_tokens: 0.015
        claude-3-haiku:
          input_per_1k_tokens: 0.00025
          output_per_1k_tokens: 0.00125
```

#### Token Cost Calculation Formula

```
Total Model Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price) + (Cached Tokens × Cache Price)

Where:
- Input Tokens = Sum of all input tokens across requests
- Output Tokens = Sum of all output tokens across requests
- Cached Tokens = Tokens served from cache (typically 50-90% discount)
```

#### Example Cost Calculation

```python
# Token Cost Calculator
def calculate_model_cost(
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    input_price_per_1k: float = 0.03,
    output_price_per_1k: float = 0.06,
    cache_price_per_1k: float = 0.003
) -> float:
    """
    Calculate the total cost for a model API call.
    
    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        cached_tokens: Number of tokens served from cache
        input_price_per_1k: Cost per 1K input tokens
        output_price_per_1k: Cost per 1K output tokens
        cache_price_per_1k: Cost per 1K cached tokens
    
    Returns:
        Total cost in USD
    """
    input_cost = (input_tokens / 1000) * input_price_per_1k
    output_cost = (output_tokens / 1000) * output_price_per_1k
    cache_cost = (cached_tokens / 1000) * cache_price_per_1k
    
    return input_cost + output_cost + cache_cost

# Example usage
cost = calculate_model_cost(
    input_tokens=2500,
    output_tokens=1000,
    cached_tokens=500
)
print(f"Total cost: ${cost:.6f}")  # Output: Total cost: $0.136500
```

### 2. Compute Infrastructure Costs

Infrastructure costs include servers, GPUs, memory, and storage required to run LLM systems.

#### Compute Cost Components

```yaml
compute_costs:
  gpu_instances:
    nvidia_a100:
      hourly_rate: 3.50
      memory_gb: 80
      suitable_for: "Large model training, inference"
    nvidia_h100:
      hourly_rate: 5.00
      memory_gb: 80
      suitable_for: "High-performance training, batch inference"
    nvidia_t4:
      hourly_rate: 0.35
      memory_gb: 16
      suitable_for: "Light inference, development"
  
  cpu_instances:
    general_purpose:
      hourly_rate: 0.50
      memory_gb: 32
      suitable_for: "Data preprocessing, orchestration"
    compute_optimized:
      hourly_rate: 1.00
      memory_gb: 16
      suitable_for: "CPU inference, parallel processing"
  
  memory_instances:
    memory_optimized:
      hourly_rate: 2.00
      memory_gb: 128
      suitable_for: "Large context processing, caching"
```

#### Infrastructure Cost Formula

```
Infrastructure Cost = Σ(Instance Hours × Hourly Rate) + Storage Costs + Network Costs + Data Transfer Costs

Where:
- Instance Hours = Number of instances × Hours running
- Storage Costs = GB stored × GB-month price
- Network Costs = GB transferred × GB price
- Data Transfer Costs = External API calls × per-call price
```

### 3. Storage Costs

Storage costs include databases, file storage, and caching layers required for LLM systems.

#### Storage Cost Components

```yaml
storage_costs:
  databases:
    postgresql:
      cost_per_gb_month: 0.10
      use_case: "Structured data, user sessions"
    mongodb:
      cost_per_gb_month: 0.10
      use_case: "Document storage, embeddings"
    redis:
      cost_per_gb_month: 0.20
      use_case: "Caching, session management"
  
  file_storage:
    s3_standard:
      cost_per_gb_month: 0.023
      use_case: "Documents, model artifacts"
    s3_ia:
      cost_per_gb_month: 0.0125
      use_case: "Infrequent access data"
    s3_glacier:
      cost_per_gb_month: 0.004
      use_case: "Archival, compliance data"
  
  vector_databases:
    pinecone:
      cost_per_gb_month: 0.30
      use_case: "Vector embeddings, semantic search"
    weaviate:
      cost_per_gb_month: 0.25
      use_case: "Vector embeddings, graph queries"
```

### 4. Network and Data Transfer Costs

Network costs include data transfer between services, regions, and external APIs.

```yaml
network_costs:
  data_transfer:
    aws:
      same_region: 0.01  # per GB
      cross_region: 0.02  # per GB
      internet: 0.09  # per GB
    azure:
      same_region: 0.01  # per GB
      cross_region: 0.02  # per GB
      internet: 0.087  # per GB
    gcp:
      same_region: 0.01  # per GB
      cross_region: 0.02  # per GB
      internet: 0.12  # per GB
  
  api_calls:
    rest_api:
      cost_per_1000_calls: 0.01
    graphql:
      cost_per_1000_calls: 0.015
    websocket:
      cost_per_1000_connections: 0.05
```

### 5. Monitoring and Observability Costs

Observability costs include logging, metrics, tracing, and alerting infrastructure.

```yaml
monitoring_costs:
  logging:
    cloudwatch:
      cost_per_gb: 0.50
      retention_days: 30
    elasticsearch:
      cost_per_gb_month: 0.10
      retention_days: 90
  
  metrics:
    prometheus:
      cost_per_metrics: 0.10  # per metric series
    datadog:
      cost_per_host_month: 15.00
      cost_per_metrics: 0.05  # per metric series
  
  tracing:
    jaeger:
      cost_per_trace: 0.001
    datadog_apm:
      cost_per_host_month: 31.00
```

---

## Cost Attribution

Cost attribution is the practice of assigning costs to specific business units, teams, applications, or features. This is critical for understanding which components drive costs and for making informed optimization decisions.

### Cost Attribution Models

#### 1. Tag-Based Attribution

Tags are key-value pairs applied to resources to enable cost allocation.

```yaml
cost_tags:
  required_tags:
    - key: "environment"
      values: ["production", "staging", "development"]
      description: "Deployment environment"
    
    - key: "team"
      values: ["ml-engineering", "platform", "data-science"]
      description: "Responsible team"
    
    - key: "application"
      values: ["chatbot", "content-generation", "code-assist"]
      description: "Application name"
    
    - key: "cost-center"
      values: ["cc-001", "cc-002", "cc-003"]
      description: "Financial cost center"
    
    - key: "project"
      values: ["project-alpha", "project-beta", "project-gamma"]
      description: "Project identifier"
  
  optional_tags:
    - key: "model-version"
      values: ["gpt-4", "gpt-4-turbo", "claude-3-opus"]
      description: "LLM model version"
    
    - key: "workload-type"
      values: ["inference", "training", "batch-processing"]
      description: "Type of workload"
    
    - key: "priority"
      values: ["critical", "high", "medium", "low"]
      description: "Business priority level"
```

#### 2. Service-Based Attribution

Costs attributed to specific services or microservices.

```yaml
service_attribution:
  services:
    - name: "chat-gateway"
      cost_category: "api-management"
      cost_drivers: ["api_calls", "authentication", "rate_limiting"]
    
    - name: "llm-router"
      cost_category: "model-inference"
      cost_drivers: ["model_calls", "token_usage", "caching"]
    
    - name: "content-processor"
      cost_category: "data-processing"
      cost_drivers: ["compute", "storage", "network"]
    
    - name: "vector-store"
      cost_category: "data-storage"
      cost_drivers: ["storage", "queries", "embedding_generation"]
    
    - name: "embedding-service"
      cost_category: "model-inference"
      cost_drivers: ["model_calls", "token_usage", "batch_processing"]
```

#### 3. User-Based Attribution

Costs attributed to individual users or user segments.

```yaml
user_attribution:
  user_tiers:
    - tier: "free"
      monthly_cost_limit: 0.10
      features: ["basic_chat", "limited_tokens"]
    
    - tier: "pro"
      monthly_cost_limit: 5.00
      features: ["advanced_chat", "code_generation", "analysis"]
    
    - tier: "enterprise"
      monthly_cost_limit: 50.00
      features: ["all_features", "priority_support", "custom_models"]
  
  cost_allocation_rules:
    - rule: "per_user"
      description: "Costs divided equally among active users"
      formula: "total_cost / active_users"
    
    - rule: "usage_based"
      description: "Costs allocated based on token consumption"
      formula: "user_tokens / total_tokens * total_cost"
    
    - rule: "feature_based"
      description: "Costs allocated based on feature usage"
      formula: "feature_cost * user_feature_usage / feature_total_usage"
```

### Cost Attribution Implementation

```python
# Cost Attribution Engine
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import json

@dataclass
class CostRecord:
    """Represents a single cost record for attribution."""
    timestamp: datetime
    resource_id: str
    resource_type: str
    amount: float
    tags: Dict[str, str]
    metadata: Optional[Dict[str, str]] = None

class CostAttributionEngine:
    """Engine for attributing costs to business entities."""
    
    def __init__(self):
        self.cost_records: List[CostRecord] = []
        self.attribution_rules: Dict[str, callable] = {}
    
    def add_cost_record(self, record: CostRecord):
        """Add a cost record for attribution."""
        self.cost_records.append(record)
    
    def attribute_by_tags(self, tag_key: str) -> Dict[str, float]:
        """Attribute costs by a specific tag."""
        attribution = {}
        
        for record in self.cost_records:
            tag_value = record.tags.get(tag_key, "untagged")
            attribution[tag_value] = attribution.get(tag_value, 0) + record.amount
        
        return attribution
    
    def attribute_by_service(self) -> Dict[str, float]:
        """Attribute costs by service."""
        return self.attribute_by_tags("service")
    
    def attribute_by_team(self) -> Dict[str, float]:
        """Attribute costs by team."""
        return self.attribute_by_tags("team")
    
    def attribute_by_environment(self) -> Dict[str, float]:
        """Attribute costs by environment."""
        return self.attribute_by_tags("environment")
    
    def calculate_cost_per_user(self, user_activity: Dict[str, int]) -> Dict[str, float]:
        """Calculate cost per user based on activity."""
        total_tokens = sum(user_activity.values())
        total_cost = sum(record.amount for record in self.cost_records)
        
        cost_per_user = {}
        for user_id, tokens in user_activity.items():
            cost_per_user[user_id] = (tokens / total_tokens) * total_cost
        
        return cost_per_user
    
    def generate_attribution_report(self) -> Dict:
        """Generate comprehensive attribution report."""
        return {
            "total_cost": sum(record.amount for record in self.cost_records),
            "by_service": self.attribute_by_service(),
            "by_team": self.attribute_by_team(),
            "by_environment": self.attribute_by_environment(),
            "record_count": len(self.cost_records),
            "timestamp": datetime.now().isoformat()
        }

# Example usage
engine = CostAttributionEngine()

# Add sample cost records
records = [
    CostRecord(
        timestamp=datetime.now(),
        resource_id="api-gateway-001",
        resource_type="api_gateway",
        amount=150.00,
        tags={"team": "ml-engineering", "service": "chat-gateway", "environment": "production"}
    ),
    CostRecord(
        timestamp=datetime.now(),
        resource_id="llm-router-001",
        resource_type="compute",
        amount=500.00,
        tags={"team": "ml-engineering", "service": "llm-router", "environment": "production"}
    ),
    CostRecord(
        timestamp=datetime.now(),
        resource_id="vector-store-001",
        resource_type="database",
        amount=75.00,
        tags={"team": "data-science", "service": "vector-store", "environment": "production"}
    ),
]

for record in records:
    engine.add_cost_record(report)

# Generate report
report = engine.generate_attribution_report()
print(json.dumps(report, indent=2))
```

---

## Budgeting Framework

A robust budgeting framework provides financial guardrails for LLM systems, preventing unexpected cost overruns while enabling innovation.

### Budget Types

#### 1. Monthly Budgets

```yaml
monthly_budgets:
  total_budget: 10000.00
  
  allocations:
    model_api_costs: 6000.00  # 60% of total
    compute_infrastructure: 2500.00  # 25% of total
    storage_costs: 1000.00  # 10% of total
    monitoring_costs: 500.00  # 5% of total
  
  teams:
    ml-engineering:
      budget: 5000.00
      allocation:
        model_api: 3000.00
        compute: 1500.00
        storage: 400.00
        monitoring: 100.00
    
    data-science:
      budget: 3000.00
      allocation:
        model_api: 1500.00
        compute: 1000.00
        storage: 400.00
        monitoring: 100.00
    
    platform:
      budget: 2000.00
      allocation:
        model_api: 1500.00
        compute: 0.00
        storage: 200.00
        monitoring: 300.00
```

#### 2. Project-Based Budgets

```yaml
project_budgets:
  projects:
    - name: "chatbot-v2"
      budget: 3000.00
      duration: "3 months"
      total_budget: 9000.00
      milestones:
        - name: "MVP"
          budget: 1000.00
          timeline: "Month 1"
        
        - name: "Beta"
          budget: 2000.00
          timeline: "Month 2"
        
        - name: "Production"
          budget: 6000.00
          timeline: "Month 3"
    
    - name: "content-generator"
      budget: 2000.00
      duration: "2 months"
      total_budget: 4000.00
      milestones:
        - name: "Prototype"
          budget: 500.00
          timeline: "Month 1"
        
        - name: "Launch"
          budget: 3500.00
          timeline: "Month 2"
```

#### 3. Feature-Based Budgets

```yaml
feature_budgets:
  features:
    - name: "text-generation"
      monthly_budget: 2000.00
      cost_drivers: ["token_usage", "model_calls"]
      optimization_target: 0.70  # 70% utilization target
    
    - name: "code-assist"
      monthly_budget: 1500.00
      cost_drivers: ["token_usage", "model_calls", "caching"]
      optimization_target: 0.65
    
    - name: "image-analysis"
      monthly_budget: 1000.00
      cost_drivers: ["api_calls", "compute"]
      optimization_target: 0.60
    
    - name: "embedding-generation"
      monthly_budget: 500.00
      cost_drivers: ["model_calls", "storage"]
      optimization_target: 0.80
```

### Budget Alerts

```yaml
budget_alerts:
  thresholds:
    - name: "warning"
      percentage: 75
      notification:
        channels: ["email", "slack"]
        recipients: ["team-lead@company.com"]
    
    - name: "critical"
      percentage: 90
      notification:
        channels: ["email", "slack", "pagerduty"]
        recipients: ["team-lead@company.com", "finance@company.com"]
        escalation: true
    
    - name: "emergency"
      percentage: 100
      notification:
        channels: ["email", "slack", "pagerduty", "sms"]
        recipients: ["team-lead@company.com", "finance@company.com", "cto@company.com"]
        escalation: true
        action: "notify_management"
    
    - name: "overrun"
      percentage: 110
      notification:
        channels: ["email", "slack", "pagerduty", "sms"]
        recipients: ["team-lead@company.com", "finance@company.com", "cto@company.com", "ceo@company.com"]
        escalation: true
        action: "immediate_review"
  
  auto_actions:
    - trigger: "critical"
      action: "reduce_non_critical_workloads"
      threshold: 90
    
    - trigger: "emergency"
      action: "scale_down_development"
      threshold: 100
    
    - trigger: "overrun"
      action: "pause_non_essential_features"
      threshold: 110
```

---

## Cost Forecasting

Cost forecasting predicts future expenses based on historical data, usage patterns, and business projections.

### Forecasting Methods

#### 1. Linear Regression

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Tuple

class CostForecaster:
    """Forecast costs using various methods."""
    
    def __init__(self):
        self.historical_data: List[Tuple[int, float]] = []
    
    def add_data_point(self, day: int, cost: float):
        """Add a historical data point."""
        self.historical_data.append((day, cost))
    
    def linear_regression_forecast(self, days_ahead: int) -> List[float]:
        """Forecast using linear regression."""
        if len(self.historical_data) < 2:
            raise ValueError("Need at least 2 data points for forecasting")
        
        days = np.array([d[0] for d in self.historical_data]).reshape(-1, 1)
        costs = np.array([d[1] for d in self.historical_data])
        
        model = LinearRegression()
        model.fit(days, costs)
        
        future_days = np.array(range(
            max(days) + 1, 
            max(days) + days_ahead + 1
        )).reshape(-1, 1)
        
        predictions = model.predict(future_days)
        return predictions.tolist()
    
    def moving_average_forecast(self, window_size: int, days_ahead: int) -> List[float]:
        """Forecast using moving average."""
        if len(self.historical_data) < window_size:
            raise ValueError(f"Need at least {window_size} data points")
        
        costs = [d[1] for d in self.historical_data]
        forecasts = []
        
        for _ in range(days_ahead):
            recent_avg = sum(costs[-window_size:]) / window_size
            forecasts.append(recent_avg)
            costs.append(recent_avg)
        
        return forecasts
    
    def exponential_smoothing_forecast(self, alpha: float, days_ahead: int) -> List[float]:
        """Forecast using exponential smoothing."""
        if len(self.historical_data) < 1:
            raise ValueError("Need at least 1 data point")
        
        costs = [d[1] for d in self.historical_data]
        forecasts = []
        
        last_forecast = costs[0]
        for cost in costs:
            last_forecast = alpha * cost + (1 - alpha) * last_forecast
        
        for _ in range(days_ahead):
            forecasts.append(last_forecast)
        
        return forecasts

# Example usage
forecaster = CostForecaster()

# Add historical data (day, cost)
historical_data = [
    (1, 150.00), (2, 160.00), (3, 155.00), (4, 170.00),
    (5, 165.00), (6, 180.00), (7, 175.00), (8, 190.00),
    (9, 185.00), (10, 200.00)
]

for day, cost in historical_data:
    forecaster.add_data_point(day, cost)

# Generate forecasts
linear_forecast = forecaster.linear_regression_forecast(7)
ma_forecast = forecaster.moving_average_forecast(3, 7)
es_forecast = forecaster.exponential_smoothing_forecast(0.3, 7)

print("Linear Regression Forecast:", linear_forecast)
print("Moving Average Forecast:", ma_forecast)
print("Exponential Smoothing Forecast:", es_forecast)
```

#### 2. Seasonal Forecasting

```python
from datetime import datetime, timedelta
from typing import Dict, List
import numpy as np

class SeasonalCostForecaster:
    """Forecast costs with seasonal patterns."""
    
    def __init__(self):
        self.daily_costs: Dict[str, float] = {}
        self.weekly_pattern: Dict[int, float] = {}
        self.monthly_pattern: Dict[int, float] = {}
    
    def add_cost_data(self, date: datetime, cost: float):
        """Add cost data for a specific date."""
        key = date.strftime("%Y-%m-%d")
        self.daily_costs[key] = cost
        
        # Update patterns
        weekday = date.weekday()
        self.weekly_pattern[weekday] = (
            self.weekly_pattern.get(weekday, 0) + cost
        ) / 2
        
        month = date.month
        self.monthly_pattern[month] = (
            self.monthly_pattern.get(month, 0) + cost
        ) / 2
    
    def forecast_next_week(self) -> List[float]:
        """Forecast costs for the next week."""
        forecasts = []
        today = datetime.now()
        
        for i in range(7):
            future_date = today + timedelta(days=i + 1)
            weekday = future_date.weekday()
            
            base_forecast = sum(self.daily_costs.values()) / len(self.daily_costs)
            weekly_adjustment = self.weekly_pattern.get(weekday, 1.0)
            
            forecast = base_forecast * weekly_adjustment
            forecasts.append(forecast)
        
        return forecasts
    
    def forecast_next_month(self) -> List[float]:
        """Forecast costs for the next month."""
        forecasts = []
        today = datetime.now()
        
        for i in range(30):
            future_date = today + timedelta(days=i + 1)
            weekday = future_date.weekday()
            month = future_date.month
            
            base_forecast = sum(self.daily_costs.values()) / len(self.daily_costs)
            weekly_adjustment = self.weekly_pattern.get(weekday, 1.0)
            monthly_adjustment = self.monthly_pattern.get(month, 1.0)
            
            forecast = base_forecast * weekly_adjustment * monthly_adjustment
            forecasts.append(forecast)
        
        return forecasts
    
    def calculate_confidence_intervals(
        self, 
        forecasts: List[float], 
        confidence: float = 0.95
    ) -> List[Tuple[float, float]]:
        """Calculate confidence intervals for forecasts."""
        if len(self.daily_costs) < 7:
            raise ValueError("Need at least 7 days of data for confidence intervals")
        
        costs = list(self.daily_costs.values())
        std_dev = np.std(costs)
        
        # Z-score for confidence level
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        intervals = []
        for forecast in forecasts:
            margin = z * std_dev
            intervals.append((forecast - margin, forecast + margin))
        
        return intervals

# Example usage
forecaster = SeasonalCostForecaster()

# Add historical data
import random
for i in range(30):
    date = datetime.now() - timedelta(days=30-i)
    cost = 150 + random.uniform(-20, 20)  # Base cost with variation
    forecaster.add_cost_data(date, cost)

# Generate forecasts
weekly_forecast = forecaster.forecast_next_week()
monthly_forecast = forecaster.forecast_next_month()
confidence_intervals = forecaster.calculate_confidence_intervals(monthly_forecast)

print("Weekly Forecast:", weekly_forecast)
print("Monthly Forecast:", monthly_forecast)
print("Confidence Intervals:", confidence_intervals)
```

---

## Cost Optimization Strategies

Cost optimization for LLM systems involves multiple strategies to reduce expenses while maintaining performance and quality.

### 1. Token Optimization

```yaml
token_optimization:
  strategies:
    - name: "prompt_compression"
      description: "Reduce prompt length while maintaining context"
      potential_savings: "20-40%"
      implementation:
        - "Remove unnecessary whitespace and formatting"
        - "Use abbreviations for common terms"
        - "Compress examples and instructions"
    
    - name: "response_optimization"
      description: "Optimize response generation to reduce output tokens"
      potential_savings: "15-30%"
      implementation:
        - "Set max_tokens appropriately"
        - "Use stop sequences to prevent verbose responses"
        - "Implement response post-processing"
    
    - name: "context_management"
      description: "Manage context window efficiently"
      potential_savings: "10-25%"
      implementation:
        - "Implement sliding window for long conversations"
        - "Summarize older context"
        - "Use retrieval-augmented generation (RAG) instead of full context"
    
    - name: "caching"
      description: "Cache frequent queries and responses"
      potential_savings: "30-60%"
      implementation:
        - "Implement semantic caching"
        - "Cache similar queries"
        - "Use embedding similarity for cache lookup"
```

### 2. Model Selection Optimization

```yaml
model_selection:
  strategy: "right_model_for_task"
  decision_matrix:
    - task: "simple_classification"
      recommended_model: "gpt-3.5-turbo"
      cost_per_1k_tokens: 0.0015
      accuracy_tradeoff: "minimal"
    
    - task: "complex_reasoning"
      recommended_model: "gpt-4"
      cost_per_1k_tokens: 0.06
      accuracy_tradeoff: "none"
    
    - task: "code_generation"
      recommended_model: "claude-3-opus"
      cost_per_1k_tokens: 0.075
      accuracy_tradeoff: "none"
    
    - task: "content_writing"
      recommended_model: "gpt-4-turbo"
      cost_per_1k_tokens: 0.03
      accuracy_tradeoff: "minimal"
    
    - task: "data_extraction"
      recommended_model: "gpt-3.5-turbo"
      cost_per_1k_tokens: 0.0015
      accuracy_tradeoff: "moderate"
```

### 3. Infrastructure Optimization

```yaml
infrastructure_optimization:
  strategies:
    - name: "auto_scaling"
      description: "Scale resources based on demand"
      implementation:
        min_instances: 1
        max_instances: 10
        target_utilization: 70
        scale_up_threshold: 80
        scale_down_threshold: 30
    
    - name: "reserved_instances"
      description: "Reserve capacity for predictable workloads"
      potential_savings: "30-60%"
      implementation:
        - "Analyze usage patterns"
        - "Reserve for steady-state workloads"
        - "Use on-demand for variable workloads"
    
    - name: "spot_instances"
      description: "Use spot instances for fault-tolerant workloads"
      potential_savings: "60-80%"
      implementation:
        - "Identify interruptible workloads"
        - "Implement checkpointing"
        - "Handle spot interruptions gracefully"
    
    - name: "resource_scheduling"
      description: "Schedule resources based on usage patterns"
      implementation:
        - "Scale down during off-hours"
        - "Pause development environments"
        - "Schedule batch processing during off-peak"
```

---

## Cost Monitoring Architecture

A comprehensive cost monitoring architecture provides real-time visibility into costs and enables proactive management.

### Architecture Components

```yaml
cost_monitoring_architecture:
  data_collection:
    sources:
      - "cloud_provider_billing_apis"
      - "llm_api_usage_apis"
      - "infrastructure_metrics"
      - "application_logs"
      - "custom_cost_events"
    
    collection_frequency:
      real_time: "per_request"
      batch: "hourly"
      summary: "daily"
  
  data_processing:
    pipeline:
      - name: "ingestion"
        technology: "kafka"
        description: "Real-time event ingestion"
      
      - name: "processing"
        technology: "spark"
        description: "Cost data aggregation and transformation"
      
      - name: "storage"
        technology: "clickhouse"
        description: "Time-series cost data storage"
      
      - name: "analysis"
        technology: "python"
        description: "Cost analysis and anomaly detection"
  
  visualization:
    dashboards:
      - name: "executive_summary"
        description: "High-level cost overview for leadership"
        refresh_frequency: "hourly"
      
      - name: "team_costs"
        description: "Detailed costs by team and project"
        refresh_frequency: "daily"
      
      - name: "real_time_monitoring"
        description: "Real-time cost tracking and alerts"
        refresh_frequency: "real_time"
      
      - name: "forecasting"
        description: "Cost forecasting and trend analysis"
        refresh_frequency: "daily"
  
  alerting:
    channels:
      - "email"
      - "slack"
      - "pagerduty"
      - "webhook"
    
    alert_types:
      - "budget_threshold"
      - "cost_anomaly"
      - "optimization_opportunity"
      - "forecast_deviation"
```

### Monitoring Implementation

```python
import time
from dataclasses import dataclass
from typing import Dict, List, Callable
from datetime import datetime, timedelta
import statistics

@dataclass
class CostAlert:
    """Represents a cost alert."""
    alert_id: str
    severity: str  # warning, critical, emergency
    message: str
    current_cost: float
    threshold: float
    timestamp: datetime
    metadata: Dict = None

class CostMonitor:
    """Real-time cost monitoring system."""
    
    def __init__(self, budget: float, alert_thresholds: Dict[str, float]):
        self.budget = budget
        self.alert_thresholds = alert_thresholds
        self.cost_records: List[Dict] = []
        self.alerts: List[CostAlert] = []
        self.alert_callbacks: List[Callable] = []
    
    def record_cost(self, amount: float, metadata: Dict = None):
        """Record a cost event."""
        record = {
            "amount": amount,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        }
        self.cost_records.append(record)
        
        # Check for alerts
        self._check_alerts()
    
    def _check_alerts(self):
        """Check if any alert thresholds are exceeded."""
        current_cost = self.get_current_period_cost()
        
        for threshold_name, threshold_value in self.alert_thresholds.items():
            if current_cost >= self.budget * threshold_value:
                self._create_alert(threshold_name, current_cost)
    
    def _create_alert(self, severity: str, current_cost: float):
        """Create and trigger a cost alert."""
        alert = CostAlert(
            alert_id=f"alert_{int(time.time())}",
            severity=severity,
            message=f"Cost alert: ${current_cost:.2f} exceeds {severity} threshold",
            current_cost=current_cost,
            threshold=self.budget * self.alert_thresholds[severity],
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # Trigger callbacks
        for callback in self.alert_callbacks:
            callback(alert)
    
    def get_current_period_cost(self) -> float:
        """Get total cost for the current billing period."""
        now = datetime.now()
        period_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return sum(
            record["amount"] for record in self.cost_records
            if record["timestamp"] >= period_start
        )
    
    def get_cost_trend(self, days: int = 7) -> List[float]:
        """Get cost trend for the last N days."""
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        daily_costs = {}
        for record in self.cost_records:
            if record["timestamp"] >= start_date:
                day = record["timestamp"].date()
                daily_costs[day] = daily_costs.get(day, 0) + record["amount"]
        
        return [daily_costs.get(now.date() - timedelta(days=i), 0) 
                for i in range(days-1, -1, -1)]
    
    def detect_anomalies(self, threshold: float = 2.0) -> List[Dict]:
        """Detect cost anomalies using standard deviation."""
        costs = [record["amount"] for record in self.cost_records]
        
        if len(costs) < 10:
            return []
        
        mean_cost = statistics.mean(costs)
        std_cost = statistics.stdev(costs)
        
        anomalies = []
        for record in self.cost_records:
            if abs(record["amount"] - mean_cost) > threshold * std_cost:
                anomalies.append({
                    "amount": record["amount"],
                    "timestamp": record["timestamp"],
                    "deviation": (record["amount"] - mean_cost) / std_cost
                })
        
        return anomalies

# Example usage
monitor = CostMonitor(
    budget=10000.00,
    alert_thresholds={
        "warning": 0.75,
        "critical": 0.90,
        "emergency": 1.00
    }
)

# Add alert callback
def alert_handler(alert: CostAlert):
    print(f"ALERT [{alert.severity.upper()}]: {alert.message}")

monitor.alert_callbacks.append(alert_handler)

# Simulate cost events
import random
for _ in range(100):
    amount = random.uniform(50, 200)
    monitor.record_cost(amount, {"source": "llm_api"})

# Check status
print(f"Current Period Cost: ${monitor.get_current_period_cost():.2f}")
print(f"Cost Trend: {monitor.get_cost_trend(7)}")
print(f"Anomalies Detected: {len(monitor.detect_anomalies())}")
```

---

## Key Metrics and KPIs

Essential metrics for monitoring and optimizing LLM system costs.

### Cost Efficiency Metrics

```yaml
cost_metrics:
  primary_metrics:
    - name: "cost_per_token"
      formula: "total_cost / total_tokens_processed"
      unit: "USD per token"
      target: "< 0.0001"
      description: "Average cost per token processed"
    
    - name: "cost_per_request"
      formula: "total_cost / total_requests"
      unit: "USD per request"
      target: "< 0.01"
      description: "Average cost per API request"
    
    - name: "cost_per_user"
      formula: "total_cost / active_users"
      unit: "USD per user"
      target: "< 1.00"
      description: "Average cost per active user"
    
    - name: "cost_efficiency_ratio"
      formula: "value_generated / total_cost"
      unit: "ratio"
      target: "> 10"
      description: "Value generated per dollar spent"
  
  optimization_metrics:
    - name: "cache_hit_rate"
      formula: "cache_hits / (cache_hits + cache_misses)"
      unit: "percentage"
      target: "> 70%"
      description: "Percentage of requests served from cache"
    
    - name: "token_optimization_rate"
      formula: "tokens_saved / original_tokens"
      unit: "percentage"
      target: "> 30%"
      description: "Percentage of tokens saved through optimization"
    
    - name: "model_selection_accuracy"
      formula: "correct_model_selections / total_selections"
      unit: "percentage"
      target: "> 90%"
      description: "Accuracy of model selection for task complexity"
    
    - name: "cost_reduction_rate"
      formula: "(previous_period_cost - current_period_cost) / previous_period_cost"
      unit: "percentage"
      target: "> 10%"
      description: "Month-over-month cost reduction"
  
  quality_metrics:
    - name: "cost_per_accuracy_point"
      formula: "total_cost / accuracy_score"
      unit: "USD per accuracy point"
      target: "< 100"
      description: "Cost to achieve each percentage point of accuracy"
    
    - name: "cost_per_response_quality"
      formula: "total_cost / quality_score"
      unit: "USD per quality point"
      target: "< 50"
      description: "Cost to achieve each quality score point"
    
    - name: "cost_per_latency_ms"
      formula: "total_cost / average_latency_ms"
      unit: "USD per ms"
      target: "< 0.1"
      description: "Cost efficiency relative to response latency"
```

### KPI Dashboard

```yaml
kpi_dashboard:
  executive_summary:
    metrics:
      - name: "total_monthly_cost"
        value: "$8,500"
        trend: "+5%"
        status: "warning"
        benchmark: "< $10,000"
      
      - name: "cost_per_user"
        value: "$0.85"
        trend: "-10%"
        status: "good"
        benchmark: "< $1.00"
      
      - name: "cost_efficiency"
        value: "12.5x"
        trend: "+15%"
        status: "excellent"
        benchmark: "> 10x"
      
      - name: "budget_utilization"
        value: "85%"
        trend: "+5%"
        status: "warning"
        benchmark: "< 90%"
  
  operational_metrics:
    metrics:
      - name: "cache_hit_rate"
        value: "75%"
        trend: "+10%"
        status: "good"
        benchmark: "> 70%"
      
      - name: "token_optimization"
        value: "35%"
        trend: "+5%"
        status: "good"
        benchmark: "> 30%"
      
      - name: "model_selection_accuracy"
        value: "92%"
        trend: "+2%"
        status: "excellent"
        benchmark: "> 90%"
      
      - name: "cost_reduction_mom"
        value: "12%"
        trend: "+3%"
        status: "excellent"
        benchmark: "> 10%"
```

---

## Cost Governance

Cost governance provides the policies, processes, and controls needed to manage costs effectively across the organization.

### Governance Framework

```yaml
governance_framework:
  policies:
    - name: "budget_approval"
      description: "All new projects must have approved budgets before development"
      requirements:
        - "Budget request form completed"
        - "Cost-benefit analysis provided"
        - "Approval from finance and engineering leadership"
        - "Cost monitoring plan established"
    
    - name: "cost_optimization"
      description: "Regular cost optimization reviews and improvements"
      requirements:
        - "Monthly cost reviews"
        - "Quarterly optimization planning"
        - "Annual cost strategy alignment"
        - "Continuous monitoring and alerting"
    
    - name: "cost_allocation"
      description: "All costs must be properly attributed and allocated"
      requirements:
        - "All resources tagged with required tags"
        - "Cost allocation reports generated monthly"
        - "Chargeback to appropriate teams"
        - "Regular tag compliance audits"
    
    - name: "spending_controls"
      description: "Controls to prevent unauthorized spending"
      requirements:
        - "Spending limits per team/project"
        - "Approval workflows for large purchases"
        - "Real-time monitoring and alerts"
        - "Automatic shutdown for budget overruns"
  
  processes:
    - name: "cost_review_meeting"
      frequency: "weekly"
      participants: ["engineering_leads", "finance", "product"]
      agenda:
        - "Review current spend vs budget"
        - "Discuss optimization opportunities"
        - "Plan for upcoming expenses"
        - "Address any cost concerns"
    
    - name: "optimization_planning"
      frequency: "quarterly"
      participants: ["engineering_leads", "finance", "product", "leadership"]
      agenda:
        - "Review cost trends and patterns"
        - "Identify optimization opportunities"
        - "Plan implementation of cost-saving measures"
        - "Set goals for next quarter"
    
    - name: "budget_planning"
      frequency: "annually"
      participants: ["leadership", "finance", "engineering_leads"]
      agenda:
        - "Review previous year's performance"
        - "Forecast next year's costs"
        - "Allocate budgets to teams/projects"
        - "Set cost efficiency targets"
  
  controls:
    - name: "spending_limits"
      description: "Hard limits on spending per team/project"
      implementation:
        - "Daily spending limits"
        - "Weekly spending limits"
        - "Monthly spending limits"
        - "Quarterly spending limits"
    
    - name: "approval_workflows"
      description: "Approval requirements for large expenses"
      thresholds:
        - amount: 1000
          approvers: ["team_lead"]
        - amount: 5000
          approvers: ["team_lead", "engineering_manager"]
        - amount: 10000
          approvers: ["team_lead", "engineering_manager", "finance"]
        - amount: 50000
          approvers: ["team_lead", "engineering_manager", "finance", "cto"]
    
    - name: "monitoring_and_alerting"
      description: "Real-time monitoring and alerting for cost anomalies"
      implementation:
        - "Real-time cost tracking"
        - "Threshold-based alerts"
        - "Anomaly detection"
        - "Automated responses to cost spikes"
```

### Role-Based Cost Responsibilities

```yaml
cost_responsibilities:
  roles:
    - name: "cto"
      responsibilities:
        - "Overall cost strategy and direction"
        - "Approve large budget requests"
        - "Drive cost optimization culture"
        - "Report to board on cost performance"
      authority:
        - "Approve budgets over $50,000"
        - "Authorize major cost-saving initiatives"
        - "Set organization-wide cost targets"
    
    - name: "engineering_manager"
      responsibilities:
        - "Manage team budgets"
        - "Drive cost optimization within team"
        - "Review and approve cost changes"
        - "Report on team cost performance"
      authority:
        - "Approve budgets up to $50,000"
        - "Authorize team-level cost changes"
        - "Implement cost-saving measures"
    
    - name: "team_lead"
      responsibilities:
        - "Monitor daily costs"
        - "Identify optimization opportunities"
        - "Implement cost-saving measures"
        - "Report cost issues to management"
      authority:
        - "Approve budgets up to $5,000"
        - "Authorize small cost changes"
        - "Implement immediate cost controls"
    
    - name: "developer"
      responsibilities:
        - "Follow cost optimization best practices"
        - "Report cost inefficiencies"
        - "Implement cost-conscious code"
        - "Participate in cost reviews"
      authority:
        - "Flag cost concerns"
        - "Suggest optimization ideas"
        - "Implement approved cost-saving measures"
```

---

## Summary

Effective cost management for LLM and agentic systems requires a comprehensive approach that encompasses:

### Key Takeaways

1. **Understand Cost Drivers**: Know what drives costs in your LLM systems - token consumption, compute, storage, network, and monitoring costs.

2. **Implement Cost Attribution**: Attribute costs to specific teams, projects, and features to understand where money is being spent.

3. **Establish Budgeting Framework**: Create realistic budgets with clear allocation and monitoring.

4. **Forecast Future Costs**: Use historical data and patterns to predict future expenses.

5. **Optimize Continuously**: Implement token optimization, model selection, and infrastructure optimization strategies.

6. **Monitor in Real-Time**: Deploy comprehensive monitoring and alerting systems to catch cost issues early.

7. **Governance is Critical**: Establish policies, processes, and controls to manage costs effectively.

### Cost Management Maturity Model

```yaml
maturity_levels:
  level_1_initial:
    characteristics:
      - "No cost tracking"
      - "Manual budgeting"
      - "Reactive cost management"
    next_steps:
      - "Implement basic cost tracking"
      - "Set up initial budgets"
      - "Establish cost visibility"
  
  level_2_managed:
    characteristics:
      - "Basic cost tracking"
      - "Monthly budget reviews"
      - "Manual optimization"
    next_steps:
      - "Implement automated tracking"
      - "Set up real-time monitoring"
      - "Establish optimization processes"
  
  level_3_defined:
    characteristics:
      - "Automated cost tracking"
      - "Real-time monitoring"
      - "Proactive optimization"
    next_steps:
      - "Implement advanced analytics"
      - "Establish cost governance"
      - "Drive cost optimization culture"
  
  level_4_quantitatively_managed:
    characteristics:
      - "Advanced cost analytics"
      - "Predictive forecasting"
      - "Automated optimization"
    next_steps:
      - "Implement AI-driven optimization"
      - "Establish cost innovation"
      - "Drive industry-leading cost efficiency"
  
  level_5_optimizing:
    characteristics:
      - "AI-driven cost optimization"
      - "Continuous innovation"
      - "Industry-leading efficiency"
    next_steps:
      - "Maintain leadership position"
      - "Drive cost innovation"
      - "Share best practices"
```

### Implementation Checklist

- [ ] Establish cost visibility and tracking
- [ ] Implement cost attribution
- [ ] Set up budgeting and forecasting
- [ ] Deploy monitoring and alerting
- [ ] Implement optimization strategies
- [ ] Establish governance framework
- [ ] Train teams on cost management
- [ ] Continuously improve and optimize

By following these fundamentals, organizations can effectively manage costs for their LLM and agentic systems, ensuring sustainability, scalability, and profitability.
