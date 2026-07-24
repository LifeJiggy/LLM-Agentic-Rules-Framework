# Cost Management Troubleshooting for LLM & Agentic Systems

## Table of Contents

1. [Introduction](#introduction)
2. [Cost Spike Troubleshooting](#cost-spike-troubleshooting)
3. [Budget Overrun Troubleshooting](#budget-overrun-troubleshooting)
4. [Attribution Gap Troubleshooting](#attribution-gap-troubleshooting)
5. [Optimization Failure Troubleshooting](#optimization-failure-troubleshooting)
6. [Forecasting Error Troubleshooting](#forecasting-error-troubleshooting)
7. [Monitoring Issue Troubleshooting](#monitoring-issue-troubleshooting)
8. [Billing Discrepancy Troubleshooting](#billing-discrepancy-troubleshooting)
9. [Performance vs Cost Issues](#performance-vs-cost-issues)
10. [Troubleshooting Tools and Scripts](#troubleshooting-tools-and-scripts)
11. [Summary](#summary)

---

## Introduction

Cost management troubleshooting is essential for identifying and resolving cost-related issues in LLM and agentic systems. This guide provides systematic approaches to diagnose and fix common cost problems.

### Common Cost Issues

| Issue Type | Symptoms | Impact |
|------------|----------|--------|
| Cost Spikes | Sudden increase in costs | Budget overruns |
| Budget Overruns | Exceeding budget limits | Financial impact |
| Attribution Gaps | Missing cost allocation | No visibility |
| Optimization Failures | Expected savings not realized | Inefficient spending |
| Forecasting Errors | Inaccurate cost predictions | Poor planning |
| Monitoring Issues | Incomplete or inaccurate data | Blind spots |
| Billing Discrepancies | Differences between expected and actual | Financial confusion |

### Troubleshooting Approach

1. **Identify the Problem**: Understand what's happening
2. **Gather Data**: Collect relevant information
3. **Analyze Root Cause**: Determine why it's happening
4. **Implement Fix**: Apply the solution
5. **Verify Resolution**: Confirm the issue is resolved
6. **Document Learnings**: Record for future reference

---

## Cost Spike Troubleshooting

Cost spikes are sudden, unexpected increases in costs that can quickly exhaust budgets.

### Symptoms

- Daily or hourly costs significantly higher than normal
- Unexpected API call volumes
- Higher than expected token consumption
- Unusual infrastructure utilization

### Diagnostic Steps

```yaml
cost_spike_diagnosis:
  step_1: "identify_spike"
    description: "Identify when and where the spike occurred"
    actions:
      - "Check cost dashboards for exact timing"
      - "Identify which services/models are affected"
      - "Compare with historical patterns"
      - "Check for any deployment changes"
    
    commands:
      - "Review real-time cost monitoring"
      - "Check API call logs"
      - "Review infrastructure metrics"
      - "Check for recent deployments"
  
  step_2: "analyze_causes"
    description: "Analyze potential causes"
    common_causes:
      - name: "increased_traffic"
        indicators:
          - "Higher than normal API calls"
          - "More concurrent users"
          - "External traffic spike"
        verification:
          - "Check request logs"
          - "Review traffic patterns"
          - "Check for marketing campaigns"
      
      - name: "model_change"
        indicators:
          - "Different model being used"
          - "Model configuration changed"
          - "New model features enabled"
        verification:
          - "Review model selection logs"
          - "Check configuration changes"
          - "Review model usage patterns"
      
      - name: "prompt_change"
        indicators:
          - "Longer prompts"
          - "More complex queries"
          - "Increased context usage"
        verification:
          - "Review prompt patterns"
          - "Check token usage per request"
          - "Analyze query complexity"
      
      - name: "caching_failure"
        indicators:
          - "Lower cache hit rates"
          - "More cache misses"
          - "Cache size exceeded"
        verification:
          - "Check cache metrics"
          - "Review cache configuration"
          - "Monitor cache performance"
      
      - name: "error_retry"
        indicators:
          - "High error rates"
          - "Multiple retry attempts"
          - "Failed request costs"
        verification:
          - "Review error logs"
          - "Check retry policies"
          - "Monitor error rates"
  
  step_3: "implement_fix"
    description: "Implement appropriate fix"
    fixes:
      - cause: "increased_traffic"
        actions:
          - "Implement rate limiting"
          - "Scale infrastructure appropriately"
          - "Optimize request handling"
          - "Consider cost caps"
      
      - cause: "model_change"
        actions:
          - "Review model selection logic"
          - "Implement model routing"
          - "Set model usage limits"
          - "Optimize model selection"
      
      - cause: "prompt_change"
        actions:
          - "Optimize prompts"
          - "Implement prompt compression"
          - "Set token limits"
          - "Review prompt templates"
      
      - cause: "caching_failure"
        actions:
          - "Fix cache configuration"
          - "Increase cache size"
          - "Optimize cache strategy"
          - "Implement cache warming"
      
      - cause: "error_retry"
        actions:
          - "Fix error handling"
          - "Implement circuit breakers"
          - "Optimize retry logic"
          - "Set retry limits"
  
  step_4: "verify_fix"
    description: "Verify the fix is working"
    actions:
      - "Monitor costs for improvement"
      - "Check for recurrence"
      - "Validate performance impact"
      - "Document changes"
```

### Example Troubleshooting Script

```python
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta

class CostSpikeDetector:
    """Detect and diagnose cost spikes."""
    
    def __init__(self, cost_data: pd.DataFrame):
        self.cost_data = cost_data
    
    def detect_spikes(
        self, 
        threshold: float = 2.0,
        lookback_days: int = 7
    ) -> List[Dict]:
        """Detect cost spikes based on historical patterns."""
        spikes = []
        
        # Calculate historical average and standard deviation
        historical_data = self.cost_data[
            self.cost_data['date'] < datetime.now() - timedelta(days=1)
        ]
        
        if len(historical_data) < lookback_days:
            return spikes
        
        avg_cost = historical_data['cost'].mean()
        std_cost = historical_data['cost'].std()
        
        # Check recent data for spikes
        recent_data = self.cost_data[
            self.cost_data['date'] >= datetime.now() - timedelta(days=1)
        ]
        
        for _, row in recent_data.iterrows():
            if row['cost'] > avg_cost + threshold * std_cost:
                spikes.append({
                    'date': row['date'],
                    'cost': row['cost'],
                    'expected': avg_cost,
                    'deviation': (row['cost'] - avg_cost) / std_cost,
                    'severity': 'critical' if row['cost'] > avg_cost + 3 * std_cost else 'warning'
                })
        
        return spikes
    
    def diagnose_spike(self, spike: Dict) -> Dict:
        """Diagnose the cause of a cost spike."""
        diagnosis = {
            'spike': spike,
            'potential_causes': [],
            'recommended_actions': []
        }
        
        # Analyze the spike
        if spike['deviation'] > 3:
            diagnosis['potential_causes'].extend([
                'Traffic spike',
                'Model configuration change',
                'Caching failure',
                'Error retry storm'
            ])
            diagnosis['recommended_actions'].extend([
                'Check traffic logs',
                'Review recent deployments',
                'Monitor cache performance',
                'Review error handling'
            ])
        elif spike['deviation'] > 2:
            diagnosis['potential_causes'].extend([
                'Increased usage',
                'Prompt optimization issues',
                'Model selection changes'
            ])
            diagnosis['recommended_actions'].extend([
                'Review usage patterns',
                'Check prompt templates',
                'Review model selection'
            ])
        
        return diagnosis
    
    def generate_report(self, spikes: List[Dict]) -> Dict:
        """Generate a troubleshooting report."""
        report = {
            'total_spikes': len(spikes),
            'critical_spikes': len([s for s in spikes if s['severity'] == 'critical']),
            'warning_spikes': len([s for s in spikes if s['severity'] == 'warning']),
            'spikes': spikes,
            'diagnoses': [self.diagnose_spike(spike) for spike in spikes],
            'summary': self._generate_summary(spikes)
        }
        
        return report
    
    def _generate_summary(self, spikes: List[Dict]) -> str:
        """Generate a summary of the spikes."""
        if not spikes:
            return "No cost spikes detected."
        
        critical_count = len([s for s in spikes if s['severity'] == 'critical'])
        warning_count = len([s for s in spikes if s['severity'] == 'warning'])
        
        summary = f"Detected {len(spikes)} cost spikes: "
        summary += f"{critical_count} critical, {warning_count} warning."
        
        if critical_count > 0:
            summary += " Immediate action required for critical spikes."
        
        return summary

# Example usage
# Create sample cost data
dates = pd.date_range(start='2024-01-01', end='2024-01-31')
costs = [100 + i * 2 for i in range(31)]  # Base cost with slight increase
costs[15] = 500  # Spike on day 16
costs[25] = 400  # Another spike on day 26

cost_data = pd.DataFrame({
    'date': dates,
    'cost': costs
})

# Detect spikes
detector = CostSpikeDetector(cost_data)
spikes = detector.detect_spikes(threshold=2.0)

# Generate report
report = detector.generate_report(spikes)

print(f"Total spikes detected: {report['total_spikes']}")
print(f"Critical spikes: {report['critical_spikes']}")
print(f"Warning spikes: {report['warning_spikes']}")
print(f"Summary: {report['summary']}")
```

---

## Budget Overrun Troubleshooting

Budget overruns occur when spending exceeds allocated budgets, requiring immediate attention.

### Symptoms

- Budget utilization exceeds 100%
- Budget alerts triggered
- Spending limits reached
- Financial impact warnings

### Diagnostic Steps

```yaml
budget_overrun_diagnosis:
  step_1: "assess_situation"
    description: "Assess the severity of the overrun"
    actions:
      - "Calculate overrun amount"
      - "Determine overrun percentage"
      - "Identify which budget is affected"
      - "Assess financial impact"
    
    metrics:
      - "overrun_amount"
      - "overrun_percentage"
      - "affected_budget"
      - "financial_impact"
  
  step_2: "identify_causes"
    description: "Identify what caused the overrun"
    common_causes:
      - name: "unexpected_traffic"
        description: "Higher than expected usage"
        verification:
          - "Compare actual vs expected traffic"
          - "Check for external factors"
          - "Review marketing campaigns"
      
      - name: "cost_increase"
        description: "Costs per unit increased"
        verification:
          - "Check pricing changes"
          - "Review cost per request"
          - "Compare with historical costs"
      
      - name: "budget_calculation_error"
        description: "Budget was calculated incorrectly"
        verification:
          - "Review budget calculation"
          - "Check assumptions"
          - "Validate budget allocation"
      
      - name: "scope_creep"
        description: "Project scope expanded without budget adjustment"
        verification:
          - "Compare project scope"
          - "Review feature additions"
          - "Check resource allocation"
  
  step_3: "immediate_actions"
    description: "Take immediate action to control costs"
    actions:
      - name: "implement_cost_controls"
        description: "Implement immediate cost controls"
        actions:
          - "Set spending limits"
          - "Implement rate limiting"
          - "Scale down non-critical services"
          - "Pause non-essential features"
      
      - name: "communicate_with_stakeholders"
        description: "Notify stakeholders of the situation"
        actions:
          - "Alert management"
          - "Notify finance team"
          - "Inform affected teams"
          - "Document the situation"
      
      - name: "implement_emergency_measures"
        description: "Implement emergency cost reduction"
        actions:
          - "Reduce model usage"
          - "Optimize prompts"
          - "Implement caching"
          - "Reduce infrastructure"
  
  step_4: "long_term_fixes"
    description: "Implement long-term fixes"
    actions:
      - name: "adjust_budgets"
        description: "Adjust budgets if needed"
        actions:
          - "Review budget allocation"
          - "Adjust for actual usage"
          - "Plan for future growth"
          - "Set realistic budgets"
      
      - name: "optimize_costs"
        description: "Optimize costs to prevent future overruns"
        actions:
          - "Implement cost optimization"
          - "Right-size resources"
          - "Optimize model selection"
          - "Implement caching"
      
      - name: "improve_forecasting"
        description: "Improve cost forecasting"
        actions:
          - "Update forecasting models"
          - "Improve data collection"
          - "Review forecasting assumptions"
          - "Implement better monitoring"
```

### Example Budget Overrun Script

```python
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime

@dataclass
class BudgetOverrunHandler:
    """Handle budget overrun situations."""
    
    def __init__(self, budget_limit: float, current_spend: float):
        self.budget_limit = budget_limit
        self.current_spend = current_spend
        self.overrun = current_spend - budget_limit
        self.overrun_percentage = (self.overrun / budget_limit) * 100 if budget_limit > 0 else 0
    
    def assess_severity(self) -> Dict:
        """Assess the severity of the overrun."""
        if self.overrun_percentage > 20:
            severity = "critical"
            description = "Severe budget overrun"
        elif self.overrun_percentage > 10:
            severity = "high"
            description = "Significant budget overrun"
        elif self.overrun_percentage > 5:
            severity = "medium"
            description = "Moderate budget overrun"
        else:
            severity = "low"
            description = "Minor budget overrun"
        
        return {
            "severity": severity,
            "description": description,
            "overrun_amount": self.overrun,
            "overrun_percentage": self.overrun_percentage,
            "current_spend": self.current_spend,
            "budget_limit": self.budget_limit
        }
    
    def identify_causes(self) -> List[str]:
        """Identify potential causes of the overrun."""
        causes = []
        
        # Check for common causes
        if self.overrun_percentage > 50:
            causes.append("Severe cost spike or unexpected usage")
        
        if self.overrun_percentage > 20:
            causes.append("Significant increase in usage or costs")
        
        if self.overrun_percentage > 10:
            causes.append("Budget calculation error or scope creep")
        
        if self.overrun_percentage > 5:
            causes.append("Cost optimization opportunities missed")
        
        return causes
    
    def recommend_actions(self) -> List[Dict]:
        """Recommend actions to address the overrun."""
        actions = []
        
        # Immediate actions
        actions.append({
            "priority": "immediate",
            "action": "Implement cost controls",
            "description": "Set spending limits and rate limiting",
            "impact": "Stop further overrun"
        })
        
        actions.append({
            "priority": "immediate",
            "action": "Notify stakeholders",
            "description": "Alert management and finance team",
            "impact": "Ensure awareness and support"
        })
        
        # Short-term actions
        if self.overrun_percentage > 10:
            actions.append({
                "priority": "short_term",
                "action": "Optimize costs",
                "description": "Implement cost optimization measures",
                "impact": "Reduce ongoing costs"
            })
        
        # Long-term actions
        actions.append({
            "priority": "long_term",
            "action": "Review budget allocation",
            "description": "Adjust budgets for actual usage patterns",
            "impact": "Prevent future overruns"
        })
        
        return actions
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive overrun report."""
        return {
            "assessment": self.assess_severity(),
            "causes": self.identify_causes(),
            "recommendations": self.recommend_actions(),
            "timestamp": datetime.now().isoformat()
        }

# Example usage
handler = BudgetOverrunHandler(
    budget_limit=10000,
    current_spend=12500
)

report = handler.generate_report()
print(f"Severity: {report['assessment']['severity']}")
print(f"Overrun: ${report['assessment']['overrun_amount']:.2f} ({report['assessment']['overrun_percentage']:.1f}%)")
print(f"Causes: {', '.join(report['causes'])}")
print(f"Recommendations: {len(report['recommendations'])} actions suggested")
```

---

## Attribution Gap Troubleshooting

Attribution gaps occur when costs cannot be properly assigned to teams, projects, or features.

### Symptoms

- Costs with "untagged" or "unknown" attribution
- Missing team/project information
- Unable to identify cost drivers
- Inaccurate chargeback reports

### Diagnostic Steps

```yaml
attribution_gap_diagnosis:
  step_1: "identify_gaps"
    description: "Identify where attribution gaps exist"
    actions:
      - "Review cost attribution reports"
      - "Identify untagged resources"
      - "Check for missing metadata"
      - "Review data collection processes"
    
    checks:
      - "Tag compliance rate"
      - "Untagged resource count"
      - "Missing metadata fields"
      - "Data collection completeness"
  
  step_2: "analyze_root_cause"
    description: "Analyze why gaps exist"
    common_causes:
      - name: "missing_tags"
        description: "Resources not properly tagged"
        verification:
          - "Check tag enforcement"
          - "Review tagging policies"
          - "Audit resource creation processes"
      
      - name: "inconsistent_tags"
        description: "Tags applied inconsistently"
        verification:
          - "Review tag standards"
          - "Check tag values"
          - "Audit tag application"
      
      - name: "data_collection_issues"
        description: "Cost data not collected properly"
        verification:
          - "Check data pipelines"
          - "Review collection processes"
          - "Audit data quality"
      
      - name: "attribution_logic_errors"
        description: "Attribution logic has bugs"
        verification:
          - "Review attribution code"
          - "Test attribution logic"
          - "Audit attribution results"
  
  step_3: "implement_fixes"
    description: "Implement fixes for attribution gaps"
    actions:
      - name: "fix_tagging"
        description: "Fix tagging issues"
        actions:
          - "Implement tag enforcement"
          - "Audit and fix existing tags"
          - "Create tagging automation"
          - "Train teams on tagging"
      
      - name: "fix_data_collection"
        description: "Fix data collection issues"
        actions:
          - "Repair data pipelines"
          - "Implement validation"
          - "Add missing data sources"
          - "Improve data quality"
      
      - name: "fix_attribution_logic"
        description: "Fix attribution logic"
        actions:
          - "Fix bugs in attribution code"
          - "Improve attribution rules"
          - "Add missing attribution"
          - "Test attribution accuracy"
  
  step_4: "prevent_recurrence"
    description: "Prevent future attribution gaps"
    actions:
      - name: "implement_governance"
        description: "Implement attribution governance"
        actions:
          - "Create tagging standards"
          - "Implement compliance checks"
          - "Regular audits"
          - "Continuous monitoring"
      
      - name: "automate_processes"
        description: "Automate attribution processes"
        actions:
          - "Automate tag enforcement"
          - "Automate data validation"
          - "Automate reporting"
          - "Automate monitoring"
```

### Example Attribution Gap Script

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd

@dataclass
class AttributionGapAnalyzer:
    """Analyze and fix attribution gaps."""
    
    def __init__(self, cost_data: pd.DataFrame):
        self.cost_data = cost_data
    
    def identify_gaps(self) -> Dict:
        """Identify attribution gaps in cost data."""
        gaps = {
            'total_records': len(self.cost_data),
            'untagged_records': 0,
            'missing_team': 0,
            'missing_project': 0,
            'missing_feature': 0,
            'gap_details': []
        }
        
        # Check for missing tags
        required_tags = ['team', 'project', 'feature']
        
        for tag in required_tags:
            if tag in self.cost_data.columns:
                missing_count = self.cost_data[tag].isna().sum()
                gaps[f'missing_{tag}'] = missing_count
                
                if missing_count > 0:
                    gaps['gap_details'].append({
                        'type': f'missing_{tag}',
                        'count': missing_count,
                        'percentage': (missing_count / gaps['total_records']) * 100
                    })
        
        # Check for untagged records
        if 'team' in self.cost_data.columns and 'project' in self.cost_data.columns:
            untagged = self.cost_data[
                (self.cost_data['team'].isna()) & 
                (self.cost_data['project'].isna())
            ]
            gaps['untagged_records'] = len(untagged)
        
        return gaps
    
    def analyze_root_causes(self, gaps: Dict) -> List[Dict]:
        """Analyze root causes of attribution gaps."""
        causes = []
        
        # Check for missing tags
        for gap in gaps['gap_details']:
            if gap['percentage'] > 10:
                causes.append({
                    'cause': 'Tag Enforcement Gap',
                    'description': f"{gap['percentage']:.1f}% of records missing {gap['type']}",
                    'severity': 'high',
                    'impact': 'Significant attribution gaps'
                })
            elif gap['percentage'] > 5:
                causes.append({
                    'cause': 'Partial Tag Coverage',
                    'description': f"{gap['percentage']:.1f}% of records missing {gap['type']}",
                    'severity': 'medium',
                    'impact': 'Moderate attribution gaps'
                })
        
        # Check for untagged records
        if gaps['untagged_records'] > 0:
            untagged_percentage = (gaps['untagged_records'] / gaps['total_records']) * 100
            if untagged_percentage > 20:
                causes.append({
                    'cause': 'Major Attribution Gap',
                    'description': f"{untagged_percentage:.1f}% of records completely untagged",
                    'severity': 'critical',
                    'impact': 'Unable to attribute costs'
                })
        
        return causes
    
    def recommend_fixes(self, gaps: Dict, causes: List[Dict]) -> List[Dict]:
        """Recommend fixes for attribution gaps."""
        fixes = []
        
        # Immediate fixes
        if gaps['untagged_records'] > 0:
            fixes.append({
                'priority': 'immediate',
                'action': 'Audit and tag untagged records',
                'description': 'Manually review and tag untagged records',
                'impact': 'Restore attribution visibility'
            })
        
        # Short-term fixes
        for cause in causes:
            if cause['severity'] in ['high', 'critical']:
                fixes.append({
                    'priority': 'short_term',
                    'action': f"Fix {cause['cause']}",
                    'description': cause['description'],
                    'impact': 'Improve attribution accuracy'
                })
        
        # Long-term fixes
        fixes.append({
            'priority': 'long_term',
            'action': 'Implement tag enforcement',
            'description': 'Automate tag enforcement on resource creation',
            'impact': 'Prevent future attribution gaps'
        })
        
        return fixes
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive attribution gap report."""
        gaps = self.identify_gaps()
        causes = self.analyze_root_causes(gaps)
        fixes = self.recommend_fixes(gaps, causes)
        
        return {
            'gaps': gaps,
            'causes': causes,
            'recommendations': fixes,
            'summary': self._generate_summary(gaps, causes)
        }
    
    def _generate_summary(self, gaps: Dict, causes: List[Dict]) -> str:
        """Generate a summary of the analysis."""
        if not gaps['gap_details']:
            return "No significant attribution gaps detected."
        
        critical_causes = [c for c in causes if c['severity'] == 'critical']
        high_causes = [c for c in causes if c['severity'] == 'high']
        
        summary = f"Detected {len(gaps['gap_details'])} attribution gaps. "
        
        if critical_causes:
            summary += f"{len(critical_causes)} critical issues require immediate attention. "
        
        if high_causes:
            summary += f"{len(high_causes)} high-severity issues should be addressed soon."
        
        return summary

# Example usage
# Create sample cost data with gaps
data = {
    'date': ['2024-01-01'] * 100,
    'cost': [10] * 100,
    'team': ['ml-engineering'] * 80 + [None] * 20,
    'project': ['chatbot'] * 70 + [None] * 30,
    'feature': ['basic_chat'] * 90 + [None] * 10
}

cost_data = pd.DataFrame(data)

# Analyze gaps
analyzer = AttributionGapAnalyzer(cost_data)
report = analyzer.generate_report()

print(f"Total records: {report['gaps']['total_records']}")
print(f"Missing team: {report['gaps']['missing_team']}")
print(f"Missing project: {report['gaps']['missing_project']}")
print(f"Missing feature: {report['gaps']['missing_feature']}")
print(f"Summary: {report['summary']}")
```

---

## Optimization Failure Troubleshooting

Optimization failures occur when expected cost savings are not realized or optimizations don't work as intended.

### Symptoms

- Expected cost savings not achieved
- Optimization efforts not showing results
- Performance degradation without cost savings
- Optimization tools not working correctly

### Diagnostic Steps

```yaml
optimization_failure_diagnosis:
  step_1: "identify_failure"
    description: "Identify what optimization failed"
    types:
      - name: "token_optimization"
        expected_savings: "20-40%"
        symptoms:
          - "Token usage not reduced"
          - "Prompt compression not working"
          - "Response optimization failing"
      
      - name: "caching_optimization"
        expected_savings: "30-60%"
        symptoms:
          - "Cache hit rate not improving"
          - "Cache size issues"
          - "Cache invalidation problems"
      
      - name: "model_selection"
        expected_savings: "20-50%"
        symptoms:
          - "Wrong model selected"
          - "Model routing not working"
          - "Quality degradation"
      
      - name: "resource_optimization"
        expected_savings: "30-50%"
        symptoms:
          - "Resources not right-sized"
          - "Auto-scaling issues"
          - "Performance problems"
  
  step_2: "analyze_failure"
    description: "Analyze why the optimization failed"
    common_causes:
      - name: "incorrect_implementation"
        description: "Optimization implemented incorrectly"
        verification:
          - "Review implementation code"
          - "Test optimization logic"
          - "Validate configuration"
      
      - name: "data_quality_issues"
        description: "Poor data quality affecting optimization"
        verification:
          - "Check data accuracy"
          - "Validate data sources"
          - "Review data processing"
      
      - name: "configuration_errors"
        description: "Configuration issues"
        verification:
          - "Review configuration"
          - "Test configuration"
          - "Validate settings"
      
      - name: "performance_tradeoffs"
        description: "Optimization impacts performance"
        verification:
          - "Monitor performance metrics"
          - "Review performance impact"
          - "Validate user experience"
  
  step_3: "implement_fixes"
    description: "Fix the optimization failure"
    actions:
      - name: "fix_implementation"
        description: "Fix implementation issues"
        actions:
          - "Correct code bugs"
          - "Fix configuration"
          - "Update logic"
          - "Test fixes"
      
      - name: "fix_data_issues"
        description: "Fix data quality issues"
        actions:
          - "Improve data collection"
          - "Fix data processing"
          - "Validate data sources"
          - "Monitor data quality"
      
      - name: "re_optimize"
        description: "Re-optimize with fixes"
        actions:
          - "Re-implement optimization"
          - "Test optimization"
          - "Monitor results"
          - "Validate savings"
  
  step_4: "prevent_recurrence"
    description: "Prevent future optimization failures"
    actions:
      - name: "improve_monitoring"
        description: "Improve optimization monitoring"
        actions:
          - "Monitor optimization metrics"
          - "Track optimization impact"
          - "Alert on failures"
          - "Review optimization results"
      
      - name: "improve_testing"
        description: "Improve optimization testing"
        actions:
          - "Test optimization logic"
          - "Validate optimization results"
          - "Monitor performance impact"
          - "Review optimization effectiveness"
```

### Example Optimization Failure Script

```python
from dataclasses import dataclass
from typing import Dict, List
import pandas as pd

@dataclass
class OptimizationFailureAnalyzer:
    """Analyze optimization failures."""
    
    def __init__(self, optimization_data: pd.DataFrame):
        self.optimization_data = optimization_data
    
    def identify_failures(self) -> List[Dict]:
        """Identify optimization failures."""
        failures = []
        
        # Check for token optimization failures
        if 'tokens_before' in self.optimization_data.columns and 'tokens_after' in self.optimization_data.columns:
            token_reduction = 1 - (self.optimization_data['tokens_after'].sum() / 
                                  self.optimization_data['tokens_before'].sum())
            
            if token_reduction < 0.1:  # Less than 10% reduction
                failures.append({
                    'type': 'token_optimization',
                    'expected': '20-40% reduction',
                    'actual': f'{token_reduction*100:.1f}% reduction',
                    'severity': 'high',
                    'impact': 'Significant cost savings missed'
                })
        
        # Check for caching optimization failures
        if 'cache_hit_rate' in self.optimization_data.columns:
            avg_cache_hit = self.optimization_data['cache_hit_rate'].mean()
            
            if avg_cache_hit < 0.5:  # Less than 50% cache hit rate
                failures.append({
                    'type': 'caching_optimization',
                    'expected': '70%+ cache hit rate',
                    'actual': f'{avg_cache_hit*100:.1f}% cache hit rate',
                    'severity': 'high',
                    'impact': 'Cache optimization not effective'
                })
        
        # Check for model selection failures
        if 'model_cost' in self.optimization_data.columns and 'expected_model_cost' in self.optimization_data.columns:
            cost_difference = (self.optimization_data['model_cost'].sum() - 
                              self.optimization_data['expected_model_cost'].sum())
            
            if cost_difference > 0:  # Actual cost higher than expected
                failures.append({
                    'type': 'model_selection',
                    'expected': 'Lower cost with optimized model selection',
                    'actual': f'${cost_difference:.2f} higher than expected',
                    'severity': 'medium',
                    'impact': 'Model selection optimization not working'
                })
        
        return failures
    
    def analyze_root_causes(self, failures: List[Dict]) -> List[Dict]:
        """Analyze root causes of optimization failures."""
        causes = []
        
        for failure in failures:
            if failure['type'] == 'token_optimization':
                causes.append({
                    'failure': failure['type'],
                    'cause': 'Prompt compression not effective',
                    'description': 'Token usage not reduced as expected',
                    'verification': 'Review prompt templates and compression logic',
                    'fix': 'Improve prompt compression algorithms'
                })
            
            elif failure['type'] == 'caching_optimization':
                causes.append({
                    'failure': failure['type'],
                    'cause': 'Cache hit rate too low',
                    'description': 'Cache not serving enough requests',
                    'verification': 'Review cache configuration and usage patterns',
                    'fix': 'Optimize cache strategy and increase cache size'
                })
            
            elif failure['type'] == 'model_selection':
                causes.append({
                    'failure': failure['type'],
                    'cause': 'Model selection logic not working',
                    'description': 'Wrong models being selected',
                    'verification': 'Review model selection logic and complexity scoring',
                    'fix': 'Improve model selection algorithms'
                })
        
        return causes
    
    def recommend_fixes(self, failures: List[Dict], causes: List[Dict]) -> List[Dict]:
        """Recommend fixes for optimization failures."""
        fixes = []
        
        for cause in causes:
            fixes.append({
                'failure': cause['failure'],
                'fix': cause['fix'],
                'priority': 'high' if cause['failure'] in ['token_optimization', 'caching_optimization'] else 'medium',
                'expected_impact': 'Restore expected cost savings',
                'implementation_effort': 'medium'
            })
        
        return fixes
    
    def generate_report(self) -> Dict:
        """Generate a comprehensive optimization failure report."""
        failures = self.identify_failures()
        causes = self.analyze_root_causes(failures)
        fixes = self.recommend_fixes(failures, causes)
        
        return {
            'failures': failures,
            'causes': causes,
            'recommendations': fixes,
            'summary': self._generate_summary(failures)
        }
    
    def _generate_summary(self, failures: List[Dict]) -> str:
        """Generate a summary of the failures."""
        if not failures:
            return "No optimization failures detected."
        
        high_severity = [f for f in failures if f['severity'] == 'high']
        medium_severity = [f for f in failures if f['severity'] == 'medium']
        
        summary = f"Detected {len(failures)} optimization failures. "
        
        if high_severity:
            summary += f"{len(high_severity)} high-severity failures require immediate attention. "
        
        if medium_severity:
            summary += f"{len(medium_severity)} medium-severity failures should be addressed."
        
        return summary

# Example usage
# Create sample optimization data
data = {
    'tokens_before': [1000] * 100,
    'tokens_after': [950] * 100,  # Only 5% reduction
    'cache_hit_rate': [0.4] * 100,  # 40% cache hit rate
    'model_cost': [100] * 100,
    'expected_model_cost': [80] * 100  # Expected lower cost
}

optimization_data = pd.DataFrame(data)

# Analyze failures
analyzer = OptimizationFailureAnalyzer(optimization_data)
report = analyzer.generate_report()

print(f"Failures detected: {len(report['failures'])}")
print(f"Root causes: {len(report['causes'])}")
print(f"Recommendations: {len(report['recommendations'])}")
print(f"Summary: {report['summary']}")
```

---

## Forecasting Error Troubleshooting

Forecasting errors occur when cost predictions are significantly different from actual costs.

### Symptoms

- Forecasted costs differ significantly from actual
- Budget planning based on inaccurate forecasts
- Unexpected cost variations
- Poor resource planning

### Diagnostic Steps

```yaml
forecasting_error_diagnosis:
  step_1: "identify_error"
    description: "Identify forecasting errors"
    metrics:
      - "forecast_accuracy"
      - "mean_absolute_error"
      - "root_mean_square_error"
      - "forecast_bias"
    
    thresholds:
      - metric: "forecast_accuracy"
        acceptable: "> 80%"
        warning: "70-80%"
        critical: "< 70%"
      
      - metric: "mean_absolute_error"
        acceptable: "< 10%"
        warning: "10-20%"
        critical: "> 20%"
  
  step_2: "analyze_causes"
    description: "Analyze causes of forecasting errors"
    common_causes:
      - name: "insufficient_data"
        description: "Not enough historical data"
        verification:
          - "Check data availability"
          - "Review data quality"
          - "Assess data completeness"
      
      - name: "model_issues"
        description: "Forecasting model problems"
        verification:
          - "Review model performance"
          - "Check model assumptions"
          - "Validate model parameters"
      
      - name: "external_factors"
        description: "External factors not considered"
        verification:
          - "Review external data"
          - "Check for market changes"
          - "Assess business changes"
      
      - name: "seasonal_patterns"
        description: "Seasonal patterns not captured"
        verification:
          - "Review seasonal trends"
          - "Check for patterns"
          - "Validate seasonal adjustments"
  
  step_3: "implement_fixes"
    description: "Fix forecasting issues"
    actions:
      - name: "improve_data"
        description: "Improve data quality and quantity"
        actions:
          - "Collect more historical data"
          - "Improve data accuracy"
          - "Validate data sources"
          - "Monitor data quality"
      
      - name: "improve_model"
        description: "Improve forecasting model"
        actions:
          - "Update model parameters"
          - "Try different models"
          - "Validate model assumptions"
          - "Test model performance"
      
      - name: "account_for_factors"
        description: "Account for external factors"
        actions:
          - "Include external data"
          - "Adjust for business changes"
          - "Consider market factors"
          - "Update assumptions"
  
  step_4: "validate_fixes"
    description: "Validate forecasting improvements"
    actions:
      - "Test forecasting accuracy"
      - "Monitor forecast performance"
      - "Validate improvements"
      - "Document changes"
```

---

## Monitoring Issue Troubleshooting

Monitoring issues occur when cost monitoring systems fail to provide accurate or complete data.

### Symptoms

- Missing cost data
- Inaccurate cost reporting
- Dashboard not updating
- Alerts not triggering

### Diagnostic Steps

```yaml
monitoring_issue_diagnosis:
  step_1: "identify_issue"
    description: "Identify monitoring issues"
    checks:
      - name: "data_completeness"
        description: "Check if all cost data is being collected"
        verification:
          - "Review data sources"
          - "Check data pipelines"
          - "Validate data collection"
      
      - name: "data_accuracy"
        description: "Check if cost data is accurate"
        verification:
          - "Compare with billing data"
          - "Validate calculations"
          - "Check data sources"
      
      - name: "dashboard_status"
        description: "Check if dashboards are working"
        verification:
          - "Review dashboard configuration"
          - "Check data connections"
          - "Validate display logic"
      
      - name: "alert_status"
        description: "Check if alerts are working"
        verification:
          - "Review alert configuration"
          - "Test alert triggers"
          - "Validate notification channels"
  
  step_2: "analyze_root_cause"
    description: "Analyze root cause of monitoring issues"
    common_causes:
      - name: "data_pipeline_failure"
        description: "Data pipeline not working"
        verification:
          - "Check pipeline status"
          - "Review error logs"
          - "Validate data flow"
      
      - name: "configuration_error"
        description: "Configuration issues"
        verification:
          - "Review configuration"
          - "Check connections"
          - "Validate settings"
      
      - name: "resource_issues"
        description: "Resource constraints"
        verification:
          - "Check resource usage"
          - "Review performance"
          - "Validate capacity"
      
      - name: "permission_issues"
        description: "Permission problems"
        verification:
          - "Check access permissions"
          - "Review security settings"
          - "Validate credentials"
  
  step_3: "implement_fixes"
    description: "Fix monitoring issues"
    actions:
      - name: "fix_data_pipeline"
        description: "Fix data pipeline issues"
        actions:
          - "Repair broken connections"
          - "Fix data processing"
          - "Validate data flow"
          - "Monitor pipeline health"
      
      - name: "fix_configuration"
        description: "Fix configuration issues"
        actions:
          - "Update configuration"
          - "Fix connections"
          - "Validate settings"
          - "Test configuration"
      
      - name: "fix_resources"
        description: "Fix resource issues"
        actions:
          - "Scale resources"
          - "Optimize performance"
          - "Increase capacity"
          - "Monitor resource usage"
```

---

## Billing Discrepancy Troubleshooting

Billing discrepancies occur when there are differences between expected and actual billing amounts.

### Symptoms

- Differences between internal tracking and provider billing
- Unexpected billing amounts
- Discrepancies in cost allocation
- Billing errors

### Diagnostic Steps

```yaml
billing_discrepancy_diagnosis:
  step_1: "identify_discrepancy"
    description: "Identify billing discrepancies"
    checks:
      - name: "internal_vs_external"
        description: "Compare internal tracking with external billing"
        verification:
          - "Export internal cost data"
          - "Export provider billing data"
          - "Compare totals"
          - "Identify differences"
      
      - name: "allocation_discrepancies"
        description: "Check cost allocation accuracy"
        verification:
          - "Review allocation rules"
          - "Validate allocation calculations"
          - "Check for missing allocations"
          - "Verify allocation accuracy"
  
  step_2: "analyze_causes"
    description: "Analyze causes of discrepancies"
    common_causes:
      - name: "timing_differences"
        description: "Timing differences between tracking and billing"
        verification:
          - "Check billing cycles"
          - "Review timing of charges"
          - "Validate period alignment"
      
      - name: "calculation_errors"
        description: "Calculation errors"
        verification:
          - "Review calculation logic"
          - "Validate formulas"
          - "Check for bugs"
      
      - name: "missing_costs"
        description: "Costs not being tracked"
        verification:
          - "Review cost sources"
          - "Check for missing data"
          - "Validate data completeness"
      
      - name: "rate_differences"
        description: "Rate differences between tracking and billing"
        verification:
          - "Review pricing rates"
          - "Check for rate changes"
          - "Validate rate applications"
  
  step_3: "implement_fixes"
    description: "Fix billing discrepancies"
    actions:
      - name: "fix_timing"
        description: "Fix timing differences"
        actions:
          - "Align billing periods"
          - "Adjust for timing"
          - "Validate period alignment"
          - "Monitor timing"
      
      - name: "fix_calculations"
        description: "Fix calculation errors"
        actions:
          - "Correct calculation logic"
          - "Fix formulas"
          - "Validate calculations"
          - "Test fixes"
      
      - name: "fix_missing_costs"
        description: "Fix missing costs"
        actions:
          - "Add missing cost sources"
          - "Improve data collection"
          - "Validate completeness"
          - "Monitor coverage"
```

---

## Performance vs Cost Issues

Performance vs cost issues occur when there are tradeoffs between system performance and cost efficiency.

### Symptoms

- High performance but high costs
- Low costs but poor performance
- Inability to balance performance and cost
- User complaints about performance or cost

### Diagnostic Steps

```yaml
performance_cost_diagnosis:
  step_1: "identify_tradeoff"
    description: "Identify performance vs cost tradeoffs"
    metrics:
      - "performance_metrics"
        - "response_time"
        - "throughput"
        - "latency"
        - "availability"
      
      - "cost_metrics"
        - "total_cost"
        - "cost_per_request"
        - "cost_per_user"
        - "cost_efficiency"
    
    analysis:
      - "correlate_performance_and_cost"
      - "identify_tradeoff_points"
      - "assess_user_impact"
      - "evaluate_business_impact"
  
  step_2: "analyze_causes"
    description: "Analyze causes of performance vs cost issues"
    common_causes:
      - name: "over_optimization"
        description: "Too much focus on cost reduction"
        verification:
          - "Review optimization efforts"
          - "Check performance impact"
          - "Assess user experience"
      
      - name: "under_optimization"
        description: "Not enough cost optimization"
        verification:
          - "Review cost efficiency"
          - "Check optimization opportunities"
          - "Assess cost impact"
      
      - name: "misaligned_priorities"
        description: "Misaligned performance and cost priorities"
        verification:
          - "Review business requirements"
          - "Check performance targets"
          - "Validate cost targets"
  
  step_3: "implement_fixes"
    description: "Fix performance vs cost issues"
    actions:
      - name: "optimize_balance"
        description: "Optimize performance vs cost balance"
        actions:
          - "Set performance targets"
          - "Define cost limits"
          - "Optimize within constraints"
          - "Monitor balance"
      
      - name: "improve_efficiency"
        description: "Improve efficiency without sacrificing performance"
        actions:
          - "Optimize code"
          - "Improve caching"
          - "Right-size resources"
          - "Monitor efficiency"
      
      - name: "adjust_priorities"
        description: "Adjust performance and cost priorities"
        actions:
          - "Review business requirements"
          - "Adjust targets"
          - "Realign priorities"
          - "Communicate changes"
```

---

## Troubleshooting Tools and Scripts

### Diagnostic Scripts

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class CostTroubleshooter:
    """Comprehensive cost troubleshooting toolkit."""
    
    def __init__(self, cost_data: pd.DataFrame):
        self.cost_data = cost_data
    
    def detect_anomalies(
        self, 
        method: str = "zscore",
        threshold: float = 3.0
    ) -> List[Dict]:
        """Detect cost anomalies."""
        anomalies = []
        
        if method == "zscore":
            mean_cost = self.cost_data['cost'].mean()
            std_cost = self.cost_data['cost'].std()
            
            for _, row in self.cost_data.iterrows():
                zscore = (row['cost'] - mean_cost) / std_cost
                if abs(zscore) > threshold:
                    anomalies.append({
                        'date': row['date'],
                        'cost': row['cost'],
                        'expected': mean_cost,
                        'zscore': zscore,
                        'severity': 'critical' if abs(zscore) > threshold * 1.5 else 'warning'
                    })
        
        elif method == "iqr":
            q1 = self.cost_data['cost'].quantile(0.25)
            q3 = self.cost_data['cost'].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            for _, row in self.cost_data.iterrows():
                if row['cost'] < lower_bound or row['cost'] > upper_bound:
                    anomalies.append({
                        'date': row['date'],
                        'cost': row['cost'],
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'severity': 'critical' if row['cost'] > upper_bound * 1.5 else 'warning'
                    })
        
        return anomalies
    
    def analyze_trends(self, window: int = 7) -> Dict:
        """Analyze cost trends."""
        if len(self.cost_data) < window:
            return {'error': 'Insufficient data for trend analysis'}
        
        # Calculate moving average
        self.cost_data['moving_avg'] = self.cost_data['cost'].rolling(window=window).mean()
        
        # Calculate trend
        x = np.arange(len(self.cost_data))
        y = self.cost_data['cost'].values
        coefficients = np.polyfit(x, y, 1)
        slope = coefficients[0]
        
        # Determine trend direction
        if slope > 0.01:
            trend = 'increasing'
        elif slope < -0.01:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'slope': slope,
            'moving_average': self.cost_data['moving_avg'].iloc[-1],
            'current_cost': self.cost_data['cost'].iloc[-1],
            'average_cost': self.cost_data['cost'].mean()
        }
    
    def forecast_costs(self, days_ahead: int = 7) -> List[Dict]:
        """Forecast future costs."""
        if len(self.cost_data) < 14:
            return [{'error': 'Insufficient data for forecasting'}]
        
        # Simple linear regression forecast
        x = np.arange(len(self.cost_data))
        y = self.cost_data['cost'].values
        coefficients = np.polyfit(x, y, 1)
        
        forecast = []
        for i in range(1, days_ahead + 1):
            forecast_date = datetime.now() + timedelta(days=i)
            predicted_cost = coefficients[0] * (len(self.cost_data) + i) + coefficients[1]
            forecast.append({
                'date': forecast_date,
                'predicted_cost': max(0, predicted_cost),
                'confidence': 'medium'
            })
        
        return forecast
    
    def identify_optimization_opportunities(self) -> List[Dict]:
        """Identify cost optimization opportunities."""
        opportunities = []
        
        # Check for high-cost patterns
        avg_cost = self.cost_data['cost'].mean()
        high_cost_days = self.cost_data[self.cost_data['cost'] > avg_cost * 1.5]
        
        if len(high_cost_days) > 0:
            opportunities.append({
                'type': 'high_cost_days',
                'description': f'{len(high_cost_days)} days with costs > 50% above average',
                'potential_savings': (high_cost_days['cost'].sum() - 
                                   len(high_cost_days) * avg_cost) * 0.3,
                'priority': 'high'
            })
        
        # Check for cost volatility
        cost_std = self.cost_data['cost'].std()
        cost_mean = self.cost_data['cost'].mean()
        coefficient_of_variation = cost_std / cost_mean if cost_mean > 0 else 0
        
        if coefficient_of_variation > 0.3:
            opportunities.append({
                'type': 'cost_volatility',
                'description': 'High cost volatility detected',
                'potential_savings': cost_std * 0.2,
                'priority': 'medium'
            })
        
        return opportunities
    
    def generate_troubleshooting_report(self) -> Dict:
        """Generate comprehensive troubleshooting report."""
        anomalies = self.detect_anomalies()
        trends = self.analyze_trends()
        forecast = self.forecast_costs()
        opportunities = self.identify_optimization_opportunities()
        
        return {
            'anomalies': anomalies,
            'trends': trends,
            'forecast': forecast,
            'optimization_opportunities': opportunities,
            'summary': self._generate_summary(anomalies, trends, opportunities)
        }
    
    def _generate_summary(
        self, 
        anomalies: List[Dict], 
        trends: Dict, 
        opportunities: List[Dict]
    ) -> str:
        """Generate troubleshooting summary."""
        summary_parts = []
        
        if anomalies:
            critical_anomalies = [a for a in anomalies if a['severity'] == 'critical']
            summary_parts.append(f"Detected {len(anomalies)} anomalies ({len(critical_anomalies)} critical)")
        
        if trends.get('trend') == 'increasing':
            summary_parts.append("Costs are trending upward")
        elif trends.get('trend') == 'decreasing':
            summary_parts.append("Costs are trending downward")
        
        if opportunities:
            high_priority = [o for o in opportunities if o['priority'] == 'high']
            summary_parts.append(f"Found {len(opportunities)} optimization opportunities ({len(high_priority)} high priority)")
        
        return ". ".join(summary_parts) if summary_parts else "No significant issues detected"

# Example usage
# Create sample cost data
dates = pd.date_range(start='2024-01-01', end='2024-01-31')
costs = [100 + i * 2 + np.random.normal(0, 10) for i in range(31)]
costs[15] = 500  # Anomaly
costs[25] = 400  # Another anomaly

cost_data = pd.DataFrame({
    'date': dates,
    'cost': costs
})

# Troubleshoot
troubleshooter = CostTroubleshooter(cost_data)
report = troubleshooter.generate_troubleshooting_report()

print("Troubleshooting Report:")
print(f"Anomalies: {len(report['anomalies'])}")
print(f"Trend: {report['trends'].get('trend', 'unknown')}")
print(f"Optimization Opportunities: {len(report['optimization_opportunities'])}")
print(f"Summary: {report['summary']}")
```

---

## Summary

Cost management troubleshooting is essential for identifying and resolving cost-related issues in LLM and agentic systems. This guide provides systematic approaches to diagnose and fix common cost problems.

### Key Troubleshooting Areas

1. **Cost Spike Troubleshooting**: Identify and fix sudden cost increases
2. **Budget Overrun Troubleshooting**: Address budget exceedances
3. **Attribution Gap Troubleshooting**: Fix cost allocation issues
4. **Optimization Failure Troubleshooting**: Resolve optimization problems
5. **Forecasting Error Troubleshooting**: Improve cost predictions
6. **Monitoring Issue Troubleshooting**: Fix monitoring system problems
7. **Billing Discrepancy Troubleshooting**: Address billing differences
8. **Performance vs Cost Issues**: Balance performance and cost

### Troubleshooting Process

1. **Identify the Problem**: Understand what's happening
2. **Gather Data**: Collect relevant information
3. **Analyze Root Cause**: Determine why it's happening
4. **Implement Fix**: Apply the solution
5. **Verify Resolution**: Confirm the issue is resolved
6. **Document Learnings**: Record for future reference

### Prevention Strategies

| Strategy | Description | Impact |
|----------|-------------|--------|
| Proactive Monitoring | Monitor costs continuously | Early issue detection |
| Regular Reviews | Review costs regularly | Prevent issues |
| Automation | Automate troubleshooting | Faster resolution |
| Documentation | Document issues and fixes | Knowledge sharing |
| Training | Train teams on troubleshooting | Better preparedness |

By following this troubleshooting guide, organizations can quickly identify and resolve cost-related issues, ensuring effective cost management for their LLM and agentic systems.
