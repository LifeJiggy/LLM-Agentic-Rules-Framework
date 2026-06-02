# Integration Domain - Best Practices

## Overview

This document outlines integration best practices for LLM/agentic systems.

## API Best Practices

### 1. Use Pagination

```python
@app.route("/api/users")
def get_users():
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", 20)
    
    users = User.query.paginate(
        page=int(page), 
        per_page=int(per_page)
    )
    
    return jsonify({
        "data": [u.to_dict() for u in users.items],
        "total": users.total,
        "page": users.page
    })
```

### 2. Implement Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api/data")
@limiter.limit("100 per minute")
def get_data():
    return jsonify(data)
```

### 3. Use Webhooks

```python
class WebhookHandler:
    def __init__(self, url, secret):
        self.url = url
        self.secret = secret
    
    def send(self, event_type, payload):
        headers = {"X-Webhook-Secret": self.secret}
        return requests.post(self.url, json=payload, headers=headers)
```

## Related Files

- [Fundamentals](./fundamentals.md)
- [Anti-Patterns](./anti-patterns.md)
- [Examples](./examples.md)
