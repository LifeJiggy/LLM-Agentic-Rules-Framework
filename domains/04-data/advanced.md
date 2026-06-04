# Data Domain - Advanced Concepts

## Overview

This document covers advanced data concepts for LLM/agentic systems, including sophisticated data architectures, retrieval strategies, privacy-preserving techniques, and production-grade data pipeline design. All concepts are presented with implementation patterns, security considerations, and operational guidance.

---

## Table of Contents

1. [Advanced Retrieval Patterns](#1-advanced-retrieval-patterns)
2. [Data Partitioning Strategies](#2-data-partitioning-strategies)
3. [Privacy-Preserving Data Handling](#3-privacy-preserving-data-handling)
4. [Data Versioning and Lineage](#4-data-versioning-and-lineage)
5. [Streaming Data Processing](#5-streaming-data-processing)
6. [Vector Database Patterns](#6-vector-database-patterns)
7. [Data Quality Assurance](#7-data-quality-assurance)
8. [Cross-Region Data Replication](#8-cross-region-data-replication)
9. [Data Governance Automation](#9-data-governance-automation)
10. [Event Sourcing for Agents](#10-event-sourcing-for-agents)

---

## 1. Advanced Retrieval Patterns

### 1.1 Hybrid Search

```python
import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class SearchResult:
    id: str
    content: str
    score: float
    source: str
    metadata: Dict[str, Any]

class HybridSearcher:
    """Combined keyword and semantic search for optimal retrieval."""
    
    def __init__(self, vector_db, keyword_db, weights=None):
        self.vector_db = vector_db
        self.keyword_db = keyword_db
        self.weights = weights or {"semantic": 0.7, "keyword": 0.3}
    
    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        semantic_results = self.vector_db.search(query, top_k=top_k * 2)
        keyword_results = self.keyword_db.search(query, top_k=top_k * 2)
        
        combined = self._combine_results(semantic_results, keyword_results)
        return sorted(combined, key=lambda x: x.score, reverse=True)[:top_k]
    
    def _combine_results(self, semantic: List[SearchResult], 
                         keyword: List[SearchResult]) -> List[SearchResult]:
        scores = {}
        
        for result in semantic:
            scores[result.id] = {"semantic": result.score, "keyword": 0.0}
        
        for result in keyword:
            if result.id in scores:
                scores[result.id]["keyword"] = result.score
            else:
                scores[result.id] = {"semantic": 0.0, "keyword": result.score}
        
        combined = []
        for doc_id, score_data in scores.items():
            final_score = (
                score_data["semantic"] * self.weights["semantic"] +
                score_data["keyword"] * self.weights["keyword"]
            )
            combined.append(SearchResult(
                id=doc_id,
                content=self._get_content(doc_id),
                score=final_score,
                source="hybrid",
                metadata=self._get_metadata(doc_id)
            ))
        
        return combined
    
    def _get_content(self, doc_id: str) -> str:
        return self.vector_db.get(doc_id) or self.keyword_db.get(doc_id) or ""
    
    def _get_metadata(self, doc_id: str) -> Dict:
        return self.vector_db.get_metadata(doc_id) or {}

class QueryUnderstandingAgent:
    """LLM-powered query rewriting for better retrieval."""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def expand_query(self, query: str) -> List[str]:
        prompt = f"""
        Original query: {query}
        
        Generate 3-5 alternative phrasings that might match different document styles.
        Consider synonyms, related concepts, and different formulations.
        
        Return as JSON array of strings.
        """
        response = await self.llm.complete_json(prompt)
        return response if isinstance(response, list) else [query]
    
    async def decompose_query(self, query: str) -> List[str]:
        prompt = f"""
        Complex query: {query}
        
        Break this into sub-questions that can be answered independently.
        
        Return as JSON array of strings.
        """
        response = await self.llm.complete_json(prompt)
        return response if isinstance(response, list) else [query]
```

### 1.2 Re-Ranking and Cross-Attention

```python
class CrossAttentionReranker:
    """Re-rank search results using cross-attention between query and documents."""
    
    def __init__(self, model_client, max_cross_attention: int = 50):
        self.model = model_client
        self.max_cross_attention = max_cross_attention
    
    async def rerank(self, query: str, results: List[SearchResult]) -> List[SearchResult]:
        reranked = []
        for result in results[:self.max_cross_attention]:
            score = await self._compute_cross_attention_score(query, result.content)
            result.score = score
            reranked.append(result)
        return sorted(reranked, key=lambda x: x.score, reverse=True)
    
    async def _compute_cross_attention_score(self, query: str, document: str) -> float:
        prompt = f"""
        Query: {query}
        Document: {document[:2000]}
        
        Rate the relevance of this document to the query on a scale of 0-10.
        Consider:
        - Direct answer coverage
        - Contextual relevance
        - Specific information quality
        
        Return only the number.
        """
        response = await self.model.complete(prompt)
        try:
            return float(response.strip()) / 10.0
        except ValueError:
            return 0.5

class DiversityPromotionReranker:
    """Ensure search results cover diverse sources and perspectives."""
    
    def rerank(self, results: List[SearchResult], min_diversity: float = 0.3) -> List[SearchResult]:
        if not results:
            return results
        
        diversified = []
        sources_seen = set()
        
        high_quality = [r for r in results if r.score > 0.5]
        low_quality = [r for r in results if r.score <= 0.5]
        
        for result in high_quality:
            if len(diversified) / len(results) < min_diversity or result.source not in sources_seen:
                diversified.append(result)
                sources_seen.add(result.source)
        
        diversified.extend(low_quality[:len(results) - len(diversified)])
        return diversified
```

---

## 2. Data Partitioning Strategies

### 2.1 Intelligent Data Sharding

```python
import hashlib
from typing import List, Dict, Optional
import asyncio

class DataShardManager:
    """Production-ready sharding with rebalancing and failover."""
    
    def __init__(self, shards: int = 16, replication_factor: int = 3):
        self.num_shards = shards
        self.replication_factor = replication_factor
        self.shard_health: Dict[int, bool] = {i: True for i in range(shards)}
        self.shard_sizes: Dict[int, int] = {i: 0 for i in range(shards)}
    
    def get_shards(self, key: str) -> List[int]:
        """Get primary and replica shard IDs for a key."""
        primary = self._hash_key(key) % self.num_shards
        replicas = [
            (primary + i * (self.num_shards // self.replication_factor)) % self.num_shards
            for i in range(1, self.replication_factor)
        ]
        return [primary] + replicas
    
    def get_healthy_shard(self, key: str) -> int:
        """Get first healthy shard for a key."""
        shards = self.get_shards(key)
        for shard_id in shards:
            if self.shard_health.get(shard_id, False):
                return shard_id
        raise RuntimeError("No healthy shards available")
    
    def _hash_key(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def mark_unhealthy(self, shard_id: int):
        self.shard_health[shard_id] = False
    
    def mark_healthy(self, shard_id: int):
        self.shard_health[shard_id] = True

class TimeSeriesShardStrategy:
    """Time-based partitioning for temporal data."""
    
    def __init__(self, partition_granularity: str = "day"):
        self.granularity = partition_granularity
    
    def get_partition(self, timestamp: float) -> str:
        """Get partition name for timestamp."""
        if self.granularity == "hour":
            return f"partition_{int(timestamp // 3600)}"
        elif self.granularity == "day":
            return f"partition_{int(timestamp // 86400)}"
        elif self.granularity == "month":
            days = int(timestamp // 86400)
            return f"partition_{days // 30}"
        return "default_partition"
```

### 2.2 Consistent Hashing

```python
import bisect
import hashlib

class ConsistentHashRing:
    """Consistent hashing for dynamic cluster membership."""
    
    def __init__(self, nodes: List[str] = None, replicas: int = 100):
        self.replicas = replicas
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
        self.nodes: Set[str] = set()
        
        if nodes:
            for node in nodes:
                self.add_node(node)
    
    def add_node(self, node: str):
        """Add node to hash ring."""
        self.nodes.add(node)
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            bisect.insort(self.sorted_keys, key)
    
    def remove_node(self, node: str):
        """Remove node from hash ring."""
        self.nodes.discard(node)
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            del self.ring[key]
            index = bisect.bisect_left(self.sorted_keys, key)
            if index < len(self.sorted_keys) and self.sorted_keys[index] == key:
                self.sorted_keys.pop(index)
    
    def get_node(self, key: str) -> Optional[str]:
        """Get node responsible for key."""
        if not self.ring:
            return None
        
        hash_key = self._hash(key)
        index = bisect.bisect_right(self.sorted_keys, hash_key)
        
        if index == len(self.sorted_keys):
            index = 0
        
        return self.ring.get(self.sorted_keys[index])
    
    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

---

## 3. Privacy-Preserving Data Handling

### 3.1 Differential Privacy

```python
import numpy as np
from typing import List, Any

class DifferentialPrivacyEngine:
    """Apply differential privacy to query results."""
    
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta
    
    def add_noise(self, value: float, sensitivity: float = 1.0) -> float:
        """Add Laplace noise for differential privacy."""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return value + noise
    
    def private_count(self, items: List[Any], predicate) -> int:
        """Privately count items matching predicate."""
        true_count = sum(1 for item in items if predicate(item))
        return int(max(0, self.add_noise(true_count)))
    
    def private_histogram(self, values: List[Any], bins: int = 10) -> List[Tuple[float, int]]:
        """Generate differentially private histogram."""
        hist, bin_edges = np.histogram(values, bins=bins)
        private_counts = [
            max(0, self.add_noise(count)) for count in hist
        ]
        return list(zip(bin_edges, private_counts))

class QuerySanitizer:
    """Sanitize query results to prevent leakage."""
    
    def __init__(self, pii_detector, sensitivity_levels: Dict[str, float]):
        self.pii_detector = pii_detector
        self.sensitivity = sensitivity_levels
    
    def sanitize_result(self, result: Any, context: Dict) -> Any:
        """Remove or redact sensitive information."""
        if isinstance(result, dict):
            return {k: self.sanitize_result(v, context) for k, v in result.items()}
        elif isinstance(result, list):
            return [self.sanitize_result(item, context) for item in result]
        elif isinstance(result, str):
            return self._sanitize_text(result)
        return result
    
    def _sanitize_text(self, text: str) -> str:
        """Redact PII from text."""
        pii_found = self.pii_detector.detect(text)
        sanitized = text
        for pii in pii_found:
            sanitized = sanitized.replace(pii.value, "[REDACTED]")
        return sanitized
```

### 3.2 Secure Multi-Party Computation

```python
class MPCDataProcessor:
    """Secure multi-party computation for collaborative analytics."""
    
    async def compute_private_aggregate(self, data_shares: List[Dict], 
                                       operation: str) -> float:
        """Compute aggregate without revealing individual values."""
        if operation == "sum":
            shares = [share["value"] for share in data_shares]
            total = sum(shares)
            return self._add_secure_noise(total)
        elif operation == "average":
            total = await self.compute_private_aggregate(data_shares, "sum")
            count = len(data_shares)
            return total / count
        raise ValueError(f"Unsupported operation: {operation}")
    
    def _add_secure_noise(self, value: float) -> float:
        """Add cryptographically secure noise."""
        # In production, use proper MPC libraries
        noise = np.random.normal(0, 0.01 * abs(value))
        return value + noise
```

---

## 4. Data Versioning and Lineage

### 4.1 Data Version Control

```python
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

@dataclass
class DataVersion:
    version_id: str
    data_hash: str
    created_at: datetime
    parent_version: Optional[str]
    metadata: Dict[str, Any]
    transformations: List[str]

class DataRegistry:
    """Track data versions and lineage for reproducibility."""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.versions: Dict[str, DataVersion] = {}
    
    def register_dataset(self, name: str, data: Any, 
                       metadata: Dict = None) -> DataVersion:
        """Register new data version."""
        data_hash = self._compute_hash(data)
        version_id = self._generate_version_id(name, data_hash)
        
        version = DataVersion(
            version_id=version_id,
            data_hash=data_hash,
            created_at=datetime.utcnow(),
            parent_version=None,
            metadata=metadata or {},
            transformations=self.versions.get(metadata.get("parent")).transformations if metadata.get("parent") else []
        )
        
        self.versions[version_id] = version
        self.storage.save(name, version_id, data)
        return version
    
    def transform(self, dataset_name: str, version_id: str, 
                 transform_fn: callable, transform_name: str) -> DataVersion:
        """Apply transformation and create new version."""
        parent_version = self.versions[version_id]
        data = self.storage.load(dataset_name, version_id)
        transformed_data = transform_fn(data)
        
        new_version = self.register_dataset(
            dataset_name,
            transformed_data,
            metadata={"parent": version_id, "transform": transform_name}
        )
        new_version.transformations = parent_version.transformations + [transform_name]
        
        return new_version
    
    def _compute_hash(self, data: Any) -> str:
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()
    
    def _generate_version_id(self, name: str, data_hash: str) -> str:
        timestamp = datetime.utcnow().isoformat()
        return f"{name}_{data_hash[:8]}_{timestamp.replace(':', '-')}"
```

### 4.2 Data Lineage Tracking

```python
class LineageTracker:
    """Track data flow through transformations."""
    
    def __init__(self):
        self.lineage_graph: Dict[str, List[str]] = {}
        self.operations: Dict[str, Dict] = {}
    
    def record_operation(self, operation_id: str, inputs: List[str], 
                        outputs: List[str], metadata: Dict):
        """Record a data operation in lineage graph."""
        self.operations[operation_id] = {
            "inputs": inputs,
            "outputs": outputs,
            "metadata": metadata,
            "timestamp": datetime.utcnow()
        }
        
        for input_id in inputs:
            if input_id not in self.lineage_graph:
                self.lineage_graph[input_id] = []
            self.lineage_graph[input_id].extend(outputs)
    
    def get_lineage(self, data_id: str) -> List[str]:
        """Get upstream lineage for data item."""
        visited = set()
        path = []
        
        def traverse(node):
            if node in visited:
                return
            visited.add(node)
            if node in self.lineage_graph:
                for parent in self.lineage_graph[node]:
                    traverse(parent)
            path.append(node)
        
        traverse(data_id)
        return path
    
    def get_downstream(self, data_id: str) -> List[str]:
        """Get downstream consumers of data item."""
        downstream = []
        
        for op_id, op_data in self.operations.items():
            if data_id in op_data["inputs"]:
                downstream.extend(op_data["outputs"])
        
        return downstream
```

---

## 5. Streaming Data Processing

### 5.1 Event-Driven Data Pipeline

```python
import asyncio
from typing import AsyncGenerator, Callable
from dataclasses import dataclass

@dataclass
class DataEvent:
    event_type: str
    payload: Any
    timestamp: float
    source: str
    metadata: Dict

class StreamProcessor:
    """Process streaming data for real-time agent updates."""
    
    def __init__(self, buffer_size: int = 1000):
        self.buffer_size = buffer_size
        self.buffer: List[DataEvent] = []
        self.processors: List[Callable] = []
        self.subscribers: List[Callable] = []
        self._buffer_lock = asyncio.Lock()
    
    async def ingest(self, event: DataEvent):
        """Add event to processing buffer."""
        async with self._buffer_lock:
            self.buffer.append(event)
            if len(self.buffer) >= self.buffer_size:
                await self._process_batch()
    
    async def _process_batch(self):
        """Process buffered events."""
        async with self._buffer_lock:
            batch = self.buffer[:self.buffer_size]
            self.buffer = self.buffer[self.buffer_size:]
        
        for processor in self.processors:
            try:
                await processor(batch)
            except Exception as e:
                logger.error(f"Processor error: {e}")
        
        await self._notify_subscribers(batch)
    
    def add_processor(self, processor: Callable):
        self.processors.append(processor)
    
    async def _notify_subscribers(self, events: List[DataEvent]):
        for subscriber in self.subscribers:
            try:
                await subscriber(events)
            except Exception as e:
                logger.error(f"Subscriber error: {e}")

class DataChangeDetector:
    """Detect significant changes in streaming data."""
    
    def __init__(self, threshold: float = 0.1):
        self.threshold = threshold
        self.baseline_stats: Dict[str, float] = {}
    
    async def detect_change(self, new_data: List[Any]) -> bool:
        """Detect if data distribution has changed significantly."""
        current_stats = self._compute_stats(new_data)
        baseline = self.baseline_stats
        
        if not baseline:
            self.baseline_stats = current_stats
            return False
        
        deviation = self._compute_deviation(current_stats, baseline)
        return deviation > self.threshold
    
    def _compute_stats(self, data: List[Any]) -> Dict[str, float]:
        return {
            "mean": np.mean(data) if data else 0,
            "std": np.std(data) if data else 0,
            "count": len(data)
        }
    
    def _compute_deviation(self, current: Dict, baseline: Dict) -> float:
        total_dev = 0
        weights = {"mean": 0.5, "std": 0.3, "count": 0.2}
        
        for key, weight in weights.items():
            if key in current and key in baseline:
                diff = abs(current[key] - baseline[key])
                total_dev += diff * weight
        
        return total_dev / sum(weights.values())
```

---

## 6. Vector Database Patterns

### 6.1 Optimized Vector Storage

```python
import numpy as np
from typing import List, Tuple, Optional

class VectorIndexManager:
    """Manage multiple vector indexes for different use cases."""
    
    def __init__(self):
        self.indexes: Dict[str, Any] = {}
        self.embedding_models: Dict[str, Callable] = {}
    
    def create_index(self, name: str, dimension: int, 
                    index_type: str = "hnsw"):
        """Create optimized vector index."""
        if index_type == "hnsw":
            index = self._create_hnsw_index(dimension)
        elif index_type == "ivf":
            index = self._create_ivf_index(dimension)
        else:
            raise ValueError(f"Unknown index type: {index_type}")
        
        self.indexes[name] = index
        return index
    
    def _create_hnsw_index(self, dimension: int):
        """Create HNSW index for high recall."""
        # Implementation depends on vector DB library (faiss, milvus, etc.)
        pass
    
    def _create_ivf_index(self, dimension: int):
        """Create IVF index for large datasets."""
        pass

class VectorMetadataFilter:
    """Efficient filtering of vector search results."""
    
    def __init__(self, index_manager, metadata_store):
        self.index = index_manager
        self.metadata = metadata_store
    
    def filtered_search(self, query_embedding: np.ndarray, 
                       filters: Dict[str, Any], top_k: int = 10) -> List[Tuple[str, float]]:
        """Search with metadata filters."""
        candidate_ids = self._get_candidate_ids(query_embedding, top_k * 10)
        filtered = []
        
        for doc_id in candidate_ids:
            metadata = self.metadata.get(doc_id)
            if self._matches_filters(metadata, filters):
                score = self._compute_similarity(query_embedding, doc_id)
                filtered.append((doc_id, score))
        
        return sorted(filtered, key=lambda x: x[1], reverse=True)[:top_k]
    
    def _matches_filters(self, metadata: Dict, filters: Dict) -> bool:
        for key, value in filters.items():
            if isinstance(value, list):
                if metadata.get(key) not in value:
                    return False
            else:
                if metadata.get(key) != value:
                    return False
        return True
```

---

## 7. Data Quality Assurance

### 7.1 Automated Data Validation

```python
from typing import List, Dict, Any, Optional
import pandas as pd

class DataQualityValidator:
    """Comprehensive data quality assessment."""
    
    def __init__(self, rules: Dict[str, Callable]):
        self.rules = rules
        self.quality_report: Dict[str, Dict] = {}
    
    def validate(self, df: pd.DataFrame, dataset_name: str) -> Dict:
        """Run all quality checks on dataframe."""
        report = {}
        
        for rule_name, rule_fn in self.rules.items():
            try:
                result = rule_fn(df)
                report[rule_name] = {
                    "passed": result.get("passed", True),
                    "score": result.get("score", 1.0),
                    "details": result.get("details", {})
                }
            except Exception as e:
                report[rule_name] = {"passed": False, "error": str(e)}
        
        self.quality_report[dataset_name] = report
        return report

class CompletenessChecker:
    """Check data completeness and coverage."""
    
    def check_completeness(self, df: pd.DataFrame, 
                          required_columns: List[str]) -> Dict:
        completeness = {}
        for col in required_columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                completeness[col] = {
                    "null_count": null_count,
                    "null_percentage": null_count / len(df) * 100,
                    "missing_count": len(df[df[col] == ""])
                }
        
        overall_score = sum(
            1 - data["null_percentage"] / 100 
            for data in completeness.values()
        ) / len(completeness) if completeness else 1.0
        
        return {
            "passed": all(data["null_percentage"] < 5 for data in completeness.values()),
            "score": overall_score,
            "details": completeness
        }

class ConsistencyValidator:
    """Validate cross-field and cross-record consistency."""
    
    def validate_consistency(self, df: pd.DataFrame, 
                            consistency_rules: List[Dict]) -> Dict:
        issues = []
        
        for rule in consistency_rules:
            check_fn = rule["check"]
            description = rule["description"]
            
            failed_count = df.apply(lambda row: not check_fn(row), axis=1).sum()
            if failed_count > 0:
                issues.append({
                    "rule": description,
                    "failed_count": failed_count
                })
        
        return {
            "passed": len(issues) == 0,
            "score": 1 - len(issues) / len(consistency_rules) if consistency_rules else 1.0,
            "details": {"issues": issues}
        }
```

---

## 8. Cross-Region Data Replication

### 8.1 Active-Active Replication

```python
import asyncio
from typing import List, Dict
import aiohttp

class CrossRegionReplicator:
    """Replicate data across multiple regions for availability."""
    
    def __init__(self, regions: List[str], sync_mode: str = "async"):
        self.regions = regions
        self.sync_mode = sync_mode
        self.replication_lag: Dict[str, float] = {r: 0 for r in regions}
    
    async def replicate(self, data: Any, key: str) -> Dict[str, bool]:
        """Replicate data to all regions."""
        results = {}
        
        if self.sync_mode == "sync":
            tasks = [self._write_to_region(region, key, data) for region in self.regions]
            region_results = await asyncio.gather(*tasks, return_exceptions=True)
            results = {region: result for region, result in zip(self.regions, region_results)}
        else:
            # Async mode - queue for background processing
            for region in self.regions:
                asyncio.create_task(self._write_to_region(region, key, data))
                results[region] = "queued"
        
        return results
    
    async def _write_to_region(self, region: str, key: str, data: Any) -> bool:
        url = f"https://{region}.api.example.com/data/{key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(url, json=data, timeout=30) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"Replication error to {region}: {e}")
            return False
    
    async def read_with_failover(self, key: str) -> Any:
        """Read from first available region."""
        for region in self.regions:
            try:
                data = await self._read_from_region(region, key)
                return data
            except Exception:
                continue
        raise RuntimeError("All regions unavailable")
```

---

## 9. Data Governance Automation

### 9.1 Automated Policy Enforcement

```python
class DataGovernanceEngine:
    """Automated data governance and policy enforcement."""
    
    def __init__(self, policies: List[Dict]):
        self.policies = policies
        self.policy_violations: List[Dict] = []
    
    def enforce_policies(self, data_operation: Dict) -> bool:
        """Check operation against policies."""
        operation_type = data_operation.get("operation")
        data_type = data_operation.get("data_type")
        
        applicable_policies = [
            p for p in self.policies 
            if p["target"] == data_type or p["target"] == "all"
        ]
        
        for policy in applicable_policies:
            if not self._check_policy(policy, data_operation):
                self._record_violation(policy, data_operation)
                return False
        
        return True
    
    def _check_policy(self, policy: Dict, operation: Dict) -> bool:
        """Evaluate single policy against operation."""
        check_fn = policy.get("checker")
        if check_fn:
            return check_fn(operation)
        
        # Built-in checks
        if policy["type"] == "retention":
            return self._check_retention(policy, operation)
        elif policy["type"] == "access_level":
            return self._check_access_level(policy, operation)
        
        return True
    
    def _check_retention(self, policy: Dict, operation: Dict) -> bool:
        """Check data retention policy."""
        created_at = operation.get("created_at")
        retention_days = policy.get("retention_days", 365)
        
        if created_at and (datetime.utcnow() - created_at).days > retention_days:
            return False
        return True
    
    def _check_access_level(self, policy: Dict, operation: Dict) -> bool:
        """Check user access level against policy."""
        user_level = operation.get("user_level", 0)
        required_level = policy.get("required_level", 1)
        return user_level >= required_level
    
    def _record_violation(self, policy: Dict, operation: Dict):
        self.policy_violations.append({
            "policy": policy["name"],
            "operation": operation,
            "timestamp": datetime.utcnow()
        })
```

---

## 10. Event Sourcing for Agents

### 10.1 Event-Sourced Agent State

```python
from dataclasses import dataclass
from typing import Any, List, Dict
import json

@dataclass
class AgentEvent:
    event_id: str
    event_type: str
    timestamp: float
    data: Dict[str, Any]
    version: int = 1

class EventSourcedAgentState:
    """Maintain agent state through event sourcing."""
    
    def __init__(self, event_store):
        self.event_store = event_store
        self.events: List[AgentEvent] = []
        self.state: Dict[str, Any] = {}
        self.version = 0
    
    async def apply_event(self, event: AgentEvent) -> Dict:
        """Apply event and update state."""
        self.events.append(event)
        self.version = event.version
        
        handler = getattr(self, f"_handle_{event.event_type}", None)
        if handler:
            state_changes = handler(event.data)
            self.state = {**self.state, **state_changes}
        
        await self.event_store.append(event)
        return self.state
    
    async def replay(self, event_ids: List[str] = None) -> Dict:
        """Replay events to rebuild state."""
        events = event_ids or [e.event_id for e in self.events]
        
        for event_id in events:
            event = await self.event_store.get(event_id)
            if event:
                await self.apply_event(event)
        
        return self.state
    
    def _handle_tool_used(self, data: Dict) -> Dict:
        tools_used = self.state.get("tools_used", [])
        return {"tools_used": tools_used + [data]}
    
    def _handle_message_added(self, data: Dict) -> Dict:
        messages = self.state.get("messages", [])
        return {"messages": messages + [data]}
    
    def _handle_state_update(self, data: Dict) -> Dict:
        return data

class EventStore:
    """Persistent event storage."""
    
    def __init__(self, backend):
        self.backend = backend
    
    async def append(self, event: AgentEvent) -> str:
        serialized = json.dumps({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "data": event.data,
            "version": event.version
        })
        return await self.backend.save(f"event:{event.event_id}", serialized)
    
    async def get(self, event_id: str) -> Optional[AgentEvent]:
        data = await self.backend.get(f"event:{event_id}")
        if data:
            parsed = json.loads(data)
            return AgentEvent(**parsed)
        return None
    
    async def get_all_for_aggregate(self, aggregate_id: str) -> List[AgentEvent]:
        events = await self.backend.query(f"event:{aggregate_id}:*")
        return [AgentEvent(**json.loads(e)) for e in events]
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Examples](./examples.md)
- [Anti-Patterns](./anti-patterns.md)
- [Checklist](./checklist.md)
- [Troubleshooting](./troubleshooting.md)