# Cost Management Examples - LLM & Agentic Rules Framework

## Overview

This document provides practical implementation examples for cost management in LLM and agentic systems.

## Example 1: Cost Dashboard

### Context

**When to Use**: Monitoring and visualizing costs

**Goal**: Track costs across services and identify optimization opportunities

### Implementation

```yaml
cost_dashboard:
  title: "AI Service Cost Dashboard"
  refresh: "hourly"
  
  panels:
    - title: "Total Cost"
      type: "stat"
      metrics:
        - name: "total_cost"
          query: "sum(daily_cost)"
          format: "currency"
    
    - title: "Cost by Service"
      type: "pie_chart"
      metrics:
        - name: "model_cost"
          query: "sum(daily_cost{service='model'})"
        - name: "compute_cost"
          query: "sum(daily_cost{service='compute'})"
        - name: "storage_cost"
          query: "sum(daily_cost{service='storage'})"
    
    - title: "Cost Trend"
      type: "graph"
      metrics:
        - name: "daily_cost"
          query: "sum(daily_cost) by (date)"
          time_range: "30_days"
    
    - title: "Cost by Team"
      type: "table"
      metrics:
        - name: "team_cost"
          query: "sum(daily_cost) by (team)"
          group_by: "team"
  
  alerts:
    - condition: "total_cost > budget * 0.9"
      severity: "warning"
      action: "notify_finance"
    
    - condition: "total_cost > budget"
      severity: "critical"
      action: "page_cfo"
```

## Example 2: Cost Optimization Report

### Context

**When to Use**: Identifying and tracking cost optimization opportunities

**Goal**: Reduce costs while maintaining performance

### Implementation

```yaml
cost_optimization_report:
  period: "monthly"
  
  sections:
    - section: "current_costs"
      metrics:
        - name: "total_cost"
          value: "$10,000"
          trend: "+5%"
        - name: "cost_per_request"
          value: "$0.01"
          trend: "+2%"
    
    - section: "optimization_opportunities"
      items:
        - opportunity: "model_caching"
          description: "Cache frequent model responses"
          estimated_savings: "$2,000/month"
          implementation_effort: "medium"
          priority: "high"
        
        - opportunity: "resource_rightsizing"
          description: "Downsize over-provisioned instances"
          estimated_savings: "$1,500/month"
          implementation_effort: "low"
          priority: "high"
        
        - opportunity: "api_call_reduction"
          description: "Batch API calls where possible"
          estimated_savings: "$800/month"
          implementation_effort: "medium"
          priority: "medium"
    
    - section: "implemented_optimizations"
      items:
        - optimization: "response_caching"
          status: "completed"
          actual_savings: "$1,800/month"
          implementation_date: "2026-05-01"
        
        - optimization: "model_selection"
          status: "in_progress"
          expected_savings: "$1,200/month"
          implementation_date: "2026-06-15"
    
    - section: "recommendations"
      recommendations:
        - "Implement response caching for top 10 queries"
        - "Right-size database instances"
        - "Review model selection for cost-performance tradeoff"
```

## Example 3: Budget Alert Configuration

### Context

**When to Use**: Setting up budget alerts and notifications

**Goal**: Get notified before budget overruns

### Implementation

```yaml
budget_alerts:
  budgets:
    - name: "monthly_total"
      amount: 10000
      period: "monthly"
      alerts:
        - threshold: 50
          severity: "info"
          recipients: ["finance@company.com"]
        
        - threshold: 80
          severity: "warning"
          recipients: ["finance@company.com", "engineering@company.com"]
        
        - threshold: 90
          severity: "critical"
          recipients: ["finance@company.com", "engineering@company.com", "cfo@company.com"]
        
        - threshold: 100
          severity: "critical"
          recipients: ["finance@company.com", "engineering@company.com", "cfo@company.com"]
          action: "page_cfo"
    
    - name: "model_cost"
      amount: 5000
      period: "monthly"
      alerts:
        - threshold: 80
          severity: "warning"
          recipients: ["ml-team@company.com"]
        
        - threshold: 100
          severity: "critical"
          recipients: ["ml-team@company.com", "engineering@company.com"]
  
  notification_templates:
    warning: |
      Budget Alert: {{budget_name}}
      Current spend: ${{current_spend}}
      Budget: ${{budget_amount}}
      Percentage: {{percentage}}%
      
      Please review and take action if needed.
    
    critical: |
      CRITICAL Budget Alert: {{budget_name}}
      Current spend: ${{current_spend}}
      Budget: ${{budget_amount}}
      Percentage: {{percentage}}%
      
      Immediate action required. Please investigate.
```

## Example Summary

| Example | Complexity | Time Required | Key Components |
|---------|------------|---------------|----------------|
| Cost Dashboard | Medium | 2 hours | Visualization, metrics, alerts |
| Cost Optimization | High | 4 hours | Analysis, recommendations, tracking |
| Budget Alerts | Low | 1 hour | Thresholds, notifications, templates |
