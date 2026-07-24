# Architecture Templates - Comprehensive Collection

## Overview

This document provides complete templates for architecture decision records, design documents, and review checklists.

## Architecture Decision Record Template

```yaml
adr:
  adr_id: string
  title: string
  status: proposed | under_review | accepted | deprecated | superseded
  date: string
  deciders: [list]
  
  context:
    background: string
    problem_statement: string
    goals: [list]
    constraints: [list]
    assumptions: [list]
  
  options:
    - id: string
      name: string
      description: string
      pros: [list]
      cons: [list]
      risks: [list]
      mitigation: [list]
      estimated_effort: string
      estimated_cost: string
      estimated_timeline: string
  
  decision:
    chosen_option: string
    rationale: string
    alternatives_rejected: [list]
    rejection_reasons: [list]
  
  consequences:
    positive: [list]
    negative: [list]
    risks: [list]
    mitigations: [list]
  
  compliance:
    regulatory_implications: [list]
    audit_requirements: [list]
    evidence_requirements: [list]
    review_schedule: string
  
  implementation:
    phases: [list]
    dependencies: [list]
    milestones: [list]
    success_criteria: [list]
  
  review:
    review_triggers: [list]
    review_schedule: string
    review_criteria: [list]
    review_attendees: [list]
  
  references:
    - title: string
      url: string
      relevance: string
  
  approval:
    required_approvers: [list]
    approval_status: pending | approved | rejected
    approval_date: string | null
    approval_notes: string | null
```

## Design Document Template

```yaml
design_document:
  document_id: string
  title: string
  version: string
  status: draft | review | approved | archived
  author: string
  created_date: string
  last_updated: string
  
  overview:
    purpose: string
    scope: string
    audience: string
    goals: [list]
    non_goals: [list]
  
  context:
    background: string
    current_state: string
    requirements:
      functional: [list]
      non_functional: [list]
      constraints: [list]
    assumptions: [list]
    dependencies: [list]
  
  architecture:
    high_level:
      description: string
      diagram: string
      components: [list]
    
    components:
      - name: string
        description: string
        responsibilities: [list]
        interfaces: [list]
        dependencies: [list]
        technology: string
        configuration: object
    
    data_flow:
      description: string
      diagram: string
      flows:
        - name: string
          source: string
          destination: string
          data: string
          protocol: string
          security: string
    
    security:
      authentication: string
      authorization: string
      encryption: string
      secrets_management: string
      audit_logging: string
      threat_model: string
    
    deployment:
      environment: string
      topology: string
      scaling: string
      monitoring: string
      backup: string
      recovery: string
    
    integration:
      external_services: [list]
      api_contracts: [list]
      mcp_servers: [list]
      webhooks: [list]
  
  design_decisions:
    - id: string
      title: string
      context: string
      decision: string
      rationale: string
      alternatives: [list]
      consequences: [list]
  
  data_model:
    entities: [list]
    relationships: [list]
    schemas: [list]
    storage: string
    retention: string
  
  api_design:
    endpoints: [list]
    authentication: string
    versioning: string
    rate_limiting: string
    error_handling: string
  
  testing:
    strategy: [list]
    coverage_requirements: [list]
    performance_targets: [list]
    security_testing: [list]
  
  monitoring:
    metrics: [list]
    dashboards: [list]
    alerts: [list]
    logging: [list]
  
  operations:
    deployment: string
    rollback: string
    scaling: string
    maintenance: string
    support: string
  
  risks:
    - risk: string
      likelihood: high | medium | low
      impact: high | medium | low
      mitigation: string
      owner: string
  
  timeline:
    phases: [list]
    milestones: [list]
    dependencies: [list]
    resources: [list]
  
  approval:
    reviewers: [list]
    approval_status: pending | approved | rejected
    approval_date: string | null
    approval_notes: string | null
```

## System Register Template

```yaml
system_register:
  system_id: string
  system_name: string
  description: string
  owner: string
  team: string
  status: active | inactive | decommissioned
  
  risk_tier: low | medium | high | prohibited
  risk_tier_justification: string
  risk_tier_last_reviewed: string
  
  purpose:
    intended_use: string
    prohibited_uses: [list]
    target_users: [list]
    jurisdictions: [list]
  
  domains: [list]
  domains_last_reviewed: string
  
  architecture:
    type: api | ui | agent | tool | retrieval | model | storage | integration
    components: [list]
    data_flows: [list]
    integrations: [list]
  
  model:
    provider: string
    model_name: string
    version: string
    fine_tuned: boolean
    deployment: hosted | self_hosted | hybrid
  
  data:
    data_types: [list]
    data_classification: [list]
    retention_period: string
    cross_border_transfers: [list]
  
  security:
    authentication: string
    authorization: string
    encryption: string
    threat_model_date: string
    last_security_review: string
  
  compliance:
    applicable_regulations: [list]
    compliance_status: compliant | non_compliant | pending
    last_compliance_review: string
  
  operations:
    deployment_date: string
    last_deployment: string
    monitoring: string
    on_call: string
    incident_response: string
  
  documentation:
    system_documentation: string
    model_card: string
    prompt_register: string
    tool_catalog: string
    runbooks: string
  
  reviews:
    last_architecture_review: string
    last_security_review: string
    last_compliance_review: string
    last_performance_review: string
    next_scheduled_review: string
  
  contacts:
    owner: string
    technical_lead: string
    security_contact: string
    compliance_contact: string
    operations_contact: string
```

## Threat Model Template

```yaml
threat_model:
  model_id: string
  system_id: string
  system_name: string
  version: string
  created_date: string
  last_updated: string
  author: string
  
  scope:
    description: string
    boundaries: [list]
    assets: [list]
    trust_levels: [list]
  
  architecture:
    components:
      - name: string
        type: string
        trust_level: string
        description: string
    
    data_flows:
      - name: string
        source: string
        destination: string
        protocol: string
        data_classification: string
    
    entry_points:
      - name: string
        type: string
        description: string
    
    exit_points:
      - name: string
        type: string
        description: string
  
  threats:
    - threat_id: string
      category: spoofing | tampering | repudiation | information_disclosure | denial_of_service | elevation_of_privilege
      description: string
      affected_component: string
      affected_data_flow: string
      likelihood: high | medium | low
      impact: high | medium | low
      risk_rating: high | medium | low
      mitigations:
        - mitigation_id: string
          description: string
          implemented: boolean
          implementation_date: string | null
          verification: string
      
      residual_risk: high | medium | low
      residual_risk_justification: string
  
  mitigations:
    existing_controls:
      - control_id: string
        description: string
        type: preventive | detective | corrective
        effectiveness: high | medium | low
    
    recommended_controls:
      - control_id: string
        description: string
        priority: high | medium | low
        estimated_effort: string
        owner: string
  
  review:
    review_date: string
    reviewer: string
    findings: [list]
    recommendations: [list]
    next_review_date: string
  
  references:
    - title: string
      url: string
      relevance: string
```

## Review Checklist Template

```yaml
review_checklist:
  checklist_id: string
  review_type: architecture | security | compliance | performance | operational
  system_id: string
  review_date: string
  reviewer: string
  
  general:
    - item: "System register current"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Risk tier assigned and justified"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Architecture decision records present"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Release and evidence checklist available"
      status: pass | fail | na
      evidence: string
      notes: string
  
  security:
    - item: "Threat model complete and current"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Authentication reviewed"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Authorization reviewed"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Secret management verified"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Network controls reviewed"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Data security reviewed"
      status: pass | fail | na
      evidence: string
      notes: string
  
  data:
    - item: "Data inventory current"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Classification applied"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Retention enforced"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Legal hold verified"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Consent managed"
      status: pass | fail | na
      evidence: string
      notes: string
  
  operations:
    - item: "Deployment automation verified"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Rollback tested"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Monitoring configured"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Alerting configured"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Incident response ready"
      status: pass | fail | na
      evidence: string
      notes: string
  
  testing:
    - item: "Evaluation suite passing"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Regression suite passing"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Safety tests included"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Performance tests passing"
      status: pass | fail | na
      evidence: string
      notes: string
  
  compliance:
    - item: "Evidence package complete"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Exception register current"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Training current"
      status: pass | fail | na
      evidence: string
      notes: string
    - item: "Vendor records current"
      status: pass | fail | na
      evidence: string
      notes: string
  
  summary:
    total_items: integer
    passed: integer
    failed: integer
    not_applicable: integer
    pass_rate: number
    overall_status: pass | fail
    blocking_items: [list]
    recommendations: [list]
  
  approval:
    reviewer: string
    date: string
    status: approved | rejected | conditional
    conditions: [list]
    notes: string
```

## Deployment Architecture Template

```yaml
deployment_architecture:
  architecture_id: string
  system_id: string
  environment: development | staging | production
  version: string
  last_updated: string
  
  topology:
    type: monolith | microservices | serverless | hybrid
    description: string
    diagram: string
  
  components:
    - name: string
      type: service | database | cache | queue | storage | cdn | load_balancer
      technology: string
      version: string
      replicas: integer
      resources:
        cpu: string
        memory: string
        storage: string
      configuration: object
      health_check: string
      dependencies: [list]
  
  networking:
    vpc:
      cidr: string
      subnets: [list]
    load_balancing:
      type: string
      configuration: object
    dns:
      records: [list]
    firewall:
      rules: [list]
    tls:
      certificates: [list]
      configuration: object
  
  data_stores:
    - name: string
      type: sql | nosql | cache | search | object
      technology: string
      version: string
      configuration: object
      backup:
        strategy: string
        frequency: string
        retention: string
      replication:
        type: string
        replicas: integer
  
  security:
    authentication:
      mechanism: string
      configuration: object
    authorization:
      model: string
      configuration: object
    secrets:
      management: string
      rotation: string
    encryption:
      at_rest: string
      in_transit: string
    monitoring:
      logging: string
      metrics: string
      tracing: string
  
  scaling:
    horizontal:
      min_replicas: integer
      max_replicas: integer
      target_cpu: number
      target_memory: number
    vertical:
      scale_up_threshold: number
      scale_down_threshold: number
    caching:
      type: string
      ttl: string
      invalidation: string
  
  reliability:
    availability_target: number
    backup:
      strategy: string
      frequency: string
      retention: string
      tested: boolean
    disaster_recovery:
      rto: string
      rpo: string
      strategy: string
      tested: boolean
    circuit_breakers:
      enabled: boolean
      configuration: object
    rate_limiting:
      enabled: boolean
      configuration: object
  
  monitoring:
    metrics:
      provider: string
      dashboards: [list]
      alerts: [list]
    logging:
      provider: string
      retention: string
      aggregation: string
    tracing:
      provider: string
      sampling_rate: number
  
  ci_cd:
    pipeline: string
    stages: [list]
    environments: [list]
    deployment_strategy: blue_green | canary | rolling
    rollback_strategy: string
    approval_required: boolean
    approval_workflow: string
  
  cost:
    estimated_monthly: string
    cost_drivers: [list]
    optimization_opportunities: [list]
  
  contacts:
    owner: string
    technical_lead: string
    on_call: string
    escalation: string
```

## Control Mapping Template

```yaml
control_mapping:
  mapping_id: string
  system_id: string
  version: string
  created_date: string
  last_updated: string
  
  controls:
    - control_id: string
      domain: string
      name: string
      description: string
      priority: P0 | P1 | P2 | P3
      type: preventive | detective | corrective
      implementation: code | configuration | process
      owner: string
      status: implemented | in_progress | planned | exception
      
      evidence:
        required: boolean
        type: automated | manual | hybrid
        description: string
        location: string
        frequency: string
        retention: string
      
      testing:
        required: boolean
        method: unit_test | integration_test | penetration_test | manual_review
        frequency: string
        last_tested: string
        results: string
      
      exceptions:
        has_exception: boolean
        exception_id: string | null
        exception_reason: string | null
        compensating_controls: [list]
        expiry_date: string | null
      
      review:
        review_frequency: string
        last_reviewed: string
        next_review: string
        reviewer: string
  
  coverage:
    total_controls: integer
    implemented: integer
    in_progress: integer
    planned: integer
    with_exception: integer
    coverage_percentage: number
  
  by_domain:
    - domain: string
      total: integer
      implemented: integer
      coverage: number
  
  by_priority:
    - priority: string
      total: integer
      implemented: integer
      coverage: number
  
  gaps:
    - control_id: string
      domain: string
      priority: string
      description: string
      remediation_plan: string
      target_date: string
      owner: string
  
  summary:
    overall_coverage: number
    critical_gaps: [list]
    high_priority_gaps: [list]
    recommendations: [list]
```

## Evidence Package Template

```yaml
evidence_package:
  package_id: string
  system_id: string
  release_id: string
  version: string
  created_date: string
  created_by: string
  
  system_information:
    system_name: string
    risk_tier: string
    owner: string
    domains: [list]
  
  release_information:
    release_type: major | minor | patch | emergency | experimental | maintenance
    candidate_version: string
    baseline_version: string
    change_description: string
  
  evidence:
    - evidence_id: string
      control_id: string
      domain: string
      type: automated | manual | hybrid
      description: string
      location: string
      hash: string
      generated_at: string
      generated_by: string
      valid_until: string
      status: valid | expired | invalid
  
  controls_summary:
    total_controls: integer
    controls_with_evidence: integer
    controls_without_evidence: integer
    coverage_percentage: number
  
  by_priority:
    - priority: string
      total: integer
      with_evidence: integer
      without_evidence: integer
      coverage: number
  
  by_domain:
    - domain: string
      total: integer
      with_evidence: integer
      coverage: number
  
  exceptions:
    - exception_id: string
      control_id: string
      reason: string
      owner: string
      expiry_date: string
      compensating_controls: [list]
  
  validation:
    evidence_links_resolved: boolean
    evidence_timestamps_current: boolean
    evidence_signatures_valid: boolean
    validation_date: string
    validated_by: string
  
  sign_off:
    compliance_officer: string
    compliance_officer_date: string
    security_lead: string
    security_lead_date: string
    release_manager: string
    release_manager_date: string
```

## Compliance Evidence Pack Template

```yaml
compliance_evidence_pack:
  pack_id: string
  system_id: string
  audit_id: string
  audit_date: string
  auditor: string
  
  scope:
    regulations: [list]
    domains: [list]
    controls: [list]
    period: string
  
  evidence:
    - evidence_id: string
      control_id: string
      regulation: string
      requirement: string
      evidence_type: document | configuration | log | report | attestation
      description: string
      location: string
      hash: string
      generated_at: string
      generated_by: string
      status: valid | expired | missing
  
  coverage:
    total_requirements: integer
    requirements_met: integer
    requirements_partial: integer
    requirements_not_met: integer
    coverage_percentage: number
  
  by_regulation:
    - regulation: string
      total_requirements: integer
      met: integer
      coverage: number
  
  by_control:
    - control_id: string
      total_requirements: integer
      met: integer
      coverage: number
  
  gaps:
    - requirement: string
      regulation: string
      control_id: string
      status: not_met | partial
      description: string
      remediation: string
      owner: string
      target_date: string
  
  findings:
    - finding_id: string
      severity: critical | high | medium | low
      regulation: string
      control_id: string
      description: string
      evidence: string
      recommendation: string
      owner: string
      target_date: string
      status: open | in_progress | closed
  
  exceptions:
    - exception_id: string
      control_id: string
      regulation: string
      reason: string
      compensating_controls: [list]
      owner: string
      expiry_date: string
      approved_by: string
  
  sign_off:
    compliance_officer: string
    compliance_officer_date: string
    legal_counsel: string
    legal_counsel_date: string
    auditor: string
    auditor_date: string
```
