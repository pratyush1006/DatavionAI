# Architecture Overview

DatavionAI follows a layered architecture.

```
                DatavionAI
                     │
      ┌──────────────┴───────────────┐
      │                              │
  Platform Layer               Business Layer
      │                              │
 Logging                     Workforce
 Audit                       Healthcare
 Security                    Revenue Cycle
 Common                      AI
```

## Platform Layer

Provides reusable infrastructure:

- Logging
- Audit
- Authentication
- Request Correlation
- Pagination
- Exception Handling
- API Responses

## Business Layer

Contains all business modules.

Every module follows:

- Model
- Selector
- Service
- Serializer
- API View
- Tests

Business modules never communicate directly with each other.
