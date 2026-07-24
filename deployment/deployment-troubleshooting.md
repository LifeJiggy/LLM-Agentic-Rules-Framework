# Deployment Troubleshooting for LLM & Agentic Systems

## Table of Contents

1. [Overview](#overview)
2. [Deployment Failures](#deployment-failures)
   - [Image Pull Errors](#image-pull-errors)
   - [Resource Constraints](#resource-constraints)
   - [Configuration Errors](#configuration-errors)
3. [Rollback Issues](#rollback-issues)
   - [Rollback Failures](#rollback-failures)
   - [State Management](#state-management)
4. [Configuration Problems](#configuration-problems)
   - [Environment Variable Issues](#environment-variable-issues)
   - [Secret Management Issues](#secret-management-issues)
5. [Service Discovery](#service-discovery)
   - [DNS Issues](#dns-issues)
   - [Load Balancer Issues](#load-balancer-issues)
6. [Health Check Failures](#health-check-failures)
   - [Liveness Probe Failures](#liveness-probe-failures)
   - [Readiness Probe Failures](#readiness-probe-failures)
7. [Performance Issues](#performance-issues)
   - [Memory Issues](#memory-issues)
   - [CPU Issues](#cpu-issues)
   - [GPU Issues](#gpu-issues)
8. [Network Issues](#network-issues)
   - [Connectivity Problems](#connectivity-problems)
   - [Port Conflicts](#port-conflicts)
9. [Debugging Tools](#debugging-tools)
10. [Summary](#summary)

---

## Overview

Troubleshooting deployment issues is a critical skill for maintaining reliable AI/LLM systems. This document covers common issues, their symptoms, root causes, and solutions.

### Troubleshooting Approach

```
1. Identify the symptom
2. Gather relevant logs and metrics
3. Analyze the root cause
4. Apply the fix
5. Verify the fix works
6. Document the issue and solution
```

---

## Deployment Failures

### Image Pull Errors

#### Symptoms

```
Error: ImagePullBackOff
Warning: Failed to pull image "llm-api:1.3.0": rpc error: code = Unknown desc = failed to pull and unpack image: failed to resolve reference "llm-api:1.3.0": pulling from host registry-1.docker.io failed with status 404: NOT_FOUND
```

#### Root Causes

1. Image tag doesn't exist in the registry
2. Registry authentication failed
3. Network connectivity issues
4. Registry is down

#### Solutions

```yaml
# Fix 1: Verify image tag exists
kubectl describe pod <pod-name> -n production
# Look for Events section

# Fix 2: Check image pull secrets
kubectl get secrets -n production
kubectl get serviceaccount default -n production -o yaml

# Fix 3: Test registry connectivity
kubectl run test-pod --rm -it --image=busybox -- wget -qO- https://registry-1.docker.io/v2/

# Fix 4: Create image pull secret
kubectl create secret docker-registry registry-credentials \
    --docker-server=ghcr.io \
    --docker-username=<username> \
    --docker-password=<token> \
    --namespace=production
```

```yaml
# Fix 5: Use correct image reference
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          image: ghcr.io/myorg/llm-api:1.3.0  # Use full path
      imagePullSecrets:
        - name: registry-credentials
```

### Resource Constraints

#### Symptoms

```
Warning: FailedScheduling: 0/3 nodes are available: 3 Insufficient cpu.
Warning: FailedScheduling: 0/3 nodes are available: 3 Insufficient memory.
Warning: FailedScheduling: 0/3 nodes are available: 3 Insufficient nvidia.com/gpu.
```

#### Root Causes

1. Cluster doesn't have enough resources
2. Resource requests are too high
3. Node selectors are too restrictive
4. Taints and tolerations don't match

#### Solutions

```yaml
# Fix 1: Check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Fix 2: Reduce resource requests
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          resources:
            requests:
              memory: "2Gi"  # Reduced from 4Gi
              cpu: "1"       # Reduced from 2
              nvidia.com/gpu: "0"  # No GPU required
            limits:
              memory: "4Gi"
              cpu: "2"
              nvidia.com/gpu: "1"

# Fix 3: Use node affinity instead of node selectors
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 1
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - gpu
```

### Configuration Errors

#### Symptoms

```
Error: container has restarted 3 times
Warning: BackOff: Back-off restarting failed container
Error: Liveness probe failed: HTTP probe failed with statuscode: 500
```

#### Root Causes

1. Missing environment variables
2. Incorrect configuration values
3. Invalid YAML syntax
4. Secret not found

#### Solutions

```yaml
# Fix 1: Check pod logs
kubectl logs <pod-name> -n production --previous

# Fix 2: Describe pod for events
kubectl describe pod <pod-name> -n production

# Fix 3: Validate configuration
kubectl get configmap llm-api-config -n production -o yaml

# Fix 4: Check secrets exist
kubectl get secret llm-api-secrets -n production

# Fix 5: Validate YAML syntax
kubectl apply -f deployment.yaml --dry-run=client
```

---

## Rollback Issues

### Rollback Failures

#### Symptoms

```
error: unable to rollback deployment "llm-api": deployment has already been rolled out
error: unable to find replica set for deployment "llm-api" with rollback-to revision 5
```

#### Root Causes

1. Revision doesn't exist
2. Deployment is already at the requested revision
3. ReplicaSet was garbage collected
4. Rollback command is incorrect

#### Solutions

```bash
# Fix 1: Check deployment history
kubectl rollout history deployment/llm-api -n production

# Fix 2: Check specific revision
kubectl rollout history deployment/llm-api -n production --revision=5

# Fix 3: Rollback to previous revision
kubectl rollout undo deployment/llm-api -n production

# Fix 4: Rollback to specific revision
kubectl rollout undo deployment/llm-api -n production --to-revision=5

# Fix 5: Monitor rollback progress
kubectl rollout status deployment/llm-api -n production --timeout=300s
```

### State Management

#### Symptoms

```
Warning: Unhealthy: Readiness probe failed: connection refused
Warning: Unhealthy: Liveness probe failed: timeout
Error: Pod stuck in Terminating state
```

#### Root Causes

1. StatefulSets have complex rollback behavior
2. Persistent volumes are stuck
3. Finalizers are blocking deletion
4. Node is unreachable

#### Solutions

```yaml
# Fix 1: Check StatefulSet status
kubectl get statefulset llm-api -n production
kubectl describe statefulset llm-api -n production

# Fix 2: Check PVC status
kubectl get pvc -n production
kubectl describe pvc <pvc-name> -n production

# Fix 3: Force delete stuck pods
kubectl delete pod <pod-name> -n production --grace-period=0 --force

# Fix 4: Remove finalizers if stuck
kubectl patch pvc <pvc-name> -n production -p '{"metadata":{"finalizers":null}}'
```

---

## Configuration Problems

### Environment Variable Issues

#### Symptoms

```
Error: KeyError: 'DATABASE_URL'
Error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: password authentication failed
Warning: Environment variable not set: REDIS_URL
```

#### Root Causes

1. Environment variable not set
2. Environment variable has wrong value
3. ConfigMap doesn't exist
4. Secret doesn't exist

#### Solutions

```yaml
# Fix 1: Check environment variables in pod
kubectl exec -it <pod-name> -n production -- env | grep DATABASE

# Fix 2: Check ConfigMap
kubectl get configmap llm-api-config -n production -o yaml

# Fix 3: Check Secret
kubectl get secret llm-api-secrets -n production -o yaml

# Fix 4: Verify environment variable injection
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          envFrom:
            - configMapRef:
                name: llm-api-config
            - secretRef:
                name: llm-api-secrets
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: llm-api-secrets
                  key: database-url
```

### Secret Management Issues

#### Symptoms

```
Error: secret "llm-api-secrets" not found
Error: secret "llm-api-secrets" has no key "api-key"
Warning: Using default token as credentials
```

#### Root Causes

1. Secret doesn't exist in the namespace
2. Secret key doesn't exist
3. Secret is not properly base64 encoded
4. Secret is not mounted correctly

#### Solutions

```bash
# Fix 1: Create secret
kubectl create secret generic llm-api-secrets \
    --namespace=production \
    --from-literal=database-url='postgresql://admin:secret@postgres:5432/llm_api' \
    --from-literal=redis-url='redis://redis:6379' \
    --from-literal=api-key='sk-1234567890abcdef'

# Fix 2: Verify secret exists
kubectl get secret llm-api-secrets -n production

# Fix 3: Check secret keys
kubectl get secret llm-api-secrets -n production -o jsonpath='{.data}' | jq

# Fix 4: Update secret
kubectl create secret generic llm-api-secrets \
    --namespace=production \
    --from-literal=database-url='postgresql://admin:secret@postgres:5432/llm_api' \
    --dry-run=client -o yaml | kubectl apply -f -
```

---

## Service Discovery

### DNS Issues

#### Symptoms

```
Error: curl: (6) Could not resolve host: postgres
Error: Name or service not known
Warning: DNS lookup failed for postgres.default.svc.cluster.local
```

#### Root Causes

1. Service doesn't exist
2. Service is in a different namespace
3. DNS is not working
4. Network policy is blocking DNS

#### Solutions

```bash
# Fix 1: Check service exists
kubectl get svc -n production

# Fix 2: Test DNS resolution
kubectl run dns-test --rm -it --image=busybox -- nslookup postgres

# Fix 3: Check DNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Fix 4: Test connectivity
kubectl run connectivity-test --rm -it --image=busybox -- wget -qO- http://postgres:5432

# Fix 5: Use fully qualified domain name
kubectl run connectivity-test --rm -it --image=busybox -- wget -qO- http://postgres.production.svc.cluster.local:5432
```

### Load Balancer Issues

#### Symptoms

```
Warning: Service has no endpoints
Warning: LoadBalancer has no external IP
Error: Connection refused
```

#### Root Causes

1. No pods matching service selector
2. Service port is wrong
3. Load balancer is not provisioned
4. Health checks are failing

#### Solutions

```bash
# Fix 1: Check service endpoints
kubectl get endpoints llm-api -n production

# Fix 2: Check pod labels
kubectl get pods -l app=llm-api -n production

# Fix 3: Check service selector
kubectl get svc llm-api -n production -o yaml

# Fix 4: Verify pod health
kubectl get pods -l app=llm-api -n production -o wide

# Fix 5: Check load balancer status
kubectl get svc llm-api -n production -o jsonpath='{.status.loadBalancer}'
```

---

## Health Check Failures

### Liveness Probe Failures

#### Symptoms

```
Warning: Unhealthy: Liveness probe failed: HTTP probe failed with statuscode: 503
Warning: Unhealthy: Liveness probe failed: Get "http://localhost:8080/health/live": dial tcp 127.0.0.1:8080: connect: connection refused
Error: Container llm-api failed liveness probe 3 times
```

#### Root Causes

1. Application is not responding
2. Health endpoint is broken
3. Application is taking too long to start
4. Application is consuming too much memory

#### Solutions

```bash
# Fix 1: Check pod logs
kubectl logs <pod-name> -n production --previous

# Fix 2: Test health endpoint manually
kubectl exec -it <pod-name> -n production -- curl http://localhost:8080/health/live

# Fix 3: Increase initial delay
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 120  # Increased from 60
            periodSeconds: 15
            timeoutSeconds: 10
            failureThreshold: 5  # Increased from 3

# Fix 4: Add startup probe
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          startupProbe:
            httpGet:
              path: /health/startup
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 60  # 5 minutes to start
```

### Readiness Probe Failures

#### Symptoms

```
Warning: Unhealthy: Readiness probe failed: HTTP probe failed with statuscode: 503
Warning: Endpoints are not ready for service llm-api
Error: No endpoints available for service llm-api
```

#### Root Causes

1. Application is not ready to serve traffic
2. Dependencies are not available
3. Health check is too strict
4. Application is overloaded

#### Solutions

```bash
# Fix 1: Check readiness endpoint
kubectl exec -it <pod-name> -n production -- curl http://localhost:8080/health/ready

# Fix 2: Check dependencies
kubectl exec -it <pod-name> -n production -- curl http://localhost:8080/health/ready -v

# Fix 3: Make readiness check less strict
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 5  # Increased from 3

# Fix 4: Increase pod resources
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          resources:
            requests:
              memory: "8Gi"  # Increased from 4Gi
              cpu: "4"       # Increased from 2
            limits:
              memory: "16Gi"
              cpu: "8"
```

---

## Performance Issues

### Memory Issues

#### Symptoms

```
Warning: OOMKilled: Container llm-api exceeded memory limit
Error: Container killed: memory cgroup out of memory
Warning: Memory pressure on node
```

#### Root Causes

1. Memory limit too low
2. Memory leak in application
3. Model loading requires more memory
4. Too many concurrent requests

#### Solutions

```yaml
# Fix 1: Increase memory limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          resources:
            requests:
              memory: "8Gi"
              cpu: "4"
            limits:
              memory: "16Gi"
              cpu: "8"

# Fix 2: Add memory monitoring
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: llm-api
spec:
  selector:
    matchLabels:
      app: llm-api
  endpoints:
    - port: metrics
      interval: 30s

# Fix 3: Use horizontal pod autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
```

### CPU Issues

#### Symptoms

```
Warning: CPUThrottlingHigh: Throttling of container llm-api is high
Warning: Container is using more CPU than requested
Error: Pods are pending due to insufficient CPU
```

#### Root Causes

1. CPU limit too low
2. Application is CPU-bound
3. Insufficient CPU on node
4. Inefficient code

#### Solutions

```yaml
# Fix 1: Increase CPU limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          resources:
            requests:
              memory: "8Gi"
              cpu: "4"
            limits:
              memory: "16Gi"
              cpu: "8"

# Fix 2: Use node affinity for CPU-optimized nodes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node-type
                    operator: In
                    values:
                      - compute-optimized

# Fix 3: Profile application
kubectl exec -it <pod-name> -n production -- python -m cProfile -s cumtime src/main.py
```

### GPU Issues

#### Symptoms

```
Warning: Insufficient nvidia.com/gpu
Error: CUDA error: out of memory
Warning: GPU utilization is low
```

#### Root Causes

1. GPU not available on node
2. GPU memory exhausted
3. GPU drivers not installed
4. Application not using GPU efficiently

#### Solutions

```bash
# Fix 1: Check GPU availability
kubectl get nodes -o json | jq '.items[].status.capacity."nvidia.com/gpu"'

# Fix 2: Check GPU utilization
kubectl exec -it <pod-name> -n production -- nvidia-smi

# Fix 3: Use GPU operator
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/gpu-operator/v23.9.1/deploy/gpu-operator-crds.yaml
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/gpu-operator/v23.9.1/deploy/gpu-operator-values.yaml

# Fix 4: Optimize GPU usage
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          resources:
            requests:
              nvidia.com/gpu: "1"
            limits:
              nvidia.com/gpu: "1"
          env:
            - name: CUDA_VISIBLE_DEVICES
              value: "0"
            - name: PYTORCH_CUDA_ALLOC_CONF
              value: "max_split_size_mb:512"
```

---

## Network Issues

### Connectivity Problems

#### Symptoms

```
Error: Connection refused
Error: dial tcp: lookup postgres: no such host
Error: context deadline exceeded
```

#### Root Causes

1. Service is down
2. Network policy blocking traffic
3. DNS resolution failure
4. Firewall rules

#### Solutions

```bash
# Fix 1: Test connectivity
kubectl run network-test --rm -it --image=busybox -- wget -qO- http://postgres:5432

# Fix 2: Check network policies
kubectl get networkpolicy -n production

# Fix 3: Check service endpoints
kubectl get endpoints postgres -n production

# Fix 4: Check DNS
kubectl run dns-test --rm -it --image=busybox -- nslookup postgres

# Fix 5: Check pod-to-pod connectivity
kubectl exec -it <pod-name> -n production -- ping <other-pod-ip>
```

### Port Conflicts

#### Symptoms

```
Error: bind: address already in use
Error: listen tcp: 0.0.0.0:8080: bind: address already in use
Warning: Multiple containers using same port
```

#### Root Causes

1. Port already in use by another container
2. Port already in use by host process
3. Multiple pods using same port
4. Service port conflict

#### Solutions

```yaml
# Fix 1: Use different ports
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      containers:
        - name: llm-api
          ports:
            - containerPort: 8081  # Changed from 8080
              name: http
        - name: sidecar
          ports:
            - containerPort: 8082
              name: sidecar

# Fix 2: Use host networking carefully
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  template:
    spec:
      hostNetwork: true
      containers:
        - name: llm-api
          ports:
            - containerPort: 8080
              hostPort: 8080  # Only use if necessary
```

---

## Debugging Tools

```yaml
# debugging-tools.yaml
apiVersion: v1
kind: Pod
metadata:
  name: debug-pod
  namespace: production
spec:
  containers:
    - name: debug
      image: busybox
      command: ["sleep", "3600"]
      resources:
        requests:
          memory: "64Mi"
          cpu: "50m"
        limits:
          memory: "128Mi"
          cpu: "100m"
  tolerations:
    - operator: Exists
```

```bash
# Useful debugging commands

# Check pod status
kubectl get pods -n production -o wide

# Check pod logs
kubectl logs <pod-name> -n production --previous

# Exec into pod
kubectl exec -it <pod-name> -n production -- /bin/sh

# Check events
kubectl get events -n production --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n production

# Check node resources
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check network policies
kubectl get networkpolicy -n production

# Check service endpoints
kubectl get endpoints -n production

# Check ingress
kubectl get ingress -n production

# Check certificates
kubectl get certificates -n production
```

---

## Summary

Deployment troubleshooting requires a systematic approach to identify and resolve issues. Key takeaways:

1. **Start with logs**: Always check pod logs first
2. **Check events**: Kubernetes events provide valuable insights
3. **Verify configuration**: Ensure ConfigMaps and Secrets exist and are correct
4. **Test connectivity**: Verify network connectivity between services
5. **Monitor resources**: Check CPU, memory, and GPU usage
6. **Use debugging tools**: Leverage kubectl commands and debugging pods
7. **Document solutions**: Record issues and solutions for future reference

By following these troubleshooting steps, teams can quickly resolve deployment issues and maintain reliable AI/LLM systems.
