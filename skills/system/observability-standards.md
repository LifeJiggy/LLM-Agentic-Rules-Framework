# Observability Standards

Use this guide when implementing logging, metrics, tracing, and monitoring for LLM, agentic, adapter, CLI, IDE, plugin, validation, and release workflows.

## Observability Philosophy

Observability is the ability to understand the internal state of a system from its external outputs. For complex LLM and agentic systems, observability is not optional—it is essential for reliability, debugging, and continuous improvement.

### Three Pillars of Observability

**Logs**
- Discrete events with context
- Structured data for querying
- Timestamped records
- Detailed diagnostic information

**Metrics**
- Numeric measurements over time
- Aggregated data points
- Trends and patterns
- Alerting thresholds

**Traces**
- End-to-end request flows
- Distributed transaction tracking
- Service dependency mapping
- Latency breakdowns

### Observability Goals

**Understand System Behavior**
- What is the system doing?
- Why is it behaving this way?
- How is performance trending?
- Where are bottlenecks?

**Detect Problems Early**
- Identify failures before users notice
- Detect degradation before outages
- Spot anomalies in patterns
- Alert on threshold breaches

**Debug Issues Quickly**
- Trace errors to root cause
- Understand failure context
- Reproduce issues from logs
- Verify fixes with metrics

**Optimize Performance**
- Identify slow operations
- Find resource bottlenecks
- Measure improvement impact
- Capacity planning

## Logging Standards

### Structured Logging Principles

**Use Structured Formats**
- JSON for machine parsing
- Key-value pairs for clarity
- Consistent field names
- Avoid free-text parsing

**Example Structured Log Entry**
```json
{
  "timestamp": "2026-06-04T14:30:00.123Z",
  "level": "ERROR",
  "service": "llm-agent",
  "operation": "model_inference",
  "request_id": "req-12345-abcde",
  "user_id": "user-789",
  "duration_ms": 4500,
  "error": {
    "type": "ModelTimeoutError",
    "message": "Model inference exceeded timeout",
    "stack_trace": "..."
  },
  "context": {
    "model": "gpt-4",
    "prompt_tokens": 1500,
    "max_tokens": 500
  }
}
```

**Include Essential Fields**

Every log entry should include:
- `timestamp`: ISO 8601 format with timezone
- `level`: DEBUG, INFO, WARN, ERROR, FATAL
- `service`: Name of service/component
- `operation`: Operation being performed
- `request_id`: Unique request identifier
- `user_id`: User or system identifier (if applicable)

### Log Levels

**DEBUG**
- Detailed diagnostic information
- Development and troubleshooting
- High volume, not for production
- Examples: Variable values, internal state, detailed flow

**INFO**
- Normal operational events
- Audit trail of significant events
- Low to medium volume
- Examples: Service startup, configuration loaded, user login

**WARN**
- Potential problems
- Degraded performance
- Recoverable errors
- Examples: High latency, retry attempts, deprecated usage

**ERROR**
- Failures that need attention
- Operation failures
- Requires investigation
- Examples: Failed API calls, validation errors, timeouts

**FATAL/CRITICAL**
- System is unusable
- Immediate attention required
- Service shutdown imminent
- Examples: Database connection lost, critical configuration missing

### Logging Best Practices

**1. Log at the Right Level**
- DEBUG: Development and deep debugging
- INFO: Business events and milestones
- WARN: Recoverable problems
- ERROR: Failures requiring attention
- FATAL: System-threatening failures

**2. Include Context**
- Who: User ID, service name
- What: Operation, action, event
- When: Timestamp
- Where: Service, component, file
- Why: Reason for log, error cause
- How: Method, parameters (sanitized)

**3. Be Specific**
- Use descriptive messages
- Include error codes
- Reference specific resources
- Provide actionable information

**4. Avoid Sensitive Data**
- Never log passwords
- Never log API keys or tokens
- Never log credit card numbers
- Never log personal identifying information
- Mask or redact sensitive fields

**5. Make Logs Searchable**
- Use consistent field names
- Include identifiers for correlation
- Use enumerations for status values
- Structure data for querying

**6. Control Volume**
- Log at appropriate frequency
- Use sampling for high-volume events
- Set reasonable log levels
- Avoid logging in tight loops

### Logging Anti-Patterns

**Anti-Pattern: Logging Everything**
- Problem: Too much data, expensive, hard to find signals
- Solution: Log strategically, use appropriate levels

**Anti-Pattern: Logging Nothing**
- Problem: Cannot debug or monitor
- Solution: Log errors, warnings, and key events

**Anti-Pattern: Unstructured Logs**
- Problem: Cannot query or analyze effectively
- Solution: Use structured logging formats

**Anti-Pattern: Logging Secrets**
- Problem: Security vulnerability
- Solution: Never log sensitive data

**Anti-Pattern: Inconsistent Formatting**
- Problem: Difficult to parse and analyze
- Solution: Use logging libraries and formatters

**Anti-Pattern: Logging in Hot Paths**
- Problem: Performance degradation
- Solution: Use sampling, async logging

## Metrics Standards

### Metric Types

**Counter**
- Cumulative value that only increases
- Reset on restart
- Examples: Request count, error count, retry count

**Gauge**
- Value that can go up or down
- Point-in-time measurement
- Examples: Active connections, queue depth, memory usage

**Histogram**
- Distribution of values
- Bucketed measurements
- Examples: Request duration, payload size, processing time

**Summary**
- Similar to histogram but with calculated percentiles
- Pre-computed statistics
- Examples: Response time percentiles, latency distribution

### Golden Signals

The four golden signals of monitoring:

**Latency**
- Time to service requests
- Measure: Request duration distribution
- Alert: P95 or P99 latency exceeds threshold
- Target: < 200ms for P95, < 500ms for P99 (typical)

**Traffic**
- Demand on your system
- Measure: Requests per second
- Alert: Unusual spikes or drops
- Target: Monitor for anomalies

**Errors**
- Rate of failed requests
- Measure: Error count / total count
- Alert: Error rate exceeds threshold
- Target: < 1% error rate typical

**Saturation**
- How "full" is your service
- Measure: Resource utilization
- Alert: Utilization exceeds threshold
- Target: < 70% typical, < 85% warning

### RED Metrics

For services, track:

**Rate**
- Requests per second
- Per endpoint or operation
- By user or client type

**Errors**
- Error rate (errors / total requests)
- Errors by type
- Errors by endpoint

**Duration**
- Response time distribution
- P50, P95, P99 percentiles
- By endpoint and operation

### USE Metrics

For resources, track:

**Utilization**
- Percentage of time resource is busy
- CPU, memory, disk, network

**Saturation**
- How much extra work can resource handle
- Queue depth, backlog

**Errors**
- Error count by resource
- Error rate by resource type

### Metric Naming Conventions

**Format: `<domain>_<component>_<metric>_<unit>`**

Examples:
- `api_requests_total` (counter)
- `api_request_duration_seconds` (histogram)
- `db_connections_active` (gauge)
- `model_inference_duration_seconds` (histogram)
- `agent_tool_calls_total` (counter)
- `queue_messages_processed_total` (counter)
- `cache_hit_rate` (gauge)
- `memory_usage_bytes` (gauge)

### Metric Labels/Tags

Common labels for metrics:

**service**: Name of service
**operation**: Operation or endpoint name
**method**: HTTP method (GET, POST, etc.)
**status_code**: HTTP status code or error code
`error_type`: Type of error
`user_id`: User identifier (hashed for privacy)
`region`: Geographic region
`version`: Service or model version
`result`: Success, failure, timeout

### Metric Collection

**Automatic Collection**
- Framework-level metrics (request count, duration)
- Infrastructure metrics (CPU, memory, disk)
- Database metrics (connections, queries, duration)
- Cache metrics (hit rate, size, evictions)

**Custom Metrics**
- Business metrics (transactions, conversions)
- Domain metrics (model accuracy, relevance)
- Operational metrics (queue depth, batch size)
- Quality metrics (error rate, success rate)

**Metric Aggregation**
- Aggregate at appropriate granularity
- Roll up high-cardinality metrics
- Downsample for long-term storage
- Retain raw data for short periods

### Metric Alerting

**Alert Design Principles**
- Alert on symptoms, not causes
- Alert on user impact
- Avoid alert storms
- Make alerts actionable

**Alert Thresholds**

**Warning Level**
- Indicates potential issues
- Requires monitoring
- May need investigation
- Example: Error rate > 1% for 5 minutes

**Critical Level**
- Requires immediate action
- Service is impacted
- Users are affected
- Example: Error rate > 5% for 2 minutes

**Alert Best Practices**
- Include runbook links
- Provide context and impact
- Suggest initial investigation steps
- Define escalation procedures
- Set appropriate severity levels

## Tracing Standards

### Distributed Tracing

**Trace Structure**
- Trace: End-to-end request flow
- Span: Individual operation within trace
- Parent-child relationships between spans
- Timing and status information

**Trace Context Propagation**
- Propagate trace ID across services
- Include span ID for relationships
- Include trace flags (sampling, debug)
- Use standard formats (W3C Trace Context)

**Span Attributes**
- Service name
- Operation name
- Start and end timestamps
- Status (OK, ERROR, UNSET)
- Error messages and stack traces
- Tags for additional context
- Logs within spans

### Trace Implementation

**Python (OpenTelemetry)**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracer
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({"service.name": "llm-agent"})
))
tracer = trace.get_tracer(__name__)

# Create spans
def process_request(request):
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("request.id", request.id)
        span.set_attribute("user.id", request.user_id)
        
        # Call model
        with tracer.start_as_current_span("model_inference") as model_span:
            model_span.set_attribute("model.name", "gpt-4")
            response = call_model(request)
        
        # Process response
        with tracer.start_as_current_span("process_response") as resp_span:
            result = format_response(response)
        
        return result
```

**JavaScript (OpenTelemetry)**
```javascript
import { NodeTracerProvider } from '@opentelemetry/sdk-trace-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';

const provider = new NodeTracerProvider({
  resource: { 'service.name': 'llm-agent' }
});
provider.addSpanProcessor(new BatchSpanProcessor(new JaegerExporter()));
provider.register();

const tracer = trace.getTracer(__name);

async function processRequest(request) {
  return tracer.startActiveSpan('process_request', async (span) => {
    span.setAttribute('request.id', request.id);
    span.setAttribute('user.id', request.user_id);
    
    const modelSpan = tracer.startSpan('model_inference');
    const response = await callModel(request);
    modelSpan.setAttribute('model.name', 'gpt-4');
    modelSpan.end();
    
    const responseSpan = tracer.startSpan('process_response');
    const result = await formatResponse(response);
    responseSpan.end();
    
    span.end();
    return result;
  });
}
```

### Trace Sampling

**Sampling Strategies**

**Always On (Development)**
- Sample 100% of traces
- No sampling decisions
- Complete visibility
- High overhead

**Probabilistic (Staging)**
- Sample fixed percentage
- Example: 10% of traces
- Balance visibility and overhead
- Configurable rate

**Rate Limiting (Production)**
- Limit traces per second
- Example: 100 traces/second
- Prevent overload
- Maintain visibility

**Adaptive Sampling**
- Adjust rate based on system load
- Sample more during low load
- Sample less during high load
- Optimize visibility and overhead

**Tail-Based Sampling**
- Sample based on trace outcome
- Always sample errors
- Sample slow traces
- Sample representative successes

### Trace Analysis

**Trace Queries**
- Find traces by service
- Find traces with errors
- Find slow traces
- Find traces by user or request ID
- Find traces by operation

**Trace Visualization**
- Waterfall view of spans
- Service dependency map
- Latency breakdown
- Error highlighting
- Critical path identification

## Alerting Standards

### Alert Design

**Good Alerts**
- Actionable: Clear what to do
- Understandable: Clear what is wrong
- Relevant: Matters to recipients
- Timely: Not too early, not too late
- Accurate: Few false positives

**Bad Alerts**
- Vague: "Something is wrong"
- Overwhelming: Too many alerts
- Noisy: Many false positives
- Ignored: Alert fatigue
- Delayed: Alert too late to act

### Alert Categories

**Availability Alerts**
- Service down
- Health check failing
- Dependency unavailable
- Response rate drops

**Performance Alerts**
- Latency increases
- Throughput drops
- Resource saturation
- Queue depth increases

**Error Alerts**
- Error rate spikes
- New error types
- Error pattern changes
- Critical errors

**Business Alerts**
- Transaction failures
- Conversion rate drops
- User experience degradation
- SLA breaches

### Alert Severity Levels

**P0 - Critical**
- Service is down or severely degraded
- Data loss is occurring
- Security breach suspected
- Immediate action required
- Page on-call engineer

**P1 - High**
- Service is degraded
- Many users affected
- Significant business impact
- Action required within 1 hour
- Notify on-call engineer

**P2 - Medium**
- Service has issues
- Some users affected
- Minor business impact
- Action required within 4 hours
- Create ticket for next business day

**P3 - Low**
- Minor issues
- No user impact
- Cosmetic problems
- Action when convenient
- Add to backlog

### Alert Content

**Alert Should Include**
- What is wrong
- Impact assessment
- Time of occurrence
- Location/service affected
- Current status
- Runbook link
- Escalation path

**Example Alert**
```
CRITICAL: API Error Rate High

Service: llm-agent-api
Error Rate: 15% (threshold: 5%)
Duration: 3 minutes
Impact: Users experiencing failures

Runbook: https://wiki.company.com/runbooks/api-errors
On-Call: @oncall-engineer

Current Status:
- P95 Latency: 2.3s (normal: 500ms)
- Error Rate: 15% (threshold: 5%)
- Active Users: 1,250 (normal: 2,000)

Initial Investigation:
1. Check service logs for error patterns
2. Check dependent services (model-api, database)
3. Check recent deployments

Escalation: If not resolved in 15 minutes, escalate to tech lead.
```

### Alert Routing

**Alert Routing Matrix**
| Severity | Channel | Response Time | Escalation |
|----------|---------|---------------|------------|
| P0 | Page + Slack | 5 minutes | Tech Lead (15m), Manager (30m) |
| P1 | Slack + Email | 15 minutes | Tech Lead (1h), Manager (4h) |
| P2 | Ticket | 4 hours | Next business day |
| P3 | Ticket | Next sprint | Next planning |

## Monitoring Standards

### What to Monitor

**Infrastructure**
- CPU utilization
- Memory usage
- Disk space and I/O
- Network bandwidth and latency
- Process count and health
- Container metrics (if applicable)
- Cloud resource metrics

**Application**
- Request rate and volume
- Error rate and types
- Response time distribution
- Active users/connections
- Queue depths and processing rates
- Cache hit/miss rates
- Session count and duration

**Dependencies**
- External API availability
- Database performance
- Message queue metrics
- Cache performance
- CDN metrics
- Third-party service status

**Business**
- Transaction volume
- Conversion rates
- User engagement
- Feature adoption
- Revenue metrics
- Customer satisfaction

### Monitoring Architecture

**Three-Tier Monitoring**

**Tier 1: Infrastructure Monitoring**
- Host-level metrics
- Network monitoring
- Storage monitoring
- Basic health checks

**Tier 2: Application Monitoring**
- Application metrics
- Service health
- Dependency health
- Performance metrics

**Tier 3: Business Monitoring**
- Business metrics
- User experience metrics
- SLA compliance
- Business impact

### Dashboard Design

**Dashboard Hierarchy**

**Executive Dashboard**
- High-level business metrics
- SLA compliance
- Major incident status
- Key performance indicators

**Operations Dashboard**
- Service health
- Error rates
- Performance metrics
- Resource utilization

**Development Dashboard**
- Feature metrics
- A/B test results
- Deployment status
- Code quality metrics

**Dashboard Best Practices**
- Keep it simple and focused
- Use consistent color coding
- Show trends, not just current values
- Include context (baselines, targets)
- Make drill-downs available
- Update frequency appropriate to metric

## Log Aggregation

### Log Collection

**Collection Methods**
- Agent-based collection (Filebeat, Fluentd)
- API-based collection
- Sidecar containers
- Direct integration

**Collection Requirements**
- Reliable delivery (no data loss)
- Minimal performance impact
- Secure transmission (TLS)
- Buffering for reliability

### Log Storage

**Storage Tiers**

**Hot Storage (7-30 days)**
- Full fidelity logs
- Fast query performance
- Expensive storage
- For active investigation

**Warm Storage (30-90 days)**
- Compressed logs
- Slower queries
- Medium cost
- For recent analysis

**Cold Storage (90+ days)**
- Highly compressed
- Very slow queries
- Low cost
- For compliance and audit

### Log Analysis

**Query Patterns**
- Search by service
- Filter by time range
- Aggregate by field
- Correlate across services

**Analysis Tools**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Datadog
- CloudWatch Logs Insights
- Grafana Loki

## Metric Aggregation

### Aggregation Methods

**Sum**
- Total count of events
- Examples: Total requests, total errors

**Average**
- Mean value over time
- Examples: Average response time, average CPU

**Percentile**
- Distribution percentiles
- Examples: P50, P95, P99 latency
- Better than average for latency

**Rate**
- Events per time unit
- Examples: Requests per second

**Histogram**
- Distribution of values
- Bucketed data
- Examples: Request duration buckets

### Metric Retention

**Retention Policy**
- High-resolution metrics: 1 minute for 15 days
- Medium-resolution: 5 minutes for 90 days
- Low-resolution: 1 hour for 1 year
- Long-term: 1 day for 7 years

**Retention Considerations**
- Compliance requirements
- Storage costs
- Query performance
- Business needs

## Health Checks

### Health Check Design

**Liveness Probe**
- Is the service running?
- Simple check
- Restarts service if failing
- Example: Process is running, port is open

**Readiness Probe**
- Is the service ready for traffic?
- More comprehensive
- Removes from load balancer if failing
- Example: Database connection, dependencies available

**Startup Probe**
- Has the service finished starting?
- Prevents premature health checks
- Example: Configuration loaded, migrations complete

### Health Check Endpoints

**/health**
- Overall health status
- Quick check
- Returns 200 if healthy, 503 if not

**/health/ready**
- Readiness check
- Checks dependencies
- Returns detailed status

**/health/live**
- Liveness check
- Basic process health
- Returns simple status

**Implementation**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.2.3',
        'checks': {
            'database': check_database(),
            'cache': check_cache(),
            'model_api': check_model_api(),
        }
    }), 200 if all_checks_pass() else 503

def check_database():
    try:
        db.execute('SELECT 1')
        return {'status': 'healthy'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}
```

## Observability Implementation by Component

### LLM and AI Systems

**Model Inference Observability**
- Inference duration
- Token count (input/output)
- Model version
- Prompt and response (sanitized)
- Error types and rates
- Fallback model usage

**Prompt Observability**
- Prompt length and tokens
- Prompt validation results
- Injection attempts detected
- Prompt template versions

**Response Observability**
- Response length and tokens
- Response validation results
- Content filter triggers
- Quality metrics

### Agentic Systems

**Agent Execution Observability**
- Agent step duration
- Tool call count and duration
- Decision points and reasoning
- State transitions
- Error types and recovery

**Tool Usage Observability**
- Tool call success/failure
- Tool call duration
- Tool input/output sizes
- Tool availability
- Tool fallback usage

**Workflow Observability**
- Workflow step completion
- Workflow duration
- Workflow failures and retries
- Workflow branching decisions
- Workflow outcome

### Adapter Systems

**Adapter Performance**
- Adapter call duration
- Adapter success/failure rate
- Adapter fallback activation
- Adapter version compatibility

**Adapter Errors**
- Adapter-specific errors
- Error patterns by adapter
- Error recovery success
- Timeout and retry metrics

### CLI and IDE Tools

**Command Execution**
- Command execution duration
- Command success/failure
- Command arguments (sanitized)
- Exit codes
- Output size

**User Interaction**
- Command frequency
- Help usage
- Error frequency
- Feature usage

### Plugin Systems

**Plugin Loading**
- Plugin load duration
- Plugin load success/failure
- Plugin version compatibility
- Plugin dependency resolution

**Plugin Execution**
- Plugin call duration
- Plugin success/failure
- Plugin resource usage
- Plugin error types

### Validation Systems

**Validation Execution**
- Validation duration
- Validation pass/fail rate
- Validation rule execution
- Validation error types

**Validation Results**
- Pass/fail counts by rule
- Validation coverage
- False positive/negative rates
- Validation confidence

## Observability for Specific Scenarios

### Release Monitoring

**Pre-Release**
- Baseline metrics established
- Health checks passing
- Monitoring active
- Alerts configured

**During Release**
- Deployment events logged
- Metrics tracked during rollout
- Error rates monitored
- Performance compared to baseline

**Post-Release**
- Metrics validated
- No unexpected alerts
- Performance stable
- User impact minimal

### Incident Investigation

**Investigation Process**
1. Identify incident time
2. Check error logs
3. Review metrics around incident
4. Trace affected requests
5. Identify root cause
6. Document findings

**Investigation Tools**
- Log aggregation search
- Metric dashboards
- Distributed tracing
- Alert history
- Deployment history

### Performance Optimization

**Optimization Process**
1. Identify slow operations
2. Profile execution
3. Analyze metrics
4. Implement improvements
5. Measure impact
6. Iterate

**Optimization Metrics**
- Before/after latency
- Throughput improvement
- Resource utilization
- User experience impact

### Capacity Planning

**Planning Process**
1. Analyze current usage
2. Project growth
3. Identify bottlenecks
4. Plan capacity additions
5. Monitor after changes

**Capacity Metrics**
- Current utilization
- Growth rate
- Time to capacity limit
- Cost per unit capacity

## Observability Automation

### Automated Alerting

**Alert Generation**
- Threshold-based alerts
- Anomaly detection
- Machine learning alerts
- Composite alerts

**Alert Enrichment**
- Add context automatically
- Link to runbooks
- Include recent changes
- Suggest remediation

**Alert Correlation**
- Group related alerts
- Identify root cause alerts
- Suppress secondary alerts
- Create incident from alerts

### Automated Remediation

**Remediation Triggers**
- Clear failure conditions
- Known fixes
- Low risk actions
- Reversible changes

**Remediation Actions**
- Restart service
- Clear cache
- Scale resources
- Rollback deployment
- Failover to backup

**Remediation Safety**
- Require approval for high-risk actions
- Log all remediation actions
- Verify remediation success
- Alert on remediation actions

### Automated Analysis

**Log Analysis**
- Pattern detection
- Anomaly detection
- Correlation analysis
- Root cause suggestion

**Metric Analysis**
- Trend analysis
- Forecasting
- Anomaly detection
- Performance regression detection

**Trace Analysis**
- Bottleneck identification
- Service dependency analysis
- Error pattern analysis
- Optimization suggestions

## Observability Maturity Model

### Level 1: Basic Monitoring
- Health checks implemented
- Basic metrics collected
- Alerts configured for critical issues
- Logs collected centrally

### Level 2: Proactive Monitoring
- Comprehensive metrics
- Alerting with runbooks
- Dashboard for key metrics
- Log querying capabilities

### Level 3: Advanced Observability
- Distributed tracing
- Structured logging
- Custom business metrics
- Automated alerting

### Level 4: Predictive Observability
- ML-based anomaly detection
- Automated root cause analysis
- Predictive alerting
- Self-healing systems

## Observability Checklist

### Logging Checklist

- [ ] Structured logging implemented
- [ ] Essential fields included in all logs
- [ ] Appropriate log levels used
- [ ] Sensitive data is not logged
- [ ] Log aggregation configured
- [ ] Log retention policy defined
- [ ] Log search and querying available
- [ ] Log-based alerts configured
- [ ] Log samples reviewed regularly

### Metrics Checklist

- [ ] Golden signals monitored
- [ ] RED/USE metrics collected
- [ ] Custom business metrics defined
- [ ] Metric naming conventions followed
- [ ] Metrics aggregated appropriately
- [ ] Dashboards created for key metrics
- [ ] Alerts configured with thresholds
- [ ] Metric retention policy defined
- [ ] Metrics reviewed regularly

### Tracing Checklist

- [ ] Distributed tracing implemented
- [ ] Trace context propagated
- [ ] Sampling strategy defined
- [ ] Trace storage configured
- [ ] Trace visualization available
- [ ] Trace-based debugging used
- [ ] Performance traces analyzed
- [ ] Error traces investigated

### Alerting Checklist

- [ ] Alerts are actionable
- [ ] Alert thresholds are appropriate
- [ ] Alert routing configured
- [ ] Runbooks linked to alerts
- [ ] Escalation paths defined
- [ ] Alert fatigue prevented
- [ ] Alert review process exists
- [ ] Incident response integrated

### Monitoring Checklist

- [ ] Infrastructure monitored
- [ ] Application monitored
- [ ] Dependencies monitored
- [ ] Business metrics monitored
- [ ] Dashboards created
- [ ] On-call rotation established
- [ ] Monitoring coverage verified
- [ ] Monitoring tested regularly

## Appendix: Observability Tools

### Logging Tools
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- Datadog Logs
- CloudWatch Logs
- Grafana Loki
- Fluentd
- Filebeat

### Metrics Tools
- Prometheus + Grafana
- Datadog Metrics
- CloudWatch Metrics
- New Relic
- StatsD
- InfluxDB

### Tracing Tools
- Jaeger
- Zipkin
- OpenTelemetry
- Datadog APM
- New Relic APM
- AWS X-Ray

### Alerting Tools
- Alertmanager (Prometheus)
- PagerDuty
- Opsgenie
- VictorOps
- Slack alerts
- Email alerts

## Appendix: Observability Patterns

### Correlation ID Pattern

Generate and propagate correlation IDs:

```python
import uuid

class CorrelationContext:
    def __init__(self):
        self.request_id = str(uuid.uuid4())
        self.parent_id = None
        self.trace_id = str(uuid.uuid4())
    
    def to_dict(self):
        return {
            'request_id': self.request_id,
            'parent_id': self.parent_id,
            'trace_id': self.trace_id,
        }
```

### Log Enrichment Pattern

Enrich logs with context at entry points:

```python
class LogEnricher:
    def __init__(self, context):
        self.context = context
    
    def enrich(self, record):
        record['request_id'] = self.context.request_id
        record['user_id'] = self.context.user_id
        record['timestamp'] = datetime.now().isoformat()
        return record
```

### Metric Tagging Pattern

Tag metrics with consistent dimensions:

```python
class MetricTagger:
    @staticmethod
    def tag_operation(operation_name, **kwargs):
        tags = {'operation': operation_name}
        tags.update(kwargs)
        return tags
    
    @staticmethod
    def tag_error(error_type, service, operation):
        return {
            'error_type': error_type,
            'service': service,
            'operation': operation,
        }
```
