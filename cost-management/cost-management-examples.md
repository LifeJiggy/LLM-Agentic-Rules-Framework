# Cost Management Examples for LLM & Agentic Systems

## Table of Contents

1. [Introduction](#introduction)
2. [Cost Dashboard Examples](#cost-dashboard-examples)
3. [Budget Alert Examples](#budget-alert-examples)
4. [Optimization Report Examples](#optimization-report-examples)
5. [Chargeback Model Examples](#chargeback-model-examples)
6. [Cost Calculation Examples](#cost-calculation-examples)
7. [Monitoring Configuration Examples](#monitoring-configuration-examples)
8. [Governance Examples](#governance-examples)
9. [Automation Examples](#automation-examples)
10. [Summary](#summary)

---

## Introduction

This document provides practical examples of cost management configurations, dashboards, and implementations for LLM and agentic systems. These examples can be used as templates or references for implementing cost management in your own systems.

### How to Use These Examples

1. **Copy and Modify**: Use these examples as starting points and modify them for your specific needs
2. **Combine Examples**: Mix and match examples to create comprehensive solutions
3. **Scale as Needed**: Adapt examples to your organization's scale and requirements
4. **Test Thoroughly**: Always test configurations before deploying to production

---

## Cost Dashboard Examples

### Executive Cost Dashboard

```yaml
executive_dashboard:
  name: "LLM Cost Executive Dashboard"
  description: "High-level cost overview for leadership"
  refresh_frequency: "hourly"
  widgets:
    - name: "total_monthly_cost"
      type: "metric"
      query: |
        SELECT SUM(cost) as total_cost
        FROM cost_records
        WHERE date >= date_trunc('month', NOW())
      format: "currency"
      threshold:
        warning: 8000
        critical: 10000
    
    - name: "cost_trend"
      type: "line_chart"
      query: |
        SELECT date, SUM(cost) as daily_cost
        FROM cost_records
        WHERE date >= NOW() - INTERVAL '30 days'
        GROUP BY date
        ORDER BY date
      time_range: "30d"
    
    - name: "cost_by_team"
      type: "pie_chart"
      query: |
        SELECT team, SUM(cost) as team_cost
        FROM cost_records
        WHERE date >= date_trunc('month', NOW())
        GROUP BY team
        ORDER BY team_cost DESC
    
    - name: "budget_utilization"
      type: "gauge"
      query: |
        SELECT 
          SUM(cost) as current_spend,
          budget_limit,
          (SUM(cost) / budget_limit * 100) as utilization
        FROM cost_records
        JOIN budgets ON cost_records.budget_id = budgets.id
        WHERE date >= date_trunc('month', NOW())
        GROUP BY budget_limit
      format: "percentage"
      thresholds:
        green: 0-70
        yellow: 70-90
        red: 90-100
    
    - name: "cost_forecast"
      type: "metric"
      query: |
        SELECT 
          SUM(cost) as current_spend,
          SUM(cost) / day(NOW()) * day(last_day(NOW())) as forecast
        FROM cost_records
        WHERE date >= date_trunc('month', NOW())
      format: "currency"
    
    - name: "top_cost_drivers"
      type: "table"
      query: |
        SELECT 
          service,
          SUM(cost) as service_cost,
          COUNT(*) as request_count,
          AVG(cost) as avg_cost_per_request
        FROM cost_records
        WHERE date >= date_trunc('month', NOW())
        GROUP BY service
        ORDER BY service_cost DESC
        LIMIT 10
      columns:
        - "Service"
        - "Cost"
        - "Requests"
        - "Avg Cost/Request"
```

### Team Cost Dashboard

```yaml
team_dashboard:
  name: "LLM Cost Team Dashboard"
  description: "Detailed costs for ML Engineering team"
  refresh_frequency: "daily"
  widgets:
    - name: "team_monthly_cost"
      type: "metric"
      query: |
        SELECT SUM(cost) as team_cost
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= date_trunc('month', NOW())
      format: "currency"
    
    - name: "team_cost_by_project"
      type: "bar_chart"
      query: |
        SELECT project, SUM(cost) as project_cost
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= date_trunc('month', NOW())
        GROUP BY project
        ORDER BY project_cost DESC
    
    - name: "team_cost_by_model"
      type: "pie_chart"
      query: |
        SELECT model, SUM(cost) as model_cost
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= date_trunc('month', NOW())
        GROUP BY model
        ORDER BY model_cost DESC
    
    - name: "team_token_usage"
      type: "line_chart"
      query: |
        SELECT date, SUM(tokens) as daily_tokens
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= NOW() - INTERVAL '30 days'
        GROUP BY date
        ORDER BY date
    
    - name: "team_cost_efficiency"
      type: "metric"
      query: |
        SELECT 
          SUM(cost) as total_cost,
          SUM(tokens) as total_tokens,
          SUM(cost) / SUM(tokens) * 1000 as cost_per_1k_tokens
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= date_trunc('month', NOW())
      format: "currency"
    
    - name: "team_optimization_savings"
      type: "metric"
      query: |
        SELECT 
          SUM(CASE WHEN optimized THEN cost ELSE 0 END) as optimized_cost,
          SUM(CASE WHEN NOT optimized THEN cost ELSE 0 END) as unoptimized_cost,
          SUM(CASE WHEN NOT optimized THEN cost ELSE 0 END) * 0.3 as potential_savings
        FROM cost_records
        WHERE team = 'ml-engineering'
        AND date >= date_trunc('month', NOW())
      format: "currency"
```

### Real-Time Cost Monitoring Dashboard

```yaml
realtime_dashboard:
  name: "LLM Cost Real-Time Dashboard"
  description: "Real-time cost monitoring"
  refresh_frequency: "real_time"
  widgets:
    - name: "current_hour_cost"
      type: "metric"
      query: |
        SELECT SUM(cost) as hourly_cost
        FROM cost_records
        WHERE timestamp >= date_trunc('hour', NOW())
      format: "currency"
      update_interval: "1m"
    
    - name: "cost_per_minute"
      type: "line_chart"
      query: |
        SELECT 
          date_trunc('minute', timestamp) as minute,
          SUM(cost) as minute_cost
        FROM cost_records
        WHERE timestamp >= NOW() - INTERVAL '1 hour'
        GROUP BY minute
        ORDER BY minute
      time_range: "1h"
      update_interval: "1m"
    
    - name: "active_api_calls"
      type: "metric"
      query: |
        SELECT COUNT(*) as active_calls
        FROM cost_records
        WHERE timestamp >= NOW() - INTERVAL '5 minutes'
      format: "number"
      update_interval: "30s"
    
    - name: "cost_anomalies"
      type: "table"
      query: |
        SELECT 
          timestamp,
          service,
          cost,
          'High cost detected' as anomaly
        FROM cost_records
        WHERE cost > (
          SELECT AVG(cost) + 3 * STDDEV(cost)
          FROM cost_records
          WHERE timestamp >= NOW() - INTERVAL '1 hour'
        )
        AND timestamp >= NOW() - INTERVAL '1 hour'
        ORDER BY timestamp DESC
      columns:
        - "Time"
        - "Service"
        - "Cost"
        - "Anomaly"
      update_interval: "1m"
    
    - name: "budget_status"
      type: "gauge"
      query: |
        SELECT 
          SUM(cost) as current_spend,
          budget_limit,
          (SUM(cost) / budget_limit * 100) as utilization
        FROM cost_records
        JOIN budgets ON cost_records.budget_id = budgets.id
        WHERE date >= date_trunc('month', NOW())
        GROUP BY budget_limit
      format: "percentage"
      thresholds:
        green: 0-70
        yellow: 70-90
        red: 90-100
      update_interval: "5m"
```

---

## Budget Alert Examples

### Multi-Level Budget Alerts

```yaml
budget_alerts:
  - name: "warning_alert"
    threshold_percentage: 75
    severity: "warning"
    notification:
      channels:
        - type: "email"
          recipients:
            - "team-lead@company.com"
          subject: "LLM Cost Warning: Budget 75% Utilized"
          body: |
            Budget Warning Alert
            
            Current spend: ${{current_spend}}
            Budget limit: ${{budget_limit}}
            Utilization: {{utilization}}%
            
            Please review and optimize costs.
        
        - type: "slack"
          channel: "#cost-alerts"
          message: |
            :warning: LLM Cost Warning
            Budget {{utilization}}% utilized
            Current: ${{current_spend}} / ${{budget_limit}}
    
    auto_actions:
      - action: "send_notification"
        target: "team_lead"
      - action: "log_alert"
        level: "warning"
  
  - name: "critical_alert"
    threshold_percentage: 90
    severity: "critical"
    notification:
      channels:
        - type: "email"
          recipients:
            - "team-lead@company.com"
            - "finance@company.com"
          subject: "LLM Cost Critical: Budget 90% Utilized"
          body: |
            Budget Critical Alert
            
            Current spend: ${{current_spend}}
            Budget limit: ${{budget_limit}}
            Utilization: {{utilization}}%
            
            Immediate action required.
        
        - type: "slack"
          channel: "#cost-alerts"
          message: |
            :rotating_light: LLM Cost Critical
            Budget {{utilization}}% utilized
            Current: ${{current_spend}} / ${{budget_limit}}
            Action required immediately
        
        - type: "pagerduty"
          severity: "critical"
          summary: "LLM Budget Critical: {{utilization}}% utilized"
    
    auto_actions:
      - action: "send_notification"
        target: "team_lead, finance"
      - action: "escalate"
        target: "management"
      - action: "log_alert"
        level: "critical"
  
  - name: "emergency_alert"
    threshold_percentage: 100
    severity: "emergency"
    notification:
      channels:
        - type: "email"
          recipients:
            - "team-lead@company.com"
            - "finance@company.com"
            - "cto@company.com"
          subject: "LLM Cost Emergency: Budget Exceeded"
          body: |
            Budget Emergency Alert
            
            Current spend: ${{current_spend}}
            Budget limit: ${{budget_limit}}
            Utilization: {{utilization}}%
            
            BUDGET EXCEEDED. Immediate action required.
        
        - type: "slack"
          channel: "#cost-alerts"
          message: |
            :rotating_light::rotating_light: LLM Cost Emergency
            BUDGET EXCEEDED
            Current: ${{current_spend}} / ${{budget_limit}}
            Immediate action required
        
        - type: "pagerduty"
          severity: "emergency"
          summary: "LLM Budget EXCEEDED: {{utilization}}% utilized"
        
        - type: "sms"
          recipients:
            - "+1-555-0123"
          message: "LLM Budget EXCEEDED: ${{current_spend}} / ${{budget_limit}}"
    
    auto_actions:
      - action: "send_notification"
        target: "team_lead, finance, cto"
      - action: "escalate"
        target: "management, finance"
      - action: "log_alert"
        level: "emergency"
      - action: "trigger_automation"
        target: "cost_reduction_automation"
```

### Anomaly Detection Alerts

```yaml
anomaly_alerts:
  - name: "cost_spike_alert"
    description: "Alert on unexpected cost spikes"
    detection:
      method: "standard_deviation"
      threshold: 3
      lookback_period: "1 hour"
    notification:
      channels:
        - type: "email"
          recipients:
            - "team-lead@company.com"
          subject: "LLM Cost Anomaly Detected"
          body: |
            Cost Anomaly Alert
            
            Detected anomaly:
            - Time: ${{anomaly_timestamp}}
            - Cost: ${{anomaly_cost}}
            - Expected: ${{expected_cost}}
            - Deviation: {{deviation}} standard deviations
            
            Please investigate.
        
        - type: "slack"
          channel: "#cost-alerts"
          message: |
            :warning: LLM Cost Anomaly Detected
            Cost: ${{anomaly_cost}} (expected ${{expected_cost}})
            Deviation: {{deviation}} std devs
    
    auto_actions:
      - action: "log_anomaly"
        details: "full_anomaly_data"
      - action: "investigate"
        target: "cost_investigation"
  
  - name: "high_cost_per_request_alert"
    description: "Alert on high cost per request"
    detection:
      metric: "cost_per_request"
      threshold: 0.10
      lookback_period: "5 minutes"
    notification:
      channels:
        - type: "email"
          recipients:
            - "team-lead@company.com"
          subject: "High Cost Per Request Detected"
          body: |
            High Cost Alert
            
            Cost per request exceeded threshold:
            - Current: ${{current_cost_per_request}}
            - Threshold: ${{threshold}}
            - Time: ${{timestamp}}
            
            Please optimize model selection or prompts.
    
    auto_actions:
      - action: "log_alert"
        level: "warning"
      - action: "suggest_optimization"
        target: "model_selection_optimizer"
```

---

## Optimization Report Examples

### Monthly Optimization Report

```yaml
monthly_optimization_report:
  name: "Monthly Cost Optimization Report"
  description: "Monthly report on cost optimization efforts"
  frequency: "monthly"
  recipients:
    - "engineering_leads"
    - "finance"
    - "management"
  
  sections:
    - name: "executive_summary"
      title: "Executive Summary"
      content: |
        ## Executive Summary
        
        ### Key Metrics
        - Total Monthly Cost: ${{total_cost}}
        - Budget Utilization: {{budget_utilization}}%
        - Cost Reduction: {{cost_reduction}}%
        - Optimization Savings: ${{optimization_savings}}
        
        ### Highlights
        - Implemented {{optimizations_implemented}} optimizations
        - Achieved {{savings_percentage}}% cost reduction
        - Improved cost efficiency by {{efficiency_improvement}}%
        
        ### Recommendations
        - Continue current optimization strategy
        - Focus on {{focus_area}} for next month
        - Implement {{recommendation}} for additional savings
    
    - name: "cost_analysis"
      title: "Cost Analysis"
      content: |
        ## Cost Analysis
        
        ### Cost Breakdown
        | Category | Cost | % of Total | Change |
        |----------|------|------------|--------|
        | API Costs | ${{api_cost}} | {{api_percentage}}% | {{api_change}} |
        | Infrastructure | ${{infra_cost}} | {{infra_percentage}}% | {{infra_change}} |
        | Storage | ${{storage_cost}} | {{storage_percentage}}% | {{storage_change}} |
        | Other | ${{other_cost}} | {{other_percentage}}% | {{other_change}} |
        
        ### Cost Trends
        - API costs {{api_trend}} by {{api_change}}%
        - Infrastructure costs {{infra_trend}} by {{infra_change}}%
        - Storage costs {{storage_trend}} by {{storage_change}}%
    
    - name: "optimization_impact"
      title: "Optimization Impact"
      content: |
        ## Optimization Impact
        
        ### Optimizations Implemented
        | Optimization | Savings | Impact |
        |--------------|---------|--------|
        | Token Optimization | ${{token_savings}} | {{token_impact}}% |
        | Caching Implementation | ${{cache_savings}} | {{cache_impact}}% |
        | Model Selection | ${{model_savings}} | {{model_impact}}% |
        | Resource Right-Sizing | ${{resource_savings}} | {{resource_impact}}% |
        
        ### Total Savings
        - Monthly Savings: ${{monthly_savings}}
        - Annual Projected: ${{annual_savings}}
        - ROI: {{roi}}%
    
    - name: "recommendations"
      title: "Recommendations"
      content: |
        ## Recommendations
        
        ### Immediate Actions
        1. {{immediate_action_1}}
        2. {{immediate_action_2}}
        3. {{immediate_action_3}}
        
        ### Medium-Term Actions
        1. {{medium_action_1}}
        2. {{medium_action_2}}
        3. {{medium_action_3}}
        
        ### Long-Term Strategy
        1. {{long_term_strategy_1}}
        2. {{long_term_strategy_2}}
        3. {{long_term_strategy_3}}
    
    - name: "next_month_plan"
      title: "Next Month Plan"
      content: |
        ## Next Month Plan
        
        ### Budget Allocation
        - Total Budget: ${{next_month_budget}}
        - API Costs: ${{next_api_budget}}
        - Infrastructure: ${{next_infra_budget}}
        - Storage: ${{next_storage_budget}}
        
        ### Optimization Goals
        - Target Cost Reduction: {{target_reduction}}%
        - Focus Areas: {{focus_areas}}
        - Success Metrics: {{success_metrics}}
        
        ### Action Items
        1. {{action_item_1}}
        2. {{action_item_2}}
        3. {{action_item_3}}
```

### Optimization Recommendation Report

```yaml
optimization_recommendation_report:
  name: "Cost Optimization Recommendations"
  description: "Detailed optimization recommendations"
  frequency: "weekly"
  recipients:
    - "engineering_leads"
    - "ml_engineers"
  
  sections:
    - name: "current_status"
      title: "Current Cost Status"
      content: |
        ## Current Cost Status
        
        ### Weekly Cost Summary
        - Total Cost: ${{weekly_cost}}
        - Daily Average: ${{daily_average}}
        - Cost per Request: ${{cost_per_request}}
        - Cost per Token: ${{cost_per_token}}
        
        ### Cost Breakdown
        | Model | Cost | Requests | Avg Cost |
        |-------|------|----------|----------|
        | GPT-4 | ${{gpt4_cost}} | {{gpt4_requests}} | ${{gpt4_avg}} |
        | GPT-3.5 | ${{gpt35_cost}} | {{gpt35_requests}} | ${{gpt35_avg}} |
        | Claude | ${{claude_cost}} | {{claude_requests}} | ${{claude_avg}} |
    
    - name: "optimization_opportunities"
      title: "Optimization Opportunities"
      content: |
        ## Optimization Opportunities
        
        ### Token Optimization
        - **Opportunity**: Compress prompts for simple queries
        - **Current Token Usage**: {{current_tokens}} tokens/request
        - **Potential Savings**: {{token_savings}} tokens/request
        - **Estimated Cost Savings**: ${{token_cost_savings}}/month
        
        ### Caching
        - **Opportunity**: Implement semantic caching
        - **Current Cache Hit Rate**: {{current_cache_hit}}%
        - **Potential Cache Hit Rate**: {{potential_cache_hit}}%
        - **Estimated Cost Savings**: ${{cache_cost_savings}}/month
        
        ### Model Selection
        - **Opportunity**: Use GPT-3.5 for simple tasks
        - **Current Model Distribution**: {{current_distribution}}
        - **Optimized Distribution**: {{optimized_distribution}}
        - **Estimated Cost Savings**: ${{model_cost_savings}}/month
    
    - name: "implementation_plan"
      title: "Implementation Plan"
      content: |
        ## Implementation Plan
        
        ### Week 1
        - [ ] Implement prompt compression
        - [ ] Set up token monitoring
        - [ ] Baseline current costs
        
        ### Week 2
        - [ ] Implement semantic caching
        - [ ] Set up cache monitoring
        - [ ] Test cache performance
        
        ### Week 3
        - [ ] Implement model selection logic
        - [ ] Set up model routing
        - [ ] Test model selection
        
        ### Week 4
        - [ ] Monitor optimization impact
        - [ ] Measure cost savings
        - [ ] Report results
    
    - name: "expected_outcomes"
      title: "Expected Outcomes"
      content: |
        ## Expected Outcomes
        
        ### Cost Reduction
        - Token Optimization: ${{token_savings}}/month
        - Caching: ${{cache_savings}}/month
        - Model Selection: ${{model_savings}}/month
        - **Total**: ${{total_savings}}/month
        
        ### Performance Impact
        - Response Time: {{response_time_change}}
        - Throughput: {{throughput_change}}
        - Quality: {{quality_change}}
        
        ### ROI
        - Implementation Cost: ${{implementation_cost}}
        - Monthly Savings: ${{monthly_savings}}
        - Payback Period: ${{payback_period}}
        - Annual ROI: {{annual_roi}}%
```

---

## Chargeback Model Examples

### Team-Based Chargeback

```yaml
team_chargeback:
  name: "Team-Based Cost Allocation"
  description: "Allocate costs to teams based on usage"
  
  allocation_rules:
    - name: "api_cost_allocation"
      description: "Allocate API costs to teams"
      formula: "team_api_cost = team_tokens / total_tokens * total_api_cost"
      implementation: |
        def allocate_api_costs(cost_records, teams):
            total_tokens = sum(record.tokens for record in cost_records)
            total_api_cost = sum(record.cost for record in cost_records)
            
            allocations = {}
            for team in teams:
                team_records = [r for r in cost_records if r.team == team]
                team_tokens = sum(record.tokens for record in team_records)
                team_cost = (team_tokens / total_tokens) * total_api_cost
                allocations[team] = team_cost
            
            return allocations
    
    - name: "infrastructure_cost_allocation"
      description: "Allocate infrastructure costs to teams"
      formula: "team_infra_cost = team_compute_hours / total_compute_hours * total_infra_cost"
      implementation: |
        def allocate_infrastructure_costs(resource_usage, teams):
            total_compute_hours = sum(usage.compute_hours for usage in resource_usage)
            total_infra_cost = sum(usage.cost for usage in resource_usage)
            
            allocations = {}
            for team in teams:
                team_usage = [u for u in resource_usage if u.team == team]
                team_compute_hours = sum(usage.compute_hours for usage in team_usage)
                team_cost = (team_compute_hours / total_compute_hours) * total_infra_cost
                allocations[team] = team_cost
            
            return allocations
    
    - name: "storage_cost_allocation"
      description: "Allocate storage costs to teams"
      formula: "team_storage_cost = team_storage_gb / total_storage_gb * total_storage_cost"
      implementation: |
        def allocate_storage_costs(storage_usage, teams):
            total_storage_gb = sum(usage.storage_gb for usage in storage_usage)
            total_storage_cost = sum(usage.cost for usage in storage_usage)
            
            allocations = {}
            for team in teams:
                team_usage = [u for u in storage_usage if u.team == team]
                team_storage_gb = sum(usage.storage_gb for usage in team_usage)
                team_cost = (team_storage_gb / total_storage_gb) * total_storage_cost
                allocations[team] = team_cost
            
            return allocations
  
  reporting:
    - name: "monthly_team_report"
      description: "Monthly team cost report"
      content: |
        ## Monthly Team Cost Report
        
        ### Team: {{team_name}}
        - Period: {{period}}
        - Total Cost: ${{total_cost}}
        - Budget Utilization: {{budget_utilization}}%
        
        ### Cost Breakdown
        | Category | Cost | % of Total |
        |----------|------|------------|
        | API Costs | ${{api_cost}} | {{api_percentage}}% |
        | Infrastructure | ${{infra_cost}} | {{infra_percentage}}% |
        | Storage | ${{storage_cost}} | {{storage_percentage}}% |
        | Other | ${{other_cost}} | {{other_percentage}}% |
        
        ### Cost Trends
        - Month-over-Month: {{mom_change}}%
        - Year-over-Year: {{yoy_change}}%
        
        ### Optimization Opportunities
        - {{optimization_1}}
        - {{optimization_2}}
        - {{optimization_3}}
```

### Project-Based Chargeback

```yaml
project_chargeback:
  name: "Project-Based Cost Allocation"
  description: "Allocate costs to projects based on usage"
  
  allocation_rules:
    - name: "project_cost_allocation"
      description: "Allocate all costs to projects"
      formula: "project_cost = project_usage / total_usage * total_cost"
      implementation: |
        def allocate_project_costs(cost_records, projects):
            total_cost = sum(record.cost for record in cost_records)
            
            allocations = {}
            for project in projects:
                project_records = [r for r in cost_records if r.project == project]
                project_cost = sum(record.cost for record in project_records)
                allocations[project] = {
                    "cost": project_cost,
                    "percentage": (project_cost / total_cost) * 100
                }
            
            return allocations
  
  project_budgets:
    - project: "chatbot-v2"
      budget: 5000
      allocated: 3500
      utilization: 70
      status: "on_track"
    
    - project: "content-generator"
      budget: 3000
      allocated: 2800
      utilization: 93
      status: "warning"
    
    - project: "code-assist"
      budget: 4000
      allocated: 2000
      utilization: 50
      status: "under_budget"
  
  reporting:
    - name: "monthly_project_report"
      description: "Monthly project cost report"
      content: |
        ## Monthly Project Cost Report
        
        ### Project: {{project_name}}
        - Period: {{period}}
        - Total Cost: ${{total_cost}}
        - Budget: ${{budget}}
        - Utilization: {{utilization}}%
        - Status: {{status}}
        
        ### Cost Breakdown
        | Category | Cost | % of Budget |
        |----------|------|-------------|
        | API Costs | ${{api_cost}} | {{api_percentage}}% |
        | Infrastructure | ${{infra_cost}} | {{infra_percentage}}% |
        | Storage | ${{storage_cost}} | {{storage_percentage}}% |
        | Other | ${{other_cost}} | {{other_percentage}}% |
        
        ### Budget Forecast
        - Current Run Rate: ${{run_rate}}/month
        - Forecasted End of Month: ${{forecast}}
        - Budget Remaining: ${{remaining}}
        
        ### Recommendations
        - {{recommendation_1}}
        - {{recommendation_2}}
        - {{recommendation_3}}
```

### User-Based Chargeback

```yaml
user_chargeback:
  name: "User-Based Cost Allocation"
  description: "Allocate costs to users based on usage"
  
  allocation_rules:
    - name: "user_cost_allocation"
      description: "Allocate costs to users based on token usage"
      formula: "user_cost = user_tokens / total_tokens * total_cost"
      implementation: |
        def allocate_user_costs(cost_records, users):
            total_tokens = sum(record.tokens for record in cost_records)
            total_cost = sum(record.cost for record in cost_records)
            
            allocations = {}
            for user in users:
                user_records = [r for r in cost_records if r.user_id == user]
                user_tokens = sum(record.tokens for record in user_records)
                user_cost = (user_tokens / total_tokens) * total_cost
                allocations[user] = {
                    "cost": user_cost,
                    "tokens": user_tokens,
                    "cost_per_token": user_cost / user_tokens if user_tokens > 0 else 0
                }
            
            return allocations
  
  user_tiers:
    - tier: "free"
      monthly_limit: 0.10
      features: ["basic_chat"]
      cost_per_token: 0.0001
    
    - tier: "pro"
      monthly_limit: 5.00
      features: ["basic_chat", "code_generation", "analysis"]
      cost_per_token: 0.00008
    
    - tier: "enterprise"
      monthly_limit: 50.00
      features: ["all_features", "priority_support"]
      cost_per_token: 0.00006
  
  reporting:
    - name: "monthly_user_report"
      description: "Monthly user cost report"
      content: |
        ## Monthly User Cost Report
        
        ### User: {{user_name}}
        - Period: {{period}}
        - Tier: {{tier}}
        - Total Cost: ${{total_cost}}
        - Monthly Limit: ${{monthly_limit}}
        - Utilization: {{utilization}}%
        
        ### Usage Summary
        - Total Tokens: {{total_tokens}}
        - API Calls: {{api_calls}}
        - Avg Tokens per Call: {{avg_tokens}}
        
        ### Cost Breakdown
        | Feature | Tokens | Cost |
        |---------|--------|------|
        | Basic Chat | {{chat_tokens}} | ${{chat_cost}} |
        | Code Generation | {{code_tokens}} | ${{code_cost}} |
        | Analysis | {{analysis_tokens}} | ${{analysis_cost}} |
        
        ### Cost Trends
        - Month-over-Month: {{mom_change}}%
        - Daily Average: ${{daily_average}}
        
        ### Recommendations
        - {{recommendation_1}}
        - {{recommendation_2}}
```

---

## Cost Calculation Examples

### Token Cost Calculator

```python
from dataclasses import dataclass
from typing import Dict, List
import json

@dataclass
class TokenCost:
    """Calculate token costs for different models."""
    
    # Pricing per 1K tokens (USD)
    pricing: Dict[str, Dict[str, float]] = None
    
    def __post_init__(self):
        if self.pricing is None:
            self.pricing = {
                "gpt-4": {
                    "input": 0.03,
                    "output": 0.06,
                    "cached": 0.003
                },
                "gpt-4-turbo": {
                    "input": 0.01,
                    "output": 0.03,
                    "cached": 0.001
                },
                "gpt-3.5-turbo": {
                    "input": 0.0005,
                    "output": 0.0015,
                    "cached": 0.00005
                },
                "claude-3-opus": {
                    "input": 0.015,
                    "output": 0.075,
                    "cached": 0.0015
                },
                "claude-3-sonnet": {
                    "input": 0.003,
                    "output": 0.015,
                    "cached": 0.0003
                },
                "claude-3-haiku": {
                    "input": 0.00025,
                    "output": 0.00125,
                    "cached": 0.000025
                }
            }
    
    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0
    ) -> Dict[str, float]:
        """Calculate cost for a model call."""
        if model not in self.pricing:
            raise ValueError(f"Unknown model: {model}")
        
        pricing = self.pricing[model]
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        cache_cost = (cached_tokens / 1000) * pricing["cached"]
        
        total_cost = input_cost + output_cost + cache_cost
        
        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "cache_cost": cache_cost,
            "total_cost": total_cost,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "cached": cached_tokens,
                "total": input_tokens + output_tokens + cached_tokens
            }
        }
    
    def compare_models(
        self,
        models: List[str],
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0
    ) -> Dict[str, Dict]:
        """Compare costs across multiple models."""
        comparisons = {}
        
        for model in models:
            cost = self.calculate_cost(
                model, input_tokens, output_tokens, cached_tokens
            )
            comparisons[model] = cost
        
        return comparisons
    
    def optimize_model_selection(
        self,
        task_complexity: float,
        input_tokens: int,
        output_tokens: int
    ) -> str:
        """Select the most cost-effective model based on complexity."""
        if task_complexity > 0.7:
            return "gpt-4"  # High complexity, use best model
        elif task_complexity > 0.4:
            return "gpt-4-turbo"  # Medium complexity
        else:
            return "gpt-3.5-turbo"  # Low complexity, use cheapest

# Example usage
calculator = TokenCost()

# Calculate cost for a single call
cost = calculator.calculate_cost(
    model="gpt-4",
    input_tokens=2500,
    output_tokens=1000,
    cached_tokens=500
)
print(f"Cost breakdown: {json.dumps(cost, indent=2)}")

# Compare models
comparison = calculator.compare_models(
    models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
    input_tokens=2500,
    output_tokens=1000
)
print(f"\nModel comparison: {json.dumps(comparison, indent=2)}")

# Optimize model selection
model = calculator.optimize_model_selection(
    task_complexity=0.3,
    input_tokens=2500,
    output_tokens=1000
)
print(f"\nRecommended model: {model}")
```

### Cost Forecast Calculator

```python
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CostForecaster:
    """Forecast future costs based on historical data."""
    
    historical_data: List[Dict] = None
    
    def __post_init__(self):
        if self.historical_data is None:
            self.historical_data = []
    
    def add_data_point(self, date: datetime, cost: float):
        """Add a historical data point."""
        self.historical_data.append({
            "date": date,
            "cost": cost
        })
    
    def linear_regression_forecast(self, days_ahead: int) -> List[Dict]:
        """Forecast using linear regression."""
        if len(self.historical_data) < 2:
            raise ValueError("Need at least 2 data points")
        
        # Prepare data
        dates = [d["date"] for d in self.historical_data]
        costs = [d["cost"] for d in self.historical_data]
        
        # Convert dates to numeric
        base_date = min(dates)
        x = np.array([(d - base_date).days for d in dates])
        y = np.array(costs)
        
        # Fit linear regression
        coefficients = np.polyfit(x, y, 1)
        slope, intercept = coefficients
        
        # Generate forecast
        forecast = []
        last_date = max(dates)
        
        for i in range(1, days_ahead + 1):
            forecast_date = last_date + timedelta(days=i)
            forecast_cost = slope * (len(self.historical_data) + i) + intercept
            forecast.append({
                "date": forecast_date,
                "predicted_cost": max(0, forecast_cost),  # Ensure non-negative
                "confidence": "medium"
            })
        
        return forecast
    
    def moving_average_forecast(self, window_size: int, days_ahead: int) -> List[Dict]:
        """Forecast using moving average."""
        if len(self.historical_data) < window_size:
            raise ValueError(f"Need at least {window_size} data points")
        
        costs = [d["cost"] for d in self.historical_data]
        forecast = []
        
        for i in range(days_ahead):
            # Calculate moving average
            recent_costs = costs[-window_size:]
            avg_cost = sum(recent_costs) / len(recent_costs)
            
            # Add some trend adjustment
            if len(costs) >= 2:
                trend = (costs[-1] - costs[-2]) / costs[-2]
                avg_cost *= (1 + trend * 0.1)  # Dampen trend
            
            forecast_date = datetime.now() + timedelta(days=i + 1)
            forecast.append({
                "date": forecast_date,
                "predicted_cost": max(0, avg_cost),
                "confidence": "low" if i > 7 else "medium"
            })
            
            # Add forecast to costs for next iteration
            costs.append(avg_cost)
        
        return forecast
    
    def exponential_smoothing_forecast(
        self, 
        alpha: float, 
        days_ahead: int
    ) -> List[Dict]:
        """Forecast using exponential smoothing."""
        if len(self.historical_data) < 1:
            raise ValueError("Need at least 1 data point")
        
        costs = [d["cost"] for d in self.historical_data]
        
        # Initialize forecast
        forecast_value = costs[0]
        for cost in costs:
            forecast_value = alpha * cost + (1 - alpha) * forecast_value
        
        # Generate forecast
        forecast = []
        for i in range(days_ahead):
            forecast_date = datetime.now() + timedelta(days=i + 1)
            forecast.append({
                "date": forecast_date,
                "predicted_cost": max(0, forecast_value),
                "confidence": "medium"
            })
        
        return forecast
    
    def calculate_confidence_intervals(
        self, 
        forecasts: List[Dict], 
        confidence: float = 0.95
    ) -> List[Dict]:
        """Calculate confidence intervals for forecasts."""
        if len(self.historical_data) < 7:
            raise ValueError("Need at least 7 days of data for confidence intervals")
        
        costs = [d["cost"] for d in self.historical_data]
        mean_cost = np.mean(costs)
        std_cost = np.std(costs)
        
        # Z-score for confidence level
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        intervals = []
        for forecast in forecasts:
            margin = z * std_cost
            intervals.append({
                "date": forecast["date"],
                "predicted_cost": forecast["predicted_cost"],
                "lower_bound": max(0, forecast["predicted_cost"] - margin),
                "upper_bound": forecast["predicted_cost"] + margin,
                "confidence_level": confidence
            })
        
        return intervals

# Example usage
forecaster = CostForecaster()

# Add historical data
for i in range(30):
    date = datetime.now() - timedelta(days=30-i)
    cost = 150 + np.random.normal(0, 20)  # Base cost with variation
    forecaster.add_data_point(date, cost)

# Generate forecasts
linear_forecast = forecaster.linear_regression_forecast(7)
ma_forecast = forecaster.moving_average_forecast(7, 7)
es_forecast = forecaster.exponential_smoothing_forecast(0.3, 7)

# Calculate confidence intervals
linear_intervals = forecaster.calculate_confidence_intervals(linear_forecast)

print("Linear Regression Forecast:")
for f in linear_forecast[:3]:
    print(f"  {f['date'].strftime('%Y-%m-%d')}: ${f['predicted_cost']:.2f}")

print("\nMoving Average Forecast:")
for f in ma_forecast[:3]:
    print(f"  {f['date'].strftime('%Y-%m-%d')}: ${f['predicted_cost']:.2f}")

print("\nExponential Smoothing Forecast:")
for f in es_forecast[:3]:
    print(f"  {f['date'].strftime('%Y-%m-%d')}: ${f['predicted_cost']:.2f}")
```

---

## Monitoring Configuration Examples

### Cost Monitoring Configuration

```yaml
cost_monitoring:
  metrics:
    - name: "api_cost"
      description: "Total API cost"
      query: "SUM(cost) FROM api_calls WHERE timestamp > NOW() - INTERVAL '1 hour'"
      threshold:
        warning: 100
        critical: 200
      alert: true
    
    - name: "cost_per_request"
      description: "Average cost per request"
      query: "AVG(cost) FROM api_calls WHERE timestamp > NOW() - INTERVAL '1 hour'"
      threshold:
        warning: 0.05
        critical: 0.10
      alert: true
    
    - name: "token_usage"
      description: "Total token usage"
      query: "SUM(tokens) FROM api_calls WHERE timestamp > NOW() - INTERVAL '1 hour'"
      threshold:
        warning: 1000000
        critical: 2000000
      alert: true
    
    - name: "cost_efficiency"
      description: "Cost efficiency ratio"
      query: "SUM(value) / SUM(cost) FROM api_calls WHERE timestamp > NOW() - INTERVAL '1 hour'"
      threshold:
        warning: 5
        critical: 2
      alert: true
  
  dashboards:
    - name: "cost_overview"
      widgets:
        - type: "metric"
          title: "Total Cost"
          query: "SUM(cost) FROM api_calls WHERE date = CURRENT_DATE"
          format: "currency"
        
        - type: "line_chart"
          title: "Cost Trend"
          query: "SELECT date, SUM(cost) FROM api_calls WHERE date >= NOW() - INTERVAL '7 days' GROUP BY date"
          time_range: "7d"
        
        - type: "pie_chart"
          title: "Cost by Model"
          query: "SELECT model, SUM(cost) FROM api_calls WHERE date = CURRENT_DATE GROUP BY model"
        
        - type: "bar_chart"
          title: "Cost by Team"
          query: "SELECT team, SUM(cost) FROM api_calls WHERE date = CURRENT_DATE GROUP BY team"
  
  alerts:
    - name: "cost_spike"
      condition: "api_cost > 200"
      severity: "critical"
      channels:
        - "email"
        - "slack"
      recipients:
        - "team-lead@company.com"
      message: "Cost spike detected: ${{api_cost}}"
    
    - name: "budget_exceeded"
      condition: "cost > budget_limit"
      severity: "emergency"
      channels:
        - "email"
        - "slack"
        - "pagerduty"
      recipients:
        - "team-lead@company.com"
        - "finance@company.com"
      message: "Budget exceeded: ${{cost}} > ${{budget_limit}}"
```

### Alert Configuration

```yaml
alert_configuration:
  channels:
    - name: "email"
      type: "email"
      config:
        smtp_server: "smtp.company.com"
        smtp_port: 587
        username: "alerts@company.com"
        password: "${SMTP_PASSWORD}"
        use_tls: true
    
    - name: "slack"
      type: "slack"
      config:
        webhook_url: "${SLACK_WEBHOOK_URL}"
        channel: "#cost-alerts"
        username: "Cost Alert Bot"
        icon_emoji: ":moneybag:"
    
    - name: "pagerduty"
      type: "pagerduty"
      config:
        integration_key: "${PAGERDUTY_KEY}"
        severity_map:
          warning: "warning"
          critical: "critical"
          emergency: "critical"
  
  templates:
    - name: "cost_alert"
      subject: "LLM Cost Alert: {{alert_name}}"
      body: |
        LLM Cost Alert
        
        Alert: {{alert_name}}
        Severity: {{severity}}
        Time: {{timestamp}}
        
        Details:
        - Current Value: {{current_value}}
        - Threshold: {{threshold}}
        - Budget: ${{budget}}
        - Current Spend: ${{current_spend}}
        
        Action Required:
        {{action_required}}
    
    - name: "budget_alert"
      subject: "Budget Alert: {{budget_name}}"
      body: |
        Budget Alert
        
        Budget: {{budget_name}}
        Limit: ${{budget_limit}}
        Current: ${{current_spend}}
        Utilization: {{utilization}}%
        
        {{#if exceeded}}
        BUDGET EXCEEDED
        {{/if}}
        
        Recommendations:
        {{recommendations}}
```

---

## Governance Examples

### Cost Governance Policy

```yaml
cost_governance_policy:
  name: "LLM Cost Governance Policy"
  version: "1.0"
  effective_date: "2024-01-01"
  
  policies:
    - name: "budget_management"
      description: "Budget creation and management"
      requirements:
        - "All projects must have approved budgets"
        - "Budgets must be reviewed monthly"
        - "Budget overruns must be reported immediately"
        - "Budget adjustments require approval"
      responsibilities:
        - "Finance team: Budget creation and approval"
        - "Engineering leads: Budget monitoring and reporting"
        - "Team leads: Cost optimization and control"
    
    - name: "cost_optimization"
      description: "Cost optimization requirements"
      requirements:
        - "Regular cost optimization reviews"
        - "Implementation of approved optimizations"
        - "Measurement of optimization impact"
        - "Documentation of optimization efforts"
      responsibilities:
        - "ML engineers: Implement optimizations"
        - "Engineering leads: Review and approve optimizations"
        - "Finance team: Measure optimization impact"
    
    - name: "cost_allocation"
      description: "Cost allocation requirements"
      requirements:
        - "All resources must be tagged"
        - "Costs must be attributed to teams/projects"
        - "Cost reports must be generated monthly"
        - "Chargeback must be implemented"
      responsibilities:
        - "Platform team: Tag enforcement"
        - "Engineering leads: Cost attribution"
        - "Finance team: Cost reporting and chargeback"
    
    - name: "spending_controls"
      description: "Spending control requirements"
      requirements:
        - "Spending limits must be set"
        - "Approval workflows for large expenses"
        - "Real-time monitoring and alerts"
        - "Emergency shutdown procedures"
      responsibilities:
        - "Finance team: Set spending limits"
        - "Engineering leads: Implement controls"
        - "Platform team: Monitor and alert"
  
  procedures:
    - name: "budget_approval"
      steps:
        - "Project team submits budget request"
        - "Engineering lead reviews and approves"
        - "Finance team reviews and approves"
        - "Budget is set up in monitoring system"
        - "Team is notified of budget limits"
    
    - name: "cost_optimization"
      steps:
        - "Identify optimization opportunity"
        - "Analyze potential savings"
        - "Create optimization plan"
        - "Get approval from engineering lead"
        - "Implement optimization"
        - "Measure and report impact"
    
    - name: "budget_overrun"
      steps:
        - "Alert is triggered at 90% utilization"
        - "Team lead reviews and takes action"
        - "If overrun occurs, escalate to management"
        - "Create remediation plan"
        - "Implement cost controls"
        - "Report to finance team"
```

### Cost Review Meeting Template

```yaml
cost_review_meeting:
  name: "Weekly Cost Review Meeting"
  frequency: "weekly"
  duration: "30 minutes"
  participants:
    - "Engineering leads"
    - "Finance representative"
    - "Product representative"
    - "Platform team"
  
  agenda:
    - name: "cost_summary"
      duration: "5 minutes"
      content: |
        ## Cost Summary
        
        - Total spend this week: ${{weekly_spend}}
        - Budget utilization: {{budget_utilization}}%
        - Week-over-week change: {{wow_change}}%
        - Forecast for month: ${{monthly_forecast}}
    
    - name: "cost_breakdown"
      duration: "10 minutes"
      content: |
        ## Cost Breakdown
        
        ### By Category
        | Category | Cost | % of Total | Change |
        |----------|------|------------|--------|
        | API Costs | ${{api_cost}} | {{api_pct}}% | {{api_change}} |
        | Infrastructure | ${{infra_cost}} | {{infra_pct}}% | {{infra_change}} |
        | Storage | ${{storage_cost}} | {{storage_pct}}% | {{storage_change}} |
        
        ### By Team
        | Team | Cost | Budget | Utilization |
        |------|------|--------|-------------|
        | ML Engineering | ${{ml_cost}} | ${{ml_budget}} | {{ml_util}}% |
        | Data Science | ${{ds_cost}} | ${{ds_budget}} | {{ds_util}}% |
        | Platform | ${{plat_cost}} | ${{plat_budget}} | {{plat_util}}% |
    
    - name: "optimization_progress"
      duration: "10 minutes"
      content: |
        ## Optimization Progress
        
        ### Completed Optimizations
        - {{completed_optimization_1}}
        - {{completed_optimization_2}}
        
        ### In Progress
        - {{in_progress_optimization_1}}
        - {{in_progress_optimization_2}}
        
        ### Planned
        - {{planned_optimization_1}}
        - {{planned_optimization_2}}
        
        ### Savings Achieved
        - This week: ${{weekly_savings}}
        - This month: ${{monthly_savings}}
        - Projected annual: ${{annual_savings}}
    
    - name: "action_items"
      duration: "5 minutes"
      content: |
        ## Action Items
        
        - [ ] {{action_item_1}}
        - [ ] {{action_item_2}}
        - [ ] {{action_item_3}}
        
        ### Next Week Focus
        - {{focus_area_1}}
        - {{focus_area_2}}
```

---

## Automation Examples

### Cost Optimization Automation

```yaml
cost_optimization_automation:
  name: "Automated Cost Optimization"
  description: "Automated cost optimization workflows"
  
  workflows:
    - name: "auto_scaling"
      trigger: "cpu_utilization > 80%"
      actions:
        - action: "scale_up"
          parameters:
            instance_count: "+2"
            max_instances: 10
        
        - action: "notify"
          parameters:
            channel: "slack"
            message: "Scaled up due to high CPU utilization"
    
    - name: "cost_reduction"
      trigger: "budget_utilization > 90%"
      actions:
        - action: "reduce_non_critical"
          parameters:
            reduce_percentage: 20
            target_services: ["development", "testing"]
        
        - action: "notify"
          parameters:
            channel: "email"
            recipients: ["team-lead@company.com"]
            message: "Reduced non-critical services due to budget utilization"
    
    - name: "cache_optimization"
      trigger: "cache_hit_rate < 50%"
      actions:
        - action: "increase_cache_size"
          parameters:
            increase_percentage: 50
        
        - action: "optimize_cache_policy"
          parameters:
            policy: "lru"
            ttl: "1 hour"
        
        - action: "notify"
          parameters:
            channel: "slack"
            message: "Optimized cache due to low hit rate"
    
    - name: "model_selection"
      trigger: "cost_per_request > 0.10"
      actions:
        - action: "analyze_model_usage"
          parameters:
            lookback_period: "1 hour"
        
        - action: "optimize_model_selection"
          parameters:
            strategy: "complexity_based"
            downscale_threshold: 0.5
        
        - action: "notify"
          parameters:
            channel: "slack"
            message: "Optimized model selection due to high cost per request"
  
  monitoring:
    metrics:
      - "automation_success_rate"
      - "cost_savings_from_automation"
      - "automation_execution_time"
      - "false_positive_rate"
    
    alerts:
      - name: "automation_failure"
        condition: "automation_success_rate < 90%"
        severity: "warning"
        action: "review_automation_logs"
      
      - name: "automation_cost_savings"
        condition: "cost_savings_from_automation < 100"
        severity: "info"
        action: "review_optimization_strategies"
```

### Cost Reporting Automation

```yaml
cost_reporting_automation:
  name: "Automated Cost Reporting"
  description: "Automated cost report generation and distribution"
  
  reports:
    - name: "daily_cost_summary"
      schedule: "0 8 * * *"  # Daily at 8 AM
      recipients:
        - "engineering_leads@company.com"
      template: |
        Daily Cost Summary - {{date}}
        
        Total Cost: ${{total_cost}}
        Budget Utilization: {{budget_utilization}}%
        
        Top Cost Drivers:
        {{#each top_drivers}}
        - {{name}}: ${{cost}} ({{percentage}}%)
        {{/each}}
        
        Anomalies:
        {{#if anomalies}}
        {{#each anomalies}}
        - {{description}}
        {{/each}}
        {{else}}
        No anomalies detected.
        {{/if}}
    
    - name: "weekly_optimization_report"
      schedule: "0 9 * * 1"  # Weekly on Monday at 9 AM
      recipients:
        - "engineering_leads@company.com"
        - "finance@company.com"
      template: |
        Weekly Optimization Report - Week {{week_number}}
        
        Cost Summary:
        - Total Cost: ${{total_cost}}
        - Week-over-Week: {{wow_change}}%
        
        Optimization Progress:
        - Completed: {{completed_optimizations}}
        - In Progress: {{in_progress_optimizations}}
        - Planned: {{planned_optimizations}}
        
        Savings:
        - This Week: ${{weekly_savings}}
        - Month-to-Date: ${{mtd_savings}}
        
        Recommendations:
        {{#each recommendations}}
        - {{description}}
        {{/each}}
    
    - name: "monthly_executive_report"
      schedule: "0 10 1 * *"  # Monthly on 1st at 10 AM
      recipients:
        - "leadership@company.com"
        - "finance@company.com"
      template: |
        Monthly Executive Report - {{month}} {{year}}
        
        Executive Summary:
        - Total Cost: ${{total_cost}}
        - Budget: ${{budget}}
        - Utilization: {{budget_utilization}}%
        
        Cost Breakdown:
        {{#each cost_breakdown}}
        - {{category}}: ${{cost}} ({{percentage}}%)
        {{/each}}
        
        Optimization Impact:
        - Monthly Savings: ${{monthly_savings}}
        - Annual Projected: ${{annual_savings}}
        - ROI: {{roi}}%
        
        Recommendations:
        {{#each recommendations}}
        - {{description}}
        {{/each}}
  
  automation:
    - name: "report_generation"
      trigger: "schedule"
      actions:
        - action: "generate_report"
          parameters:
            report_type: "{{report_name}}"
        
        - action: "distribute_report"
          parameters:
            recipients: "{{recipients}}"
            channels: ["email"]
        
        - action: "log_report"
          parameters:
            report_name: "{{report_name}}"
            timestamp: "{{timestamp}}"
    
    - name: "report_failure_handling"
      trigger: "report_generation_failed"
      actions:
        - action: "retry_report"
          parameters:
            max_retries: 3
            retry_delay: "5 minutes"
        
        - action: "notify_failure"
          parameters:
            channel: "slack"
            message: "Report generation failed: {{error}}"
```

---

## Summary

This document provides practical examples of cost management configurations, dashboards, and implementations for LLM and agentic systems. These examples can be used as templates or references for implementing cost management in your own systems.

### Key Examples

1. **Cost Dashboards**: Executive, team, and real-time monitoring dashboards
2. **Budget Alerts**: Multi-level alerts with automated actions
3. **Optimization Reports**: Monthly and recommendation reports
4. **Chargeback Models**: Team, project, and user-based allocation
5. **Cost Calculators**: Token cost and forecasting calculators
6. **Monitoring Configurations**: Metrics, dashboards, and alerts
7. **Governance Examples**: Policies, procedures, and meeting templates
8. **Automation Examples**: Optimization and reporting automation

### Implementation Guide

1. **Start with Dashboards**: Implement basic cost visibility
2. **Add Alerts**: Set up budget alerts and anomaly detection
3. **Implement Optimization**: Deploy token optimization and caching
4. **Establish Governance**: Create policies and procedures
5. **Automate Processes**: Implement automated optimization and reporting
6. **Continuous Improvement**: Regular reviews and improvements

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cost visibility | 100% | Monthly audit |
| Alert accuracy | > 95% | Monthly review |
| Optimization savings | > 10% | Month-over-month |
| Report accuracy | > 99% | Monthly verification |
| Automation success | > 90% | Monthly monitoring |

By using these examples as templates, organizations can quickly implement comprehensive cost management for their LLM and agentic systems.
