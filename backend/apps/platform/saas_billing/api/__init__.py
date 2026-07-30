"""
DatavionOS SaaS Billing API layer.

Exposes:

- Billing Account APIs
- Subscription APIs
- Invoice APIs
- Payment APIs
- Usage APIs

Architecture:

Request
    |
Permission
    |
Serializer
    |
Workflow Registry
    |
Workflow
    |
Service
    |
Domain Event
"""
