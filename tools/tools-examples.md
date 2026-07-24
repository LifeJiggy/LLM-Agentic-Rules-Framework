# Tools Examples - LLM & Agentic Rules Framework

## Overview

This document provides practical implementation examples for tool integration in LLM and agentic systems.

## Example 1: Database Query Tool

### Context

**When to Use**: Need to retrieve data from database

**Goal**: Query customer information securely

### Implementation

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
import hashlib
import time

@dataclass
class ToolConfig:
    tool_id: str
    name: str
    permissions: List[str]
    rate_limit: int
    timeout: int

class DatabaseQueryTool:
    def __init__(self, config: ToolConfig):
        self.config = config
        self.invocation_count = 0
        self.last_invocation_time = 0
    
    def execute(self, query: str, params: Optional[Dict] = None) -> Dict:
        """Execute database query with security controls."""
        # Check rate limit
        if not self.check_rate_limit():
            return {
                "success": False,
                "error": "Rate limit exceeded",
                "retry_after": 30
            }
        
        # Validate input
        if not self.validate_input(query, params):
            return {
                "success": False,
                "error": "Invalid input"
            }
        
        # Execute query
        start_time = time.time()
        try:
            result = self.run_query(query, params)
            duration = time.time() - start_time
            
            # Log audit
            self.log_audit(query, params, result, duration)
            
            return {
                "success": True,
                "result": result,
                "duration_ms": duration * 1000
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_audit(query, params, None, duration, str(e))
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_rate_limit(self) -> bool:
        """Check if rate limit allows invocation."""
        current_time = time.time()
        
        # Reset counter if minute has passed
        if current_time - self.last_invocation_time > 60:
            self.invocation_count = 0
        
        # Check limit
        if self.invocation_count >= self.config.rate_limit:
            return False
        
        self.invocation_count += 1
        self.last_invocation_time = current_time
        return True
    
    def validate_input(self, query: str, params: Optional[Dict]) -> bool:
        """Validate input parameters."""
        # Check query length
        if len(query) > 1000:
            return False
        
        # Check for SQL injection patterns
        dangerous_patterns = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        for pattern in dangerous_patterns:
            if pattern in query.upper():
                return False
        
        return True
    
    def run_query(self, query: str, params: Optional[Dict]) -> List[Dict]:
        """Run database query."""
        # Implement actual database query
        return [{"id": 1, "name": "Example"}]
    
    def log_audit(self, query: str, params: Optional[Dict], result, duration: float, error: str = None):
        """Log audit information."""
        audit_entry = {
            "tool_id": self.config.tool_id,
            "query": query,
            "params": params,
            "success": error is None,
            "duration_ms": duration * 1000,
            "timestamp": time.time()
        }
        
        if error:
            audit_entry["error"] = error
        
        # Store audit entry
        print(f"Audit: {audit_entry}")

# Example usage
config = ToolConfig(
    tool_id="db_query_001",
    name="Database Query",
    permissions=["read:customers", "read:orders"],
    rate_limit=50,
    timeout=10
)

tool = DatabaseQueryTool(config)
result = tool.execute("SELECT * FROM customers WHERE id = ?", {"id": 123})
print(f"Result: {result}")
```

### Expected Outcome

- Query executed securely
- Rate limiting enforced
- Input validated
- Audit logged

### Verification

- [ ] Query executes correctly
- [ ] Rate limiting works
- [ ] Input validation works
- [ ] Audit logging works
- [ ] Error handling works

## Example 2: Email Sending Tool

### Context

**When to Use**: Need to send emails

**Goal**: Send notifications securely

### Implementation

```python
from typing import Dict, List, Optional
from dataclasses import dataclass
import re
import time

@dataclass
class EmailConfig:
    tool_id: str
    name: str
    permissions: List[str]
    rate_limit: int
    timeout: int
    allowed_domains: List[str]

class EmailTool:
    def __init__(self, config: EmailConfig):
        self.config = config
        self.invocation_count = 0
        self.last_invocation_time = 0
    
    def send(self, to: str, subject: str, body: str, attachments: Optional[List[str]] = None) -> Dict:
        """Send email with security controls."""
        # Check rate limit
        if not self.check_rate_limit():
            return {
                "success": False,
                "error": "Rate limit exceeded",
                "retry_after": 60
            }
        
        # Validate input
        validation_result = self.validate_input(to, subject, body, attachments)
        if not validation_result["valid"]:
            return {
                "success": False,
                "error": validation_result["error"]
            }
        
        # Check recipient domain
        if not self.check_recipient_domain(to):
            return {
                "success": False,
                "error": "Recipient domain not allowed"
            }
        
        # Send email
        start_time = time.time()
        try:
            result = self.send_email(to, subject, body, attachments)
            duration = time.time() - start_time
            
            # Log audit
            self.log_audit(to, subject, duration)
            
            return {
                "success": True,
                "message_id": result["message_id"],
                "duration_ms": duration * 1000
            }
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_audit(to, subject, duration, str(e))
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_rate_limit(self) -> bool:
        """Check if rate limit allows invocation."""
        current_time = time.time()
        
        # Reset counter if minute has passed
        if current_time - self.last_invocation_time > 60:
            self.invocation_count = 0
        
        # Check limit
        if self.invocation_count >= self.config.rate_limit:
            return False
        
        self.invocation_count += 1
        self.last_invocation_time = current_time
        return True
    
    def validate_input(self, to: str, subject: str, body: str, attachments: Optional[List[str]]) -> Dict:
        """Validate input parameters."""
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, to):
            return {"valid": False, "error": "Invalid email format"}
        
        # Validate subject length
        if len(subject) > 200:
            return {"valid": False, "error": "Subject too long"}
        
        # Validate body length
        if len(body) > 10000:
            return {"valid": False, "error": "Body too long"}
        
        # Validate attachments
        if attachments:
            for attachment in attachments:
                if len(attachment) > 10 * 1024 * 1024:  # 10MB
                    return {"valid": False, "error": "Attachment too large"}
        
        return {"valid": True}
    
    def check_recipient_domain(self, email: str) -> bool:
        """Check if recipient domain is allowed."""
        domain = email.split('@')[1]
        return domain in self.config.allowed_domains
    
    def send_email(self, to: str, subject: str, body: str, attachments: Optional[List[str]]) -> Dict:
        """Send email."""
        # Implement actual email sending
        return {"message_id": "msg_123"}
    
    def log_audit(self, to: str, subject: str, duration: float, error: str = None):
        """Log audit information."""
        audit_entry = {
            "tool_id": self.config.tool_id,
            "to": to,
            "subject": subject,
            "success": error is None,
            "duration_ms": duration * 1000,
            "timestamp": time.time()
        }
        
        if error:
            audit_entry["error"] = error
        
        # Store audit entry
        print(f"Audit: {audit_entry}")

# Example usage
config = EmailConfig(
    tool_id="email_001",
    name="Email Sender",
    permissions=["send:email"],
    rate_limit=10,
    timeout=30,
    allowed_domains=["company.com"]
)

tool = EmailTool(config)
result = tool.send(
    to="user@company.com",
    subject="Notification",
    body="This is a test email."
)
print(f"Result: {result}")
```

### Expected Outcome

- Email sent securely
- Rate limiting enforced
- Input validated
- Domain restrictions enforced
- Audit logged

### Verification

- [ ] Email sends correctly
- [ ] Rate limiting works
- [ ] Input validation works
- [ ] Domain restrictions work
- [ ] Audit logging works

## Example Summary

| Example | Complexity | Time Required | Key Concepts |
|---------|------------|---------------|--------------|
| Database Query | Medium | 45 minutes | Rate limiting, input validation, audit logging |
| Email Sending | Medium | 45 minutes | Domain restrictions, attachment validation, audit logging |

## References

- Tool fundamentals: `tools-fundamentals.md`
- Tool best practices: `tools-best-practices.md`
- Tool anti-patterns: `tools-anti-patterns.md`
- Tool checklist: `tools-checklist.md`
- Tool troubleshooting: `tools-troubleshooting.md`
- Tool advanced: `tools-advanced.md`
