"""
Employee domain models.

Central export point for all
employee management entities.

Architecture:

Organization
    |
    +-- Employee
          |
          +-- Profile
          +-- Address
          +-- Identifiers
          +-- Documents
          +-- Emergency Contacts
          +-- Position
          +-- Assignment
          +-- Contracts
          +-- Skills
          +-- Education
          +-- Experience
          +-- Lifecycle History

Design Principles:

- Stable import boundary
- Hide internal module structure
- Prevent direct implementation imports
- Support future refactoring
"""

from __future__ import annotations

from .employee import Employee
from .employee_address import EmployeeAddress
from .employee_assignment import EmployeeAssignment
from .employee_contract import EmployeeContract
from .employee_document import EmployeeDocument
from .employee_education import EmployeeEducation
from .employee_emergency_contact import EmployeeEmergencyContact
from .employee_experience import EmployeeExperience
from .employee_history import EmployeeHistory
from .employee_identifier import EmployeeIdentifier
from .employee_position import EmployeePosition
from .employee_profile import EmployeeProfile
from .employee_skill import EmployeeSkill

__all__: tuple[str, ...] = (
    # Core Employee
    "Employee",
    # Personal Information
    "EmployeeProfile",
    "EmployeeAddress",
    "EmployeeEmergencyContact",
    # Organization Structure
    "EmployeePosition",
    "EmployeeAssignment",
    # Employment Lifecycle
    "EmployeeContract",
    "EmployeeHistory",
    # Professional Information
    "EmployeeEducation",
    "EmployeeExperience",
    "EmployeeSkill",
    # Identity & Documents
    "EmployeeIdentifier",
    "EmployeeDocument",
)
