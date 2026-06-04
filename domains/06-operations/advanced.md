# Operations Domain - Advanced Concepts

## Overview

This document covers advanced operations concepts for LLM/agentic systems, including deployment patterns, scaling strategies, observability, incident response, disaster recovery, GitOps, service mesh, capacity planning, and production excellence.

---

## Table of Contents

1. [Advanced Deployment Patterns](#1-advanced-deployment-patterns)
2. [Auto-Scaling Strategies](#2-auto-scaling-strategies)
3. [Observability and Monitoring](#3-observability-and-monitoring)
4. [Incident Response](#4-incident-response)
5. [Disaster Recovery](#5-disaster-recovery)
6. [GitOps for Agent Systems](#6-gitops-for-agent-systems)
7. [Service Mesh Integration](#7-service-mesh-integration)
8. [Capacity Planning](#8-capacity-planning)
9. [Chaos Engineering](#9-chaos-engineering)
10. [Production Excellence](#10-production-excellence)

---

## 1. Advanced Deployment Patterns

### Blue-Green Deployment

```yaml
# Kubernetes deployment strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      version: blue
  template:
    metadata:
      labels:
        version: blue
    spec:
      containers:
      - name: agent
        image: agent:latest
        env:
        - name: DEPLOYMENT_COLOR
          value: "blue"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-green
spec:
  replicas: 0  # Initially scaled to 0
  selector:
    matchLabels:
      version: green
```

### Canary Deployment

```python
class CanaryDeployer:
    """Gradual rollout with monitoring."""
    
    def __init__(self, k8s_client, health_checker):
        self.k8s = k8s_client
        self.health = health_checker
        self.traffic_split = {"v1": 95, "v2": 5}
    
    async def deploy_canary(self, canary_image: str, step: int = 5):
        """Deploy canary with step-by-step traffic increase."""
        await self._deploy_new_version(canary_image)
        
        while self.traffic_split["v2"] < 100:
            if await self._health_check():
                self.traffic_split["v2"] += step
                self.traffic_split["v1"] -= step
                await self._update_traffic_split()
            else:
                await self._rollback()
                break
            
            await asyncio.sleep(60)  # Wait between steps
    
    async def _deploy_new_version(self, image: str):
        await self.k8s.patch_deployment(
            "agent-v2",
            {"spec": {"template": {"spec": {
                "containers": [{"name": "agent", "image": image}]
            }}}}
        )
    
    async def _update_traffic_split(self):
        # Update Istio VirtualService
        virtual_service = {
            "spec": {
                "http": [{"route": [
                    {"destination": {"host": "agent", "subset": "v1"}, 
                     "weight": self.traffic_split["v1"]},
                    {"destination": {"host": "agent", "subset": "v2"}, 
                     "weight": self.traffic_split["v2"]}
                ]}]
            }
        }
        await self.k8s.apply("virtualservice-agent", virtual_service)
```

### Rolling Update Strategy

```python
class RollingUpdater:
    def __init__(self, k8s_client):
        self.k8s = k8s_client
        self.progress_timeout = 600
        self.interval = 10
    
    async def rolling_update(self, deployment: str, new_image: str, 
                             max_unavailable: str = "25%", 
                             max_surge: str = "25%"):
        patch = {
            "spec": {
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {
                        "maxUnavailable": max_unavailable,
                        "maxSurge": max_surge
                    }
                },
                "template": {
                    "spec": {
                        "containers": [{
                            "name": "agent",
                            "image": new_image
                        }]
                    }
                }
            }
        }
        await self.k8s.patch_deployment(deployment, patch)
        await self._wait_for_rollout(deployment)
    
    async def _wait_for_rollout(self, deployment: str):
        start = time.time()
        while time.time() - start < self.progress_timeout:
            status = await self.k8s.get_deployment_status(deployment)
            if status["replicas"] == status["updated_replicas"] == status["available_replicas"]:
                return True
            await asyncio.sleep(self.interval)
        raise RolloutTimeout(f"Deployment {deployment} did not complete in time")
```

### Feature Flag Driven Deployment

```python
class FeatureFlagDeployer:
    def __init__(self, flag_client, traffic_router):
        self.flags = flag_client
        self.router = traffic_router
    
    async def promote(self, feature: str, stages: list):
        for stage in stages:
            await self._apply_stage(feature, stage)
            await self._wait_and_evaluate(feature, stage)
    
    async def _apply_stage(self, feature: str, stage: dict):
        if stage["type"] == "percentage":
            await self.flags.set_percentage(feature, stage["value"])
        elif stage["type"] == "allow_list":
            await self.flags.set_allow_list(feature, stage["users"])
        elif stage["type"] == "organization":
            await self.flags.set_org_allow_list(feature, stage["orgs"])
    
    async def _wait_and_evaluate(self, feature: str, stage: dict):
        duration = stage.get("duration_minutes", 30)
        await asyncio.sleep(duration * 60)
        metrics = await self._get_feature_metrics(feature)
        if not self._is_healthy(metrics):
            await self.flags.disable(feature)
            raise PromotionError(f"Feature {feature} failed health check")
```

### Immutable Infrastructure

```python
class ImmutableDeployer:
    def __init__(self, image_builder, k8s_client):
        self.builder = image_builder
        self.k8s = k8s_client
    
    async def deploy(self, source_ref: str, version: str) -> str:
        image = await self.builder.build(source_ref, version)
        await self.builder.scan(image)
        
        deployment_name = f"agent-{version}"
        await self.k8s.create_deployment(deployment_name, image=image)
        await self.k8s.create_service(deployment_name)
        await self.k8s.create_ingress(deployment_name)
        
        return deployment_name
```

---

## 2. Auto-Scaling Strategies

### Agent-Aware Autoscaling

```python
class AgentAutoscaler:
    """Scale based on agent workload metrics."""
    
    def __init__(self, k8s_client):
        self.k8s = k8s_client
        self.scaling_policies = {
            "low": {"min": 2, "max": 5, "cpu": 50, "mem": 70},
            "medium": {"min": 3, "max": 10, "cpu": 60, "mem": 80},
            "high": {"min": 5, "max": 20, "cpu": 70, "mem": 85}
        }
    
    async def scale_for_workload(self, request_rate: int, error_rate: float):
        baseline_replicas = self._calculate_baseline(request_rate)
        error_adjustment = self._adjust_for_errors(error_rate)
        
        target_replicas = min(
            baseline_replicas + error_adjustment,
            self.scaling_policies["high"]["max"]
        )
        
        await self.k8s.patch_hpa(
            "agent-hpa",
            {"spec": {"maxReplicas": target_replicas}}
        )
    
    def _calculate_baseline(self, rate: int) -> int:
        if rate < 100:
            return self.scaling_policies["low"]["min"]
        elif rate < 1000:
            return self.scaling_policies["medium"]["min"]
        else:
            return self.scaling_policies["high"]["min"]
    
    def _adjust_for_errors(self, error_rate: float) -> int:
        if error_rate > 0.1:
            return 3
        return 0
```

### Predictive Scaling

```python
class PredictiveScaler:
    def __init__(self, metrics_store, model_path: str):
        self.metrics = metrics_store
        self.model = self._load_model(model_path)
        self.prediction_horizon_hours = 2
    
    def _load_model(self, path: str):
        # Load trained time-series forecasting model
        pass
    
    async def predict_load(self) -> dict:
        history = await self.metrics.get_last_24h()
        features = self._extract_features(history)
        prediction = self.model.predict(features, horizon=self.prediction_horizon_hours)
        return {
            "predicted_qps": prediction["qps"],
            "predicted_latency": prediction["latency"],
            "recommended_replicas": self._replicas_for(prediction["qps"])
        }
    
    def _extract_features(self, history: list) -> dict:
        return {
            "qps_1h_avg": mean([h["qps"] for h in history[-12:]]),
            "qps_24h_avg": mean([h["qps"] for h in history]),
            "hour_of_day": datetime.utcnow().hour,
            "day_of_week": datetime.utcnow().weekday()
        }
    
    def _replicas_for(self, qps: float) -> int:
        return max(2, math.ceil(qps / 100))
```

### Queue-Based Scaling

```python
class QueueScalePolicy:
    def __init__(self, queue_client, deployment_client):
        self.queue = queue_client
        self.deployment = deployment_client
    
    async def evaluate(self, queue_name: str):
        depth = await self.queue.depth(queue_name)
        wait_time = await self.queue.avg_wait_time(queue_name)
        
        target_replicas = self._calculate_replicas(depth, wait_time)
        current = await self.deployment.replicas("agent-worker")
        
        if target_replicas != current:
            await self.deployment.scale("agent-worker", target_replicas)
    
    def _calculate_replicas(self, depth: int, wait_time: float) -> int:
        if wait_time > 5.0:
            return max(5, math.ceil(depth / 10))
        elif depth > 1000:
            return max(3, math.ceil(depth / 100))
        return 2
```

### Spot Instance Autoscaling

```python
class SpotInstanceScaler:
    def __init__(self, node_group_manager):
        self.manager = node_group_manager
    
    async def optimize(self):
        spot_nodes = await self.manager.get_nodes("spot")
        on_demand_nodes = await self.manager.get_nodes("on-demand")
        
        spot_util = self._avg_utilization(spot_nodes)
        on_demand_util = self._avg_utilization(on_demand_nodes)
        
        if spot_util > 0.8 and on_demand_util < 0.5:
            # Shift workload to on-demand since spot is expensive/unreliable
            await self.manager.set_desired_capacity("spot", len(spot_nodes) - 2)
            await self.manager.set_desired_capacity("on-demand", len(on_demand_nodes) + 2)
        
        elif spot_util < 0.3:
            await self.manager.set_desired_capacity("spot", len(spot_nodes) + 3)
```

---

## 3. Observability and Monitoring

### Comprehensive Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

class AgentMetrics:
    """Production metrics for agent systems."""
    
    REQUESTS = Counter(
        "agent_requests_total",
        "Total agent requests",
        ["method", "endpoint", "status"]
    )
    DURATION = Histogram(
        "agent_request_duration_seconds",
        "Request duration",
        ["endpoint", "model"]
    )
    ACTIVE_SESSIONS = Gauge(
        "agent_active_sessions",
        "Number of active sessions"
    )
    TOKEN_USAGE = Counter(
        "agent_tokens_total",
        "Total tokens consumed",
        ["model", "direction"]
    )
    ERROR_TYPES = Counter(
        "agent_errors_total",
        "Errors by type",
        ["error_type", "endpoint"]
    )
    
    @classmethod
    def record_request(cls, method: str, endpoint: str, status: int, 
                     duration: float, model: str = "unknown"):
        cls.REQUESTS.labels(method=method, endpoint=endpoint, 
                          status=str(status)).inc()
        if status < 400:
            cls.DURATION.labels(endpoint=endpoint, model=model).observe(duration)
    
    @classmethod
    def record_tokens(cls, count: int, model: str, direction: str):
        cls.TOKEN_USAGE.labels(model=model, direction=direction).inc(count)
```

### Distributed Tracing

```python
import uuid
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=14268,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

class TracedAgent:
    def __init__(self, agent):
        self.agent = agent
    
    async def process(self, prompt: str, session_id: str, context: dict):
        with tracer.start_as_current_span("agent.process") as span:
            span.set_attribute("session_id", session_id)
            span.set_attribute("prompt_length", len(prompt))
            try:
                result = await self.agent.process(prompt, session_id, context)
                span.set_attribute("status", "success")
                return result
            except Exception as e:
                span.set_attribute("status", "error")
                span.record_exception(e)
                raise
```

### Health Check System

```python
class HealthCheckSystem:
    def __init__(self):
        self.checks = {}
        self.results = {}
    
    def register(self, name: str, check_fn, critical: bool = True, timeout: int = 5):
        self.checks[name] = {
            "fn": check_fn,
            "critical": critical,
            "timeout": timeout
        }
    
    async def run_checks(self) -> dict:
        results = {}
        for name, check in self.checks.items():
            try:
                result = await asyncio.wait_for(check["fn"](), timeout=check["timeout"])
                results[name] = {"status": "healthy", "result": result}
            except asyncio.TimeoutError:
                results[name] = {"status": "timeout", "critical": check["critical"]}
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
        
        self.results = results
        overall = all(r["status"] == "healthy" for r in results.values())
        return {"healthy": overall, "checks": results}
    
    def is_healthy(self) -> bool:
        if not self.results:
            return False
        return all(r["status"] == "healthy" for r in self.results.values())
```

### Alert Management

```python
class AlertManager:
    def __init__(self, notifier):
        self.notifier = notifier
        self.rules = {}
        self.active_alerts = {}
    
    def add_rule(self, name: str, condition, severity: str, 
                 message: str, cooldown: int = 300):
        self.rules[name] = {
            "condition": condition,
            "severity": severity,
            "message": message,
            "cooldown": cooldown,
            "last_triggered": 0
        }
    
    async def evaluate(self, metrics: dict):
        for rule_name, rule in self.rules.items():
            now = time.time()
            if now - rule["last_triggered"] < rule["cooldown"]:
                continue
            if rule["condition"](metrics):
                await self.notifier.send({
                    "alert": rule_name,
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "timestamp": datetime.utcnow().isoformat()
                })
                rule["last_triggered"] = now
                self.active_alerts[rule_name] = {
                    "triggered_at": now,
                    "metrics": metrics
                }
    
    async def resolve(self, rule_name: str):
        if rule_name in self.active_alerts:
            del self.active_alerts[rule_name]
            await self.notifier.send({
                "alert": rule_name,
                "status": "resolved",
                "timestamp": datetime.utcnow().isoformat()
            })
```

### Log Aggregation

```python
class LogAggregator:
    def __init__(self, sink):
        self.sink = sink
        self.buffer = []
        self.flush_interval = 5
        self.buffer_size = 1000
    
    async def log(self, level: str, message: str, **kwargs):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        self.buffer.append(entry)
        if len(self.buffer) >= self.buffer_size:
            await self.flush()
    
    async def flush(self):
        if not self.buffer:
            return
        await self.sink.write_batch(self.buffer)
        self.buffer.clear()
    
    async def start_periodic_flush(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            await self.flush()
```

### Audit Trail

```python
class AuditLogger:
    def __init__(self, storage):
        self.storage = storage
    
    async def log(self, actor: str, action: str, resource: str, 
                  outcome: str, metadata: dict = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "actor": actor,
            "action": action,
            "resource": resource,
            "outcome": outcome,
            "metadata": metadata or {},
            "source_ip": request.remote_addr if request else None
        }
        await self.storage.append("audit", entry)
    
    async def query(self, filters: dict) -> list:
        return await self.storage.query("audit", filters)
```

---

## 4. Incident Response

### Automated Alerting

```python
class IncidentDetector:
    """Detect and alert on operational issues."""
    
    def __init__(self, alert_manager):
        self.alert_manager = alert_manager
        self.thresholds = {
            "error_rate": 0.05,
            "latency_p95": 10,
            "token_usage_per_minute": 100000
        }
    
    async def check_health(self, metrics: Dict):
        if metrics["error_rate"] > self.thresholds["error_rate"]:
            await self._alert_error_spike(metrics)
        
        if metrics["latency"] > self.thresholds["latency_p95"]:
            await self._alert_performance_degradation(metrics)
    
    async def _alert_error_spike(self, metrics):
        await self.alert_manager.send({
            "severity": "critical",
            "summary": "High error rate detected",
            "description": f"Error rate: {metrics['error_rate']:.2%}",
            "labels": {"team": "ml", "service": "agent"}
        })
```

### Incident Lifecycle Management

```python
class IncidentLifecycle:
    def __init__(self, notifier, on_call):
        self.notifier = notifier
        self.on_call = on_call
        self.states = {}
    
    async def create(self, severity: str, description: str, detected_by: str):
        incident_id = str(uuid.uuid4())
        self.states[incident_id] = {
            "id": incident_id,
            "severity": severity,
            "description": description,
            "state": "open",
            "detected_by": detected_by,
            "assigned_to": self.on_call.current(),
            "created_at": datetime.utcnow(),
            "timeline": [{
                "time": datetime.utcnow().isoformat(),
                "event": "incident_created",
                "actor": detected_by
            }]
        }
        await self._notify_created(incident_id)
        return incident_id
    
    async def acknowledge(self, incident_id: str, responder: str):
        incident = self.states.get(incident_id)
        if not incident:
            return
        incident["state"] = "acknowledged"
        incident["assigned_to"] = responder
        incident["acknowledged_at"] = datetime.utcnow()
        incident["timeline"].append({
            "time": datetime.utcnow().isoformat(),
            "event": "incident_acknowledged",
            "actor": responder
        })
        await self.notifier.update(incident)
    
    async def resolve(self, incident_id: str, resolver: str, resolution: str):
        incident = self.states.get(incident_id)
        if not incident:
            return
        incident["state"] = "resolved"
        incident["resolved_by"] = resolver
        incident["resolved_at"] = datetime.utcnow()
        incident["resolution"] = resolution
        incident["timeline"].append({
            "time": datetime.utcnow().isoformat(),
            "event": "incident_resolved",
            "actor": resolver,
            "details": resolution
        })
        await self.notifier.resolve(incident)
    
    async def escalate(self, incident_id: str, reason: str):
        incident = self.states.get(incident_id)
        if not incident:
            return
        incident["state"] = "escalated"
        incident["timeline"].append({
            "time": datetime.utcnow().isoformat(),
            "event": "escalated",
            "reason": reason
        })
        await self.notifier.escalate(incident)
```

### Blameless Post-Mortem Process

```python
class PostMortemManager:
    def __init__(self, storage, notifier):
        self.storage = storage
        self.notifier = notifier
    
    async def create(self, incident_id: str, participants: list) -> str:
        incident = await self.storage.get_incident(incident_id)
        post_mortem_id = f"pm-{incident_id}"
        
        post_mortem = {
            "id": post_mortem_id,
            "incident_id": incident_id,
            "participants": participants,
            "status": "draft",
            "timeline": self._build_timeline(incident),
            "root_cause": None,
            "action_items": [],
            "created_at": datetime.utcnow().isoformat()
        }
        await self.storage.save(post_mortem_id, post_mortem)
        return post_mortem_id
    
    def _build_timeline(self, incident: dict) -> list:
        return [
            {
                "timestamp": incident["created_at"],
                "event": "Incident detected",
                "source": "monitoring"
            },
            {
                "timestamp": incident.get("acknowledged_at"),
                "event": f"Acknowledged by {incident.get('assigned_to')}"
            },
            {
                "timestamp": incident.get("resolved_at"),
                "event": f"Resolved by {incident.get('resolved_by')}: {incident.get('resolution')}"
            }
        ]
    
    async def finalize(self, post_mortem_id: str, action_items: list):
        pm = await self.storage.get(post_mortem_id)
        pm["action_items"] = action_items
        pm["status"] = "final"
        await self.storage.save(post_mortem_id, pm)
        await self.notifier.send({
            "post_mortem": post_mortem_id,
            "action_items_count": len(action_items),
            "participants": pm["participants"]
        })
```

### On-Call Management

```python
class OnCallManager:
    def __init__(self):
        self.schedule = {}
        self.escalation_policies = {}
        self.rotations = {}
    
    def define_rotation(self, rotation_name: str, members: list, 
                       rotation_days: int = 7):
        self.rotations[rotation_name] = {
            "members": members,
            "rotation_days": rotation_days,
            "current_index": 0
        }
    
    def get_current_on_call(self, rotation_name: str) -> str:
        rotation = self.rotations.get(rotation_name)
        if not rotation:
            raise ValueError(f"Unknown rotation: {rotation_name}")
        return rotation["members"][rotation["current_index"]]
    
    def advance_rotation(self, rotation_name: str):
        rotation = self.rotations[rotation_name]
        rotation["current_index"] = (rotation["current_index"] + 1) % len(rotation["members"])
    
    def set_escalation_policy(self, rotation_name: str, levels: list):
        self.escalation_policies[rotation_name] = levels
    
    async def escalate(self, rotation_name: str, current_incident: str, 
                       timeout_minutes: int):
        policy = self.escalation_policies.get(rotation_name, [])
        for level in policy:
            if time.time() - current_incident["created_at"] > level["timeout"]:
                await self._notify_escalation(current_incident, level["targets"])
```

### Runbook Engine

```python
class RunbookEngine:
    def __init__(self, runbook_registry, command_executor):
        self.registry = runbook_registry
        self.executor = command_executor
    
    async def execute(self, runbook_id: str, context: dict) -> dict:
        runbook = await self.registry.get(runbook_id)
        if not runbook:
            raise RunbookNotFound(runbook_id)
        
        results = []
        for step in runbook["steps"]:
            result = await self._execute_step(step, context)
            results.append(result)
            if not result["success"] and step.get("halt_on_failure", True):
                return {
                    "runbook_id": runbook_id,
                    "status": "failed",
                    "failed_step": step["name"],
                    "results": results
                }
        
        return {"runbook_id": runbook_id, "status": "completed", "results": results}
    
    async def _execute_step(self, step: dict, context: dict) -> dict:
        if step["type"] == "command":
            rc, stdout, stderr = await self.executor.run(step["command"])
            return {"name": step["name"], "success": rc == 0, "output": stdout}
        elif step["type"] == "check":
            result = await self._evaluate_condition(step["condition"], context)
            return {"name": step["name"], "success": result}
        elif step["type"] == "approval":
            await self._request_approval(step["approver"])
            return {"name": step["name"], "success": True}
        return {"name": step["name"], "success": False}
```

### War Room Coordination

```python
class WarRoom:
    def __init__(self, communication_client, jira_client):
        self.comm = communication_client
        self.jira = jira_client
        self.active_war_rooms = {}
    
    async def open(self, incident_id: str, severity: str, 
                   channel_name: str = None) -> str:
        war_room_id = f"war-{incident_id}"
        channel = await self.comm.create_channel(
            name=channel_name or f"incident-{incident_id}",
            is_private=(severity == "P0")
        )
        
        await self.comm.post(channel, {
            "text": f"War room opened for incident {incident_id}",
            "severity": severity,
            "incident_link": f"https://jira.example.com/browse/{incident_id}"
        })
        
        self.active_war_rooms[war_room_id] = {
            "incident_id": incident_id,
            "channel": channel,
            "participants": [],
            "opened_at": datetime.utcnow()
        }
        
        return war_room_id
    
    async def add_participant(self, war_room_id: str, user_id: str):
        room = self.active_war_rooms.get(war_room_id)
        if not room:
            return
        await self.comm.invite(room["channel"], user_id)
        room["participants"].append(user_id)
    
    async def close(self, war_room_id: str, resolution_summary: str):
        room = self.active_war_rooms.get(war_room_id)
        if not room:
            return
        await self.comm.post(room["channel"], {
            "text": f"War room closed. Resolution: {resolution_summary}"
        })
        await self.comm.archive(room["channel"])
        del self.active_war_rooms[war_room_id]
```

---

## 5. Disaster Recovery

### Backup Strategy

```python
class AgentBackupManager:
    """Backup and recovery for agent systems."""
    
    async def create_backup(self, components: List[str]):
        backup_tasks = []
        for component in components:
            if component == "database":
                backup_tasks.append(self._backup_database())
            elif component == "vector_store":
                backup_tasks.append(self._backup_vector_store())
            elif component == "models":
                backup_tasks.append(self._backup_models())
        
        results = await asyncio.gather(*backup_tasks)
        return {"results": results, "timestamp": datetime.utcnow()}
    
    async def _backup_database(self):
        # Database backup logic
        pass
    
    async def _backup_vector_store(self):
        # Vector DB backup
        pass
    
    async def _backup_models(self):
        # Model configuration backup
        pass
```

### Multi-Region Failover

```python
class MultiRegionFailover:
    def __init__(self, regions: list, health_check):
        self.regions = regions
        self.health = health_check
        self.current_region = regions[0]
    
    async def health_check_regions(self):
        results = {}
        for region in self.regions:
            healthy = await self.health.check_region(region)
            results[region] = healthy
        return results
    
    async def failover(self, target_region: str):
        if target_region not in self.regions:
            raise ValueError(f"Unknown region: {target_region}")
        
        self.current_region = target_region
        await self._update_dns(target_region)
        await self._promote_replica(target_region)
        await self._warm_caches(target_region)
        await self._notify_failover(target_region)
    
    async def _update_dns(self, region: str):
        # Update DNS to point to new region
        pass
    
    async def _promote_replica(self, region: str):
        # Promote read replica to primary
        pass
    
    async def _warm_caches(self, region: str):
        # Warm up caches in new region
        pass
    
    async def _notify_failover(self, region: str):
        # Notify stakeholders of failover
        pass
```

### Backup Verification

```python
class BackupVerifier:
    def __init__(self, backup_store):
        self.store = backup_store
    
    async def verify(self, backup_id: str) -> dict:
        meta = await self.store.get_metadata(backup_id)
        checksum = await self.store.get_checksum(backup_id)
        
        data = await self.store.download(backup_id)
        computed = hashlib.sha256(data).hexdigest()
        
        valid = computed == checksum
        return {
            "backup_id": backup_id,
            "valid": valid,
            "size": len(data),
            "created": meta.get("created_at"),
            "checksum_match": valid
        }
    
    async def test_restore(self, backup_id: str) -> dict:
        test_db = await self._create_test_db()
        try:
            await self.store.restore(backup_id, test_db)
            count = await test_db.count_records()
            return {"success": True, "records_restored": count}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await self._destroy_test_db(test_db)
```

### Recovery Time Objectives

```python
class RTOManager:
    def __init__(self):
        self.rto_targets = {
            "database": 300,    # 5 minutes
            "cache": 60,        # 1 minute
            "model_api": 120,   # 2 minutes
            "full_service": 600 # 10 minutes
        }
        self.recovery_ procedures = {}
    
    def register_procedure(self, component: str, procedure: Callable):
        self.recovery_procedures[component] = procedure
    
    async def recover(self, component: str) -> dict:
        start = time.time()
        procedure = self.recovery_procedures.get(component)
        if not procedure:
            return {"status": "no_procedure"}
        
        try:
            await procedure()
            duration = time.time() - start
            rto = self.rto_targets.get(component, 600)
            met = duration <= rto
            
            return {
                "component": component,
                "status": "recovered",
                "duration_seconds": duration,
                "rto_target": rto,
                "rto_met": met
            }
        except Exception as e:
            return {"component": component, "status": "failed", "error": str(e)}
    
    def is_rto_met(self, component: str, actual_duration: float) -> bool:
        target = self.rto_targets.get(component, 600)
        return actual_duration <= target
```

---

## 6. GitOps for Agent Systems

### Automated Deployment

```yaml
# ArgoCD application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: agent-production
spec:
  project: ml-platform
  source:
    repoURL: https://github.com/org/agent-config
    path: prod
    helm:
      valueFiles:
      - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: agent-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Configuration Drift Detection

```python
class ConfigDriftDetector:
    def __init__(self, git_client, k8s_client):
        self.git = git_client
        self.k8s = k8s_client
    
    async def detect_drift(self, app_name: str) -> list:
        git_config = await self.git.get_config(app_name, "main")
        live_config = await self.k8s.get_config(app_name)
        
        drift_items = []
        for key, git_value in git_config.items():
            live_value = live_config.get(key)
            if git_value != live_value:
                drift_items.append({
                    "key": key,
                    "git_value": git_value,
                    "live_value": live_value,
                    "drift": True
                })
        return drift_items
    
    async def remediate_drift(self, app_name: str, dry_run: bool = True):
        drift = await self.detect_drift(app_name)
        if not drift:
            return {"status": "no_drift"}
        
        if dry_run:
            return {"status": "drift_detected", "items": drift}
        
        await self.git.commit_config(app_name, drift)
        return {"status": "remediated", "items": drift}
```

### Progressive Delivery with Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: agent
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: {duration: 1m}
      - setWeight: 20
      - pause: {duration: 2m}
      - setWeight: 50
      - pause: {duration: 5m, decision: "analysis"}
      analysis:
        templates:
        - templateName: success-rate
        args:
        - name: service-name
          value: agent
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      containers:
      - name: agent
        image: agent:latest
```

### Ephemeral Environments

```python
class EphemeralEnvironmentManager:
    def __init__(self, git_client, k8s_client):
        self.git = git_client
        self.k8s = k8s_client
    
    async def create_pr_environment(self, pr_number: int) -> str:
        branch = f"pr-{pr_number}"
        
        await self.git.create_branch(branch, f"refs/pull/{pr_number}/head")
        await self.k8s.create_namespace(branch)
        await self.k8s.deploy(branch, "agent:pr-{pr_number}")
        
        url = f"https://pr-{pr_number}.agent.example.com"
        await self.git.post_comment(pr_number, f"Environment ready: {url}")
        
        return url
    
    async def destroy_pr_environment(self, pr_number: int):
        branch = f"pr-{pr_number}"
        await self.k8s.delete_namespace(branch)
        await self.git.delete_branch(branch)
```

### GitOps Compliance

```python
class GitOpsComplianceChecker:
    def __init__(self, argo_client, policy_engine):
        self.argo = argo_client
        self.policy = policy_engine
    
    async def check_all(self) -> dict:
        apps = await self.argo.list_applications()
        results = []
        for app in apps:
            sync_status = await self.argo.get_sync_status(app["name"])
            health = await self.argo.get_health(app["name"])
            
            policy_violations = await self.policy.evaluate(
                app["name"], 
                sync_status, 
                health
            )
            
            results.append({
                "app": app["name"],
                "sync_status": sync_status["status"],
                "health": health["status"],
                "policy_violations": policy_violations,
                "compliant": len(policy_violations) == 0
            })
        return {"results": results, "compliant_count": sum(1 for r in results if r["compliant"])}
```

---

## 7. Service Mesh Integration

### Istio Configuration

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: agent-service
spec:
  hosts:
  - agent-service
  http:
  - route:
    - destination:
        host: agent-service
        subset: v1
      weight: 100
    retries:
      attempts: 3
      perTryTimeout: 2s
    fault:
      delay:
        percentage:
          value: 0.1
        fixedDelay: 5s
```

### Traffic Management

```python
class ServiceMeshTrafficManager:
    def __init__(self, istio_client):
        self.istio = istio_client
    
    async def configure_timeout(self, service: str, timeout_seconds: int):
        virtual_service = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "VirtualService",
            "metadata": {"name": service},
            "spec": {
                "http": [{
                    "route": [{"destination": {"host": service}}],
                    "timeout": f"{timeout_seconds}s"
                }]
            }
        }
        await self.istio.apply(virtual_service)
    
    async def configure_retry(self, service: str, attempts: int, per_try: str):
        patch = {
            "spec": {
                "http": [{
                    "retries": {
                        "attempts": attempts,
                        "perTryTimeout": per_try,
                        "retryOn": "connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes"
                    }
                }]
            }
        }
        await self.istio.patch_virtual_service(service, patch)
    
    async def configure_fault_injection(self, service: str, delay_percent: float, delay_ms: int):
        patch = {
            "spec": {
                "http": [{
                    "fault": {
                        "delay": {
                            "percentage": {"value": delay_percent},
                            "fixedDelay": f"{delay_ms}ms"
                        }
                    }
                }]
            }
        }
        await self.istio.patch_virtual_service(service, patch)
```

### Mutual TLS

```python
class MeshMTLSManager:
    def __init__(self, istio_client):
        self.istio = istio_client
    
    async def enforce_strict_mtls(self, namespace: str):
        peer_auth = {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "PeerAuthentication",
            "metadata": {"name": "default", "namespace": namespace},
            "spec": {"mtls": {"mode": "STRICT"}}
        }
        await self.istio.apply(peer_auth)
    
    async def configure_destination_rule(self, service: str):
        destination_rule = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "DestinationRule",
            "metadata": {"name": service},
            "spec": {
                "host": service,
                "trafficPolicy": {
                    "tls": {"mode": "ISTIO_MUTUAL"},
                    "loadBalancer": {"simple": "LEAST_CONN"}
                }
            }
        }
        await self.istio.apply(destination_rule)
```

---

## 8. Capacity Planning

### Demand Forecasting

```python
class DemandForecaster:
    def __init__(self, metrics_store):
        self.metrics = metrics_store
    
    async def forecast(self, days_ahead: int = 30) -> dict:
        history = await self.metrics.get_range("request_rate", days=90)
        forecast = self._time_series_forecast(history, days_ahead)
        
        return {
            "current_peak": max(d["value"] for d in history),
            "forecasted_peak": max(forecast),
            "recommended_capacity": math.ceil(max(forecast) * 1.2),
            "confidence_interval": self._confidence_interval(forecast)
        }
    
    def _time_series_forecast(self, history: list, days: int):
        values = [d["value"] for d in history]
        # Exponential smoothing
        alpha = 0.3
        smoothed = [values[0]]
        for v in values[1:]:
            smoothed.append(alpha * v + (1 - alpha) * smoothed[-1])
        
        trend = self._calculate_trend(smoothed)
        forecast = []
        last = smoothed[-1]
        for i in range(days):
            last += trend
            forecast.append(last)
        return forecast
    
    def _calculate_trend(self, series: list) -> float:
        n = len(series)
        if n < 2:
            return 0.0
        x = list(range(n))
        y = series
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
        return numerator / denominator if denominator else 0
```

### Cost Projection

```python
class CostProjector:
    def __init__(self, pricing_client):
        self.pricing = pricing_client
        self.history_days = 90
    
    async def project(self, days_ahead: int = 90) -> dict:
        history = await self._get_cost_history()
        forecast = self._forecast_costs(history, days_ahead)
        
        return {
            "current_monthly": self._sum_month(history),
            "forecasted_monthly": self._sum_month(forecast),
            "projected_total": sum(forecast),
            "cost_drivers": self._top_cost_drivers(history),
            "recommendations": self._generate_recommendations(forecast)
        }
    
    def _forecast_costs(self, history: list, days: int):
        # Use same time series approach as demand forecaster
        pass
    
    def _top_cost_drivers(self, history: list) -> list:
        # Group costs by service
        pass
    
    def _generate_recommendations(self, forecast: list) -> list:
        recommendations = []
        if forecast[-1] > forecast[0] * 1.5:
            recommendations.append({
                "type": "scale_right",
                "description": "Consider right-sizing instances"
            })
        return recommendations
```

---

## 9. Chaos Engineering

### Experiment Design

```python
class ChaosExperiment:
    def __init__(self, name: str, hypothesis: str, blast_radius: str):
        self.name = name
        self.hypothesis = hypothesis
        self.blast_radius = blast_radius
        self.rollback_fn = None
    
    def set_fault(self, fault_type: str, params: dict):
        self.fault_type = fault_type
        self.fault_params = params
    
    def set_rollback(self, rollback_fn: Callable):
        self.rollback_fn = rollback
    
    async def run(self, duration: int) -> dict:
        # Notify start
        logger.info(f"Starting chaos experiment: {self.name}")
        
        try:
            # Inject fault
            await self._inject_fault()
            
            # Observe for duration
            await asyncio.sleep(duration)
            
            # Collect metrics
            metrics = await self._collect_metrics()
            
            return {
                "experiment": self.name,
                "status": "completed",
                "metrics": metrics
            }
        finally:
            if self.rollback_fn:
                await self.rollback_fn()
```

### Fault Injection

```python
class FaultInjector:
    def __init__(self, chaos_client):
        self.client = chaos_client
    
    async def kill_pods(self, label_selector: str, count: int = 1):
        pods = await self.client.list_pods(label_selector)
        targets = pods[:count]
        for pod in targets:
            await self.client.delete_pod(pod["name"])
    
    async def inject_latency(self, service: str, latency_ms: int, 
                            jitter_ms: int = 0):
        await self.client.patch_deployment(
            service,
            {"spec": {"template": {"spec": {
                "containers": [{
                    "name": "istio-proxy",
                    "env": [{
                        "name": "PILOT_PUSH_THROTTLE",
                        "value": str(latency_ms)
                    }]
                }]
            }}}}
        )
    
    async def inject_cpu_stress(self, pod: str, cpu_cores: float):
        await self.client.exec(
            pod,
            ["stress-ng", "-c", str(int(cpu_cores)), "--timeout", "60s"]
        )
```

### Steady State Validation

```python
class SteadyStateValidator:
    def __init__(self, metrics_client, slo_definitions):
        self.metrics = metrics_client
        self.slos = slo_definitions
    
    async def validate(self, experiment_context: dict) -> dict:
        violations = []
        for slo_name, slo_def in self.slos.items():
            # Collect metrics over the experiment window
            metric_values = await self.metrics.get_range(
                slo_def["metric"], 
                start=experiment_context["start_time"],
                end=experiment_context["end_time"]
            )
            
            actual = self._compute_slo(metric_values, slo_def)
            if actual < slo_def["target"]:
                violations.append({
                    "slo": slo_name,
                    "target": slo_def["target"],
                    "actual": actual,
                    "violation_pct": (slo_def["target"] - actual) / slo_def["target"]
                })
        
        return {
            "steady_state": len(violations) == 0,
            "violations": violations
        }
    
    def _compute_slo(self, values: list, slo_def: dict) -> float:
        if slo_def["type"] == "availability":
            return sum(1 for v in values if v["status"] == "success") / len(values)
        elif slo_def["type"] == "latency":
            sorted_values = sorted(v["latency"] for v in values)
            p99_index = int(len(sorted_values) * 0.99)
            return sorted_values[p99_index]
        return 0.0
```

---

## 10. Production Excellence

### SLO Management

```python
class SLOManager:
    def __init__(self):
        self.slos = {
            "availability": {"target": 0.999, "window": "30d"},
            "latency_p99": {"target": 5.0, "window": "7d"},
            "error_budget": {"target": 0.001, "window": "30d"}
        }
    
    def evaluate(self, metrics) -> dict:
        results = {}
        for slo_name, config in self.slos.items():
            actual = self._compute(metrics, slo_name, config["window"])
            results[slo_name] = {
                "target": config["target"],
                "actual": actual,
                "status": "met" if actual >= config["target"] else "violated",
                "remaining_budget": self._remaining_budget(actual, config["target"])
            }
        return results
    
    def _compute(self, metrics, slo_name, window):
        # Compute SLO from time series metrics
        return 0.999
```

### Error Budget Policy

```python
class ErrorBudgetPolicy:
    def __init__(self):
        self.budget_consumption_rate = 0.0
        self.burn_rate_thresholds = {
            "slow_burn": 1.0,
            "fast_burn": 10.0
        }
    
    def burn_rate(self, current_budget: float, time_elapsed: float, 
                  total_window: float) -> float:
        if time_elapsed <= 0:
            return 0.0
        burn_rate = (1.0 - current_budget) / time_elapsed
        return burn_rate / (1.0 / total_window)
    
    def actions(self, burn_rate: float) -> list:
        if burn_rate > self.burn_rate_thresholds["fast_burn"]:
            return [
                "freeze_non_essential_deployments",
                "escalate_to_engineering_manager",
                "dedicate_team_to_reliability"
            ]
        elif burn_rate > self.burn_rate_thresholds["slow_burn"]:
            return [
                "reduce_deployment_frequency",
                "focus_on_tech_debt",
                "increase_monitoring"
            ]
        return []
```

### Production Readiness Review

```python
class ProductionReadinessReview:
    def __init__(self):
        self.criteria = {
            "reliability": self._check_reliability,
            "scalability": self._check_scalability,
            "observability": self._check_observability,
            "security": self._check_security,
            "disaster_recovery": self._check_dr,
            "documentation": self._check_docs
        }
    
    async def evaluate(self, service: str) -> dict:
        results = {}
        for category, check_fn in self.criteria.items():
            results[category] = await check_fn(service)
        
        overall = all(r["passed"] for r in results.values())
        return {
            "service": service,
            "overall": overall,
            "categories": results,
            "score": sum(1 for r in results.values() if r["passed"]) / len(results) * 100
        }
    
    async def _check_reliability(self, service: str) -> dict:
        return {
            "passed": True,
            "checks": ["circuit_breakers", "retries", "timeouts"],
            "gaps": []
        }
    
    async def _check_scalability(self, service: str) -> dict:
        return {"passed": True, "checks": ["hpa", "load_test"], "gaps": []}
    
    async def _check_observability(self, service: str) -> dict:
        return {"passed": True, "checks": ["metrics", "logs", "traces"], "gaps": []}
    
    async def _check_security(self, service: str) -> dict:
        return {"passed": True, "checks": ["auth", "encryption", "rbac"], "gaps": []}
    
    async def _check_dr(self, service: str) -> dict:
        return {"passed": True, "checks": ["backups", "rto_test"], "gaps": []}
    
    async def _check_docs(self, service: str) -> dict:
        return {"passed": True, "checks": ["runbook", "architecture"], "gaps": []}
```

### Capacity Review Cadence

```python
class CapacityReviewCadence:
    def __init__(self):
        self.reviews = {
            "weekly": ["queue_depth", "error_rate", "latency"],
            "monthly": ["cost_trends", "utilization_trends", "growth_forecast"],
            "quarterly": ["architecture_review", "roadmap_alignment", "tech_debt"]
        }
    
    def get_review_schedule(self) -> dict:
        schedule = []
        for cadence, topics in self.reviews.items():
            schedule.append({
                "cadence": cadence,
                "topics": topics,
                "participants": ["engineering_manager", "sre_lead"],
                "output": f"capacity_report_{cadence}"
            })
        return schedule
    
    async def run_weekly_review(self):
        topics = self.reviews["weekly"]
        metrics = {}
        for topic in topics:
            metrics[topic] = await self._gather_metrics(topic)
        
        report = {
            "date": datetime.utcnow().isoformat(),
            "period": "weekly",
            "metrics": metrics,
            "action_items": self._identify_action_items(metrics)
        }
        await self._distribute_report(report)
        return report
```

### Operational Excellence Metrics

```python
class OperationalExcellenceMetrics:
    def __init__(self):
        self.metrics = {}
    
    def measure_deployment_frequency(self) -> dict:
        history = self._get_deployment_history(30)
        return {
            "deployments_last_30d": len(history),
            "avg_per_week": len(history) / 4.3,
            "target": 10,
            "status": "met" if len(history) >= 10 else "below_target"
        }
    
    def measure_change_failure_rate(self) -> dict:
        history = self._get_deployment_history(30)
        failures = [d for d in history if d["result"] == "rollback"]
        rate = len(failures) / len(history) if history else 0
        return {
            "change_failure_rate": rate,
            "target": 0.15,
            "status": "met" if rate <= 0.15 else "violated"
        }
    
    def measure_mttr(self) -> dict:
        incidents = self._get_incidents(30)
        if not incidents:
            return {"mttr_minutes": 0, "target": 15, "status": "no_data"}
        
        resolutions = [i["resolved_at"] - i["created_at"] for i in incidents]
        mttr_seconds = sum(resolutions) / len(resolutions)
        mttr_minutes = mttr_seconds / 60
        
        return {
            "mttr_minutes": mttr_minutes,
            "target": 15,
            "status": "met" if mttr_minutes <= 15 else "violated"
        }
    
    def generate_report(self) -> dict:
        return {
            "deployment_frequency": self.measure_deployment_frequency(),
            "change_failure_rate": self.measure_change_failure_rate(),
            "mttr": self.measure_mttr(),
            "overall_rating": self._calc_rating()
        }
    
    def _calc_rating(self) -> str:
        # Elite: Deploy on demand, <15% failure, <1hr MTTR
        # High: Between weekly and monthly, 0-15% failure, <1hr MTTR
        # Medium: Between weekly and monthly, 0-15% failure, 1-24hr MTTR
        pass
```

### Release Orchestration

```python
class ReleaseOrchestrator:
    def __init__(self):
        self.releases = {}
        self.pipeline_stages = [
            "lint", "test", "security_scan", "build", "deploy_staging", 
            "integration_test", "deploy_production"
        ]
    
    async def create_release(self, version: str, description: str, 
                            components: list) -> str:
        release_id = f"rel-{version}"
        self.releases[release_id] = {
            "id": release_id,
            "version": version,
            "description": description,
            "components": components,
            "status": "created",
            "created_at": datetime.utcnow().isoformat(),
            "stages": {}
        }
        return release_id
    
    async def execute_pipeline(self, release_id: str, 
                               parallel: bool = False) -> dict:
        release = self.releases[release_id]
        
        if parallel:
            await self._run_parallel(release)
        else:
            await self._run_sequential(release)
        
        # Promote if all stages passed
        return release
    
    async def _run_sequential(self, release: dict):
        for stage in self.pipeline_stages:
            result = await self._run_stage(stage, release)
            release["stages"][stage] = result
            if not result["success"]:
                release["status"] = "failed"
                await self._notify_stage_failure(release, stage)
                return
    
    async def promote(self, release_id: str, target: str):
        release = self.releases[release_id]
        if release["status"] != "ready_for_promotion":
            raise ReleaseNotReady(release_id)
        
        await self._deploy(release["components"], target)
        release["status"] = "promoted"
        release["promoted_at"] = datetime.utcnow().isoformat()
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)