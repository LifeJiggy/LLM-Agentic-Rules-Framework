# Integration Domain - Examples

## Overview

This document provides concrete code examples for implementing integration patterns in LLM/agentic systems, including API workflows, webhook handling, streaming, and service integration.

---

## Example 1: RESTful Agent API

```python
from flask import Flask, request, jsonify
from pydantic import BaseModel, Field
import asyncio

app = Flask(__name__)

class ProcessRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000)
    session_id: str
    context: dict = Field(default_factory=dict)

@app.route("/api/v1/agent/process", methods=["POST"])
async def process():
    try:
        req = ProcessRequest(**request.json)
    except Exception as e:
        return jsonify({"error": "Invalid request", "details": str(e)}), 400
    
    result = await agent.process(req.prompt, req.session_id, req.context)
    return jsonify({"response": result})

# Usage with curl
# curl -X POST http://localhost:5000/api/v1/agent/process \
#   -H "Content-Type: application/json" \
#   -d '{"prompt": "Hello", "session_id": "abc123"}'
```

---

## Example 2: Webhook Integration

```python
import hmac
import hashlib
import json
import asyncio
import aiohttp

class WebhookIntegration:
    def __init__(self, endpoints, signing_secret):
        self.endpoints = endpoints
        self.secret = signing_secret
    
    async def notify(self, event_type, payload):
        message = {"event": event_type, "data": payload, "timestamp": time.time()}
        signature = self._sign(message)
        
        for url in self.endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        url,
                        json=message,
                        headers={"X-Hub-Signature-256": signature}
                    )
            except Exception as e:
                logger.error(f"Webhook delivery failed to {url}: {e}")
    
    def _sign(self, payload):
        data = json.dumps(payload).encode()
        sig = hmac.new(self.secret, data, hashlib.sha256).hexdigest()
        return f"sha256={sig}"

# Usage
webhook = WebhookIntegration(["https://app.example.com/webhook"], "secret_key")
await webhook.notify("agent.completed", {"session_id": "123", "result": "done"})
```

---

## Example 3: streaming Integration

```python
from flask import Response, stream_with_context
import json

@app.route("/api/v1/agent/stream")
def stream():
    prompt = request.args.get("prompt", "")
    
    def generate():
        async def stream_chunks():
            async for chunk in agent.stream_response(prompt):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        loop = asyncio.new_event_loop()
        for chunk in loop.run_until_complete(stream_chunks()):
            yield chunk
    
    return Response(generate(), mimetype="text/event-stream")
```

---

## Example 4: GraphQL Agent Integration

```python
from ariadne import QueryType, MutationType, graphql_sync
from ariadne.asgi import GraphQL
from pydantic import BaseModel

query = QueryType()
mutation = MutationType()

class AgentInput(BaseModel):
    session_id: str
    prompt: str
    context: dict = {}

@query.field("agentSession")
async def resolve_session(obj, info, session_id: str):
    return await info.context["agent"].get_session(session_id)

@mutation.field("processPrompt")
async def resolve_process(obj, info, input: AgentInput):
    result = await info.context["agent"].process(
        input.prompt, input.session_id, input.context
    )
    return {"response": result, "session_id": input.session_id}

schema = graphql_sync(query.type_defs + mutation.type_defs)
app = GraphQL(schema, debug=True)

# Query
# query {
#   agentSession(session_id: "abc123") {
#     id
#     messages {
#       role
#       content
#     }
#   }
# }

# Mutation
# mutation {
#   processPrompt(input: {
#     sessionId: "abc123"
#     prompt: "Hello agent"
#   }) {
#     response
#     sessionId
#   }
# }
```

---

## Example 5: MCP (Model Context Protocol) Integration

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio

mcp_server = Server("agentic-llm-server")

@mcp_server.list_tools()
async def list_tools():
    return [
        Tool(
            name="agent_process",
            description="Process a prompt through the agent",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "User prompt"},
                    "session_id": {"type": "string"},
                    "context": {"type": "object"}
                },
                "required": ["prompt", "session_id"]
            }
        ),
        Tool(
            name="agent_stream",
            description="Stream agent response",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "session_id": {"type": "string"}
                },
                "required": ["prompt", "session_id"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "agent_process":
        result = await agent.process(
            arguments["prompt"],
            arguments["session_id"],
            arguments.get("context", {})
        )
        return [TextContent(type="text", text=result)]
    elif name == "agent_stream":
        chunks = []
        async for chunk in agent.stream_response(
            arguments["prompt"],
            arguments["session_id"]
        ):
            chunks.append(chunk)
        return [TextContent(type="text", text="".join(chunks))]
    raise ValueError(f"Unknown tool: {name}")

# Run with: mcp-server-run --transport stdio agent_mcp.py
```

---

## Example 6: Database Integration (PostgreSQL + Vector Store)

```python
import asyncpg
from pgvector.asyncpg import register_vector
import numpy as np

class AgentMemoryDB:
    def __init__(self, dsn: str, vector_table: str = "agent_memories"):
        self.dsn = dsn
        self.vector_table = vector_table
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(self.dsn)
        async with self.pool.acquire() as conn:
            await register_vector(conn)
    
    async def store_memory(self, session_id: str, content: str, embedding: np.ndarray):
        async with self.pool.acquire() as conn:
            await conn.execute(
                f"INSERT INTO {self.vector_table} (session_id, content, embedding) VALUES ($1, $2, $3)",
                session_id, content, embedding.tolist()
            )
    
    async def search_memories(self, session_id: str, query_embedding: np.ndarray, limit: int = 5):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                f"SELECT content, embedding <=> $1 AS distance FROM {self.vector_table} WHERE session_id = $2 ORDER BY distance LIMIT $3",
                query_embedding.tolist(), session_id, limit
            )
            return [{"content": row["content"], "score": row["distance"]} for row in rows]

# Usage
db = AgentMemoryDB("postgresql://localhost/agent_db")
await db.connect()
embeddings = np.array([0.1, 0.2, 0.3, ...])
await db.store_memory("session123", "User asked about pricing", embeddings)
results = await db.search_memories("session123", embeddings)
```

---

## Example 7: Redis / Celery Task Queue Integration

```python
from celery import Celery
import os

celery_app = Celery(
    "agent_tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery_app.conf.task_routes = {
    "agent_tasks.process_long_task": {"queue": "agent_processing"},
    "agent_tasks.stream_chunks": {"queue": "agent_streaming"},
}

@celery_app.task(bind=True, name="agent_tasks.process_long_task")
def process_long_task(self, session_id: str, prompt: str, context: dict = None):
    try:
        result = asyncio.run(agent.process(prompt, session_id, context or {}))
        return {"session_id": session_id, "status": "completed", "result": result}
    except Exception as exc:
        self.retry(exc=exc, countdown=60, max_retries=3)

@celery_app.task(name="agent_tasks.stream_chunks")
def stream_chunks_task(session_id: str, prompt: str):
    async def _stream():
        chunks = []
        async for chunk in agent.stream_response(prompt, session_id):
            chunks.append(chunk)
        return chunks
    return asyncio.run(_stream())

# Trigger task
# task = process_long_task.delay("abc123", "Summarize this document", {"doc_id": "456"})
# result = task.get(timeout=300)
```

---

## Example 8: OAuth 2.0 / Authentication Integration

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import httpx

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_authenticated_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

@app.post("/api/v1/agent/process", dependencies=[Depends(get_authenticated_user)])
async def authenticated_process(request: AgentRequest, user_id: str = Depends(get_authenticated_user)):
    enriched_context = {**request.context, "authenticated_user": user_id}
    result = await agent.process(request.prompt, request.session_id, enriched_context)
    return {"response": result, "user": user_id}

# Token endpoint
@app.post("/api/v1/token")
async def oauth_token(form_data: OAuth2PasswordRequestForm = Depends()):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://auth.example.com/oauth/token",
            data={
                "grant_type": "password",
                "username": form_data.username,
                "password": form_data.password,
                "client_id": os.getenv("OAUTH_CLIENT_ID"),
                "client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
            }
        )
        return resp.json()
```

---

## Example 9: Cloud Storage (S3 / GCS) Integration

```python
import boto3
from botocore.exceptions import ClientError
import json
from io import BytesIO

class AgentStorage:
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.s3 = boto3.client("s3", region_name=region)
        self.bucket = bucket_name
    
    async def store_conversation(self, session_id: str, messages: list[dict]):
        key = f"conversations/{session_id}.json"
        data = json.dumps(messages).encode()
        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=data,
                ContentType="application/json",
                ServerSideEncryption="AES256"
            )
        except ClientError as e:
            logger.error(f"Storage error: {e}")
            raise
    
    async def load_conversation(self, session_id: str) -> list[dict]:
        key = f"conversations/{session_id}.json"
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            content = response["Body"].read().decode()
            return json.loads(content)
        except self.s3.exceptions.NoSuchKey:
            return []
    
    async def store_artifact(self, session_id: str, filename: str, content: bytes):
        key = f"artifacts/{session_id}/{filename}"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ServerSideEncryption="AES256",
            Metadata={"session_id": session_id}
        )
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"

# Usage with FastAPI
@app.post("/api/v1/agent/process-with-storage")
async def process_with_storage(request: AgentRequest):
    messages = await storage.load_conversation(request.session_id)
    result = await agent.process(request.prompt, request.session_id, request.context)
    messages.append({"role": "user", "content": request.prompt})
    messages.append({"role": "agent", "content": result})
    await storage.store_conversation(request.session_id, messages)
    return {"response": result, "stored": True}
```

---

## Example 10: Multi-Agent Orchestration Integration

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_agent: str
    task_complete: bool

class Orchestrator:
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("router", self.route)
        workflow.add_node("research_agent", self.run_research)
        workflow.add_node("writing_agent", self.run_writing)
        workflow.add_node("review_agent", self.run_review)
        
        workflow.set_entry_point("router")
        workflow.add_edge("router", "research_agent")
        workflow.add_conditional_edges(
            "research_agent",
            lambda state: state["next_agent"],
            {
                "writing": "writing_agent",
                "review": "review_agent",
                "end": END
            }
        )
        workflow.add_conditional_edges(
            "writing_agent",
            lambda state: state["next_agent"],
            {
                "review": "review_agent",
                "end": END
            }
        )
        workflow.add_edge("review_agent", END)
        
        return workflow.compile()
    
    async def route(self, state: AgentState):
        last_msg = state["messages"][-1]
        decision = await self.router_agent.decide(last_msg)
        return {"next_agent": decision}
    
    async def run_research(self, state: AgentState):
        result = await research_agent.execute(state["messages"])
        return {"messages": [result], "next_agent": "writing"}
    
    async def run_writing(self, state: AgentState):
        result = await writing_agent.execute(state["messages"])
        return {"messages": [result], "next_agent": "end"}
    
    async def run_review(self, state: AgentState):
        result = await review_agent.execute(state["messages"])
        return {"messages": [result], "task_complete": True}
    
    async def execute(self, initial_state: AgentState):
        async for event in self.graph.astream(initial_state):
            yield event

# Usage
orchestrator = Orchestrator()
state = {
    "messages": [{"role": "user", "content": "Write a report on AI trends"}],
    "next_agent": "router",
    "task_complete": False
}
async for step in orchestrator.execute(state):
    logger.info(f"Step completed: {step.keys()}")
```

---

## Example 11: gRPC Streaming Integration

```python
import grpc
from concurrent import futures
import asyncio

# Generated from proto definition
# agent.proto:
#   service AgentService {
#     rpc Process (ProcessRequest) returns (ProcessResponse);
#     rpc Stream (StreamRequest) returns (stream StreamChunk);
#   }

import agent_pb2
import agent_pb2_grpc

class AgentServicer(agent_pb2_grpc.AgentServiceServicer):
    async def Process(self, request, context):
        try:
            result = await agent.process(
                request.prompt,
                request.session_id,
                json.loads(request.context)
            )
            return agent_pb2.ProcessResponse(response=result)
        except Exception as e:
            await context.set_code(grpc.StatusCode.INTERNAL)
            await context.set_details(str(e))
            return agent_pb2.ProcessResponse()
    
    async def Stream(self, request, context):
        try:
            async for chunk in agent.stream_response(request.prompt, request.session_id):
                yield agent_pb2.StreamChunk(chunk=chunk)
        except Exception as e:
            await context.set_code(grpc.StatusCode.INTERNAL)
            await context.set_details(str(e))
    
    async def BidirectionalStream(self, request_iterator, context):
        async for request in request_iterator:
            result = await agent.process(
                request.prompt,
                request.session_id,
                json.loads(request.context)
            )
            yield agent_pb2.ProcessResponse(response=result)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

# Run with: python -m agent_grpc
```

---

## Example 12: Event-Driven Architecture (Kafka Integration)

```python
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio

class EventDrivenAgent:
    def __init__(self, bootstrap_servers: list, topic_prefix: str = "agent"):
        self.bootstrap_servers = bootstrap_servers
        self.topic_prefix = topic_prefix
        self.producer = None
        self.consumer = None
    
    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
        self.consumer = AIOKafkaConsumer(
            f"{self.topic_prefix}.requests",
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda v: json.loads(v),
            group_id="agent-workers",
            auto_offset_reset="earliest"
        )
        await self.producer.start()
        await self.consumer.start()
    
    async def produce_event(self, event_type: str, payload: dict):
        message = {
            "event": event_type,
            "data": payload,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "agent-service"
        }
        await self.producer.send_and_wait(f"{self.topic_prefix}.{event_type}", message)
    
    async def consume_events(self):
        async for msg in self.consumer:
            try:
                event = msg.value
                result = await self.handle_event(event)
                await self.produce_event(f"{event['event']}.completed", {
                    "correlation_id": event.get("correlation_id"),
                    "result": result
                })
            except Exception as e:
                logger.error(f"Event processing failed: {e}")
                await self.produce_event(f"{event['event']}.failed", {
                    "correlation_id": event.get("correlation_id"),
                    "error": str(e)
                })
    
    async def handle_event(self, event: dict):
        event_type = event["event"]
        data = event["data"]
        if event_type == "agent.process":
            return await agent.process(data["prompt"], data["session_id"], data.get("context", {}))
        elif event_type == "agent.stream":
            return await agent.stream_response(data["prompt"], data["session_id"])
        raise ValueError(f"Unknown event: {event_type}")

# Usage
event_agent = EventDrivenAgent(["localhost:9092"])
await event_agent.start()
asyncio.create_task(event_agent.consume_events())
await event_agent.produce_event("agent.process", {"prompt": "Hello", "session_id": "abc"})
```

---

## Example 13: WebSocket Real-Time Integration

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_json(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/agent/{session_id}")
async def agent_websocket(websocket: WebSocket, session_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "process":
                result = await agent.process(
                    message["prompt"], session_id, message.get("context", {})
                )
                await manager.send_json({
                    "type": "response",
                    "session_id": session_id,
                    "data": result
                }, websocket)
            
            elif message["type"] == "stream":
                async for chunk in agent.stream_response(message["prompt"], session_id):
                    await manager.send_json({
                        "type": "chunk",
                        "session_id": session_id,
                        "chunk": chunk
                    }, websocket)
                await manager.send_json({"type": "stream_end", "session_id": session_id}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected: {session_id}")
```

---

## Example 14: Third-Party API Proxy / API Gateway

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import time

app = FastAPI()
AGENT_INTERNAL_URL = os.getenv("AGENT_INTERNAL_URL", "http://localhost:8000")
API_KEYS = {os.getenv("API_KEY", "demo-key"): "demo-org"}
RATE_LIMITS = {"demo-org": 100}  # requests per minute

request_counts = {}

class APIGateway:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def forward_request(self, path: str, headers: dict, body: bytes, method: str = "POST"):
        rate_ok, remaining = self.check_rate_limit(headers.get("X-API-Key"))
        if not rate_ok:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        forward_headers = {
            "X-Forwarded-For": headers.get("X-Forwarded-For", ""),
            "X-Original-User-Agent": headers.get("User-Agent", ""),
            "X-RateLimit-Remaining": str(remaining)
        }
        
        response = await self.client.request(
            method=method,
            url=f"{AGENT_INTERNAL_URL}{path}",
            headers=forward_headers,
            content=body
        )
        return response
    
    def check_rate_limit(self, api_key: str) -> tuple[bool, int]:
        org = API_KEYS.get(api_key)
        if not org:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        now = time.time()
        count, window_start = request_counts.get(org, (0, now))
        
        if now - window_start > 60:
            count = 0
            window_start = now
        
        count += 1
        request_counts[org] = (count, window_start)
        
        if count > RATE_LIMITS.get(org, 100):
            return (False, 0)
        return (True, RATE_LIMITS.get(org, 100) - count)

gateway = APIGateway()

@app.api_route("/api/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_endpoint(request: Request, path: str):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header required")
    
    body = await request.body()
    response = await gateway.forward_request(
        f"/api/v1/{path}",
        dict(request.headers),
        body,
        request.method
    )
    return JSONResponse(content=response.json(), status_code=response.status_code)
```

---

## Example 15: LangChain / LlamaIndex Framework Integration

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class AgentToolInput(BaseModel):
    prompt: str = Field(description="The prompt to send to the agent")

class IntegrationAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.tools = self._create_tools()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant with access to tools."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.agent = create_openai_tools_agent(llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    
    def _create_tools(self):
        def process_tool(prompt: str) -> str:
            result = asyncio.run(agent.process(prompt, "langchain_session", {}))
            return result
        
        return [
            StructuredTool.from_function(
                name="agent_process",
                func=process_tool,
                description="Process a prompt with the agent",
                args_schema=AgentToolInput
            )
        ]
    
    async def run(self, query: str, chat_history: list = None):
        return await self.executor.ainvoke({
            "input": query,
            "chat_history": chat_history or []
        })

# Usage
llm = ChatOpenAI(model="gpt-4o", temperature=0)
integration_agent = IntegrationAgent(llm)
result = await integration_agent.run("What is the status of my ticket?")
```

---

## Example 16: Monitoring & Observability Integration

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import functools
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

REQUEST_COUNT = Counter(
    "agent_requests_total",
    "Total agent requests",
    ["endpoint", "method", "status"]
)
REQUEST_LATENCY = Histogram(
    "agent_request_duration_seconds",
    "Request duration",
    ["endpoint"]
)
ACTIVE_SESSIONS = Gauge(
    "agent_active_sessions",
    "Active agent sessions"
)

def monitor(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        endpoint = func.__name__
        try:
            result = await func(*args, **kwargs)
            REQUEST_COUNT.labels(endpoint=endpoint, method="async", status="success").inc()
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start)
            logger.info("request_completed", endpoint=endpoint, duration=time.time() - start)
            return result
        except Exception as e:
            REQUEST_COUNT.labels(endpoint=endpoint, method="async", status="error").inc()
            logger.error("request_failed", endpoint=endpoint, error=str(e))
            raise
    return wrapper

class MonitoredAgent:
    def __init__(self, agent):
        self.agent = agent
    
    @monitor
    async def process(self, prompt: str, session_id: str, context: dict):
        ACTIVE_SESSIONS.inc()
        try:
            return await self.agent.process(prompt, session_id, context)
        finally:
            ACTIVE_SESSIONS.dec()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        REQUEST_COUNT.labels(
            endpoint=request.url.path,
            method=request.method,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(time.time() - start)
        return response
    except Exception as e:
        REQUEST_COUNT.labels(
            endpoint=request.url.path,
            method=request.method,
            status="error"
        ).inc()
        raise

@app.on_event("startup")
async def startup():
    start_http_server(9090)
    logger.info("metrics_server_started", port=9090)
```

---

## Example 17: CI/CD Pipeline Integration (GitHub Actions)

```yaml
# .github/workflows/agent-ci.yml
name: Agent Integration Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: agent_test
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov
      
      - name: Run linters
        run: |
          ruff check .
          mypy .
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/agent_test
          AGENT_API_KEY: ${{ secrets.TEST_AGENT_API_KEY }}
        run: |
          pytest tests/integration/ -v --cov=src --cov-report=xml -x
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to production
        env:
          DEPLOY_API_KEY: ${{ secrets.DEPLOY_API_KEY }}
        run: |
          curl -X POST https://deploy.example.com/api/deploy \
            -H "Authorization: Bearer $DEPLOY_API_KEY" \
            -d '{"image": "agent:sha-${{ github.sha }}", "env": "prod"}'
      
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          slack-message: "Agent deployed: ${{ github.sha }}"
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Example 18: Caching Layer (Redis Integration)

```python
import redis.asyncio as aioredis
import pickle
import hashlib
from functools import wraps

class CacheAgent:
    def __init__(self, redis_url: str, ttl: int = 3600, agent=None):
        self.redis = aioredis.from_url(redis_url, decode_responses=False)
        self.ttl = ttl
        self.agent = agent
    
    def _cache_key(self, prompt: str, session_id: str, context: dict) -> str:
        raw = f"{prompt}:{session_id}:{json.dumps(context, sort_keys=True)}"
        digest = hashlib.sha256(raw.encode()).hexdigest()
        return f"agent:cache:{digest}"
    
    async def get(self, key: str):
        value = await self.redis.get(key)
        if value is None:
            return None
        return pickle.loads(value)
    
    async def set(self, key: str, value, ttl: int = None):
        await self.redis.setex(key, ttl or self.ttl, pickle.dumps(value))
    
    async def cached_process(self, prompt: str, session_id: str, context: dict, skip_cache: bool = False):
        if not skip_cache:
            cache_key = self._cache_key(prompt, session_id, context)
            cached = await self.get(cache_key)
            if cached is not None:
                logger.info("cache_hit", key=cache_key)
                return cached
        
        result = await self.agent.process(prompt, session_id, context)
        if not skip_cache:
            cache_key = self._cache_key(prompt, session_id, context)
            await self.set(cache_key, result)
            logger.info("cache_set", key=cache_key)
        
        return result
    
    async def invalidate_session(self, session_id: str):
        pattern = f"agent:cache:*{session_id}*"
        keys = []
        async for key in self.redis.scan_iter(pattern):
            keys.append(key)
        if keys:
            await self.redis.delete(*keys)
    
    async def health_check(self) -> bool:
        try:
            return await self.redis.ping()
        except Exception:
            return False

# Usage
cache = CacheAgent("redis://localhost:6379/0", agent=agent)
result = await cache.cached_process("explain quantum computing", "session123", {})
```

---

## Example 19: Email / Notification Integration

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultultipart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

class NotificationService:
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
    
    async def send_email(self, to: str, subject: str, body: str, html: bool = False):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._send_sync, to, subject, body, html)
    
    def _send_sync(self, to: str, subject: str, body: str, html: bool = False):
        msg = MIMEMultipart("alternative")
        msg["From"] = self.smtp_user
        msg["To"] = to
        msg["Subject"] = subject
        
        content_type = "html" if html else "plain"
        msg.attach(MIMEText(body, content_type))
        
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.send_message(msg)
    
    async def notify_agent_completion(self, session_id: str, user_email: str, result_summary: str):
        await self.send_email(
            to=user_email,
            subject=f"Agent Session {session_id} Completed",
            body=f"Your agent session has completed.\n\n{result_summary}\n\nView details at https://app.example.com/sessions/{session_id}"
        )

class AgentEventNotifier:
    def __init__(self, webhook_integration, notification_service):
        self.webhooks = webhook_integration
        self.notifications = notification_service
    
    async def notify(self, event: str, session_id: str, user_email: str = None, payload: dict = None):
        await self.webhooks.notify(event, {"session_id": session_id, **(payload or {})})
        
        if event == "agent.completed" and user_email:
            summary = payload.get("summary", "Task completed successfully")
            await self.notifications.notify_agent_completion(session_id, user_email, summary)
        
        if event == "agent.failed" and user_email:
            error = payload.get("error", "Unknown error")
            await self.notifications.send_email(
                to=user_email,
                subject=f"Agent Session {session_id} Failed",
                body=f"Agent session encountered an error:\n\n{error}\n\nSession: {session_id}"
            )

# Usage
notifier = AgentEventNotifier(webhook, NotificationService("smtp.example.com", 587, "user", "pass"))
await notifier.notify("agent.completed", "abc123", "user@example.com", {"summary": "Report generated"})
```

---

## Example 20: Docker / Container Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

ENV AGENT_ENV=production
ENV LOG_LEVEL=INFO

EXPOSE 8000
EXPOSE 9090

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/agent_db
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_USER: postgres
      POSTGRES_DB: agent_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
  
  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
  redisdata:
```

---

## Example 21: Health Check & Graceful Shutdown

```python
import signal
import asyncio
from fastapi import FastAPI

class HealthManager:
    def __init__(self):
        self.is_shutting_down = False
    
    async def full_health_check(self):
        checks = {
            "api": self.check_api(),
            "database": self.check_database(),
            "redis": self.check_redis(),
            "llm_provider": self.check_llm()
        }
        results = {}
        for name, coro in checks.items():
            try:
                ok = await asyncio.wait_for(coro, timeout=5.0)
                results[name] = "healthy" if ok else "unhealthy"
            except asyncio.TimeoutError:
                results[name] = "timeout"
            except Exception as e:
                results[name] = f"error: {str(e)}"
        
        overall = all(v == "healthy" for v in results.values())
        return {"status": "healthy" if overall else "degraded", "checks": results}
    
    async def check_database(self):
        async with db.pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return True
    
    async def check_redis(self):
        return await cache.redis.ping()
    
    async def check_llm(self):
        return await llm_client.health_check()

health_manager = HealthManager()

@app.get("/health")
async def health_check():
    return await health_manager.full_health_check()

@app.get("/health/ready")
async def readiness():
    return {"status": "ready"}

@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

def setup_graceful_shutdown(app: FastAPI):
    loop = asyncio.get_event_loop()
    
    def shutdown():
        if health_manager.is_shutting_down:
            return
        health_manager.is_shutting_down = True
        logger.info("shutdown_signal_received")
        loop.create_task(_graceful_shutdown(app))
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)
    
    return shutdown

async def _graceful_shutdown(app: FastAPI):
    await db.close()
    await cache.redis.close()
    await llm_client.close()
    logger.info("all_resources_closed")

shutdown_handler = setup_graceful_shutdown(app)
```

---

## Example 22: Config-Managed Integration Flags

```python
import os
from pydantic_settings import BaseSettings
from enum import Enum

class IntegrationMode(str, Enum):
    DIRECT = "direct"
    QUEUED = "queued"
    STREAMING = "streaming"

class AgentIntegrationConfig(BaseSettings):
    mode: IntegrationMode = IntegrationMode.DIRECT
    redis_url: str = "redis://localhost:6379/0"
    kafka_brokers: str = "localhost:9092"
    mcp_enabled: bool = False
    mcp_server_url: str = "http://localhost:5001"
    max_concurrent_requests: int = 10
    request_timeout: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False

config = AgentIntegrationConfig()

class ModeAdapter:
    def __init__(self, config: AgentIntegrationConfig, agent):
        self.config = config
        self.agent = agent
        self._setup_mode()
    
    def _setup_mode(self):
        if self.config.mode == IntegrationMode.QUEUED:
            from celery import Celery
            self.task_queue = Celery(
                "agent",
                broker=self.config.redis_url,
                backend=self.config.redis_url
            )
            @self.task_queue.task(bind=True)
            def process(self, session_id: str, prompt: str, context: dict):
                return asyncio.run(self.agent.process(prompt, session_id, context))
            self.task_queue.process = process
        
        elif self.config.mode == IntegrationMode.STREAMING:
            self.chunk_buffer = []
        
        elif self.config.mode == IntegrationMode.DIRECT:
            pass
    
    async def execute(self, prompt: str, session_id: str, context: dict):
        if self.config.mode == IntegrationMode.QUEUED:
            task = self.task_queue.process.delay(session_id, prompt, context)
            return await asyncio.to_thread(task.get, timeout=self.config.request_timeout)
        
        elif self.config.mode == IntegrationMode.STREAMING:
            chunks = []
            async for chunk in self.agent.stream_response(prompt, session_id):
                chunks.append(chunk)
            return "".join(chunks)
        
        return await self.agent.process(prompt, session_id, context)

# Usage: set AGENT_INTEGRATION_MODE=queued in .env
adapter = ModeAdapter(config, agent)
result = await adapter.execute("Hello", "abc123", {})
```

---

## Related Files

- [Fundamentals](./fundamentals.md)
- [Best Practices](./best-practices.md)
- [Anti-Patterns](./anti-patterns.md)