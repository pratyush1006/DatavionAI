# Employees App

The Employees app manages employee information within organizations.

## Overview

This app provides comprehensive employee management functionality including:

- Employee creation, retrieval, updating, and deletion (CRUD)
- Employee hierarchies with manager relationships
- Department and team associations
- Role-based access control
- Advanced search and filtering
- Pagination support

## Data Model

### Employee Model

The `Employee` model represents an employee within an organization.

**Fields:**

- `organization` (ForeignKey): The organization the employee belongs to
- `department` (ForeignKey): The department the employee works in
- `team` (ForeignKey): The team the employee is part of (optional)
- `user` (OneToOneField): Associated user account
- `employee_code` (CharField): Unique employee identifier per organization
- `designation` (CharField): Job title or designation
- `manager` (ForeignKey): Manager/supervisor (self-referential, optional)
- `hire_date` (DateField): Date employee was hired
- `is_active` (BooleanField): Whether the employee is active
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Record last update timestamp

**Constraints:**

- `unique_employee_code_per_organization`: Employee code must be unique within an organization

## API Endpoints

### List/Create Employees

```
GET    /api/employees/              - List all employees
POST   /api/employees/              - Create a new employee
```

**Query Parameters:**

- `search`: Search by employee code, first name, last name, email, or designation
- `ordering`: Sort by employee_code, hire_date, or created_at
- `organization`: Filter by organization ID
- `department`: Filter by department ID
- `team`: Filter by team ID
- `designation`: Filter by designation
- `is_active`: Filter by active status

**Example Request:**

```bash
GET /api/employees/?search=EMP001&ordering=employee_code
```

### Retrieve/Update/Delete Employee

```
GET    /api/employees/<id>/        - Get employee details
PUT    /api/employees/<id>/        - Replace employee data
PATCH  /api/employees/<id>/        - Partial update
DELETE /api/employees/<id>/        - Delete employee
```

## Permissions

The following permission codes control access:

- `employee.view`: View employee records
- `employee.create`: Create new employees
- `employee.update`: Update employee information
- `employee.delete`: Delete employees

## Services

### create_employee(validated_data)

Creates a new employee with business rule validation.

```python
from apps.employees.services import create_employee

employee = create_employee(
    validated_data={
        'organization': org,
        'department': dept,
        'user': user,
        'employee_code': 'EMP001',
        'designation': 'Software Engineer',
        'hire_date': '2023-01-01',
    }
)
```

### update_employee(instance, validated_data)

Updates an existing employee.

```python
from apps.employees.services import update_employee

employee = update_employee(
    instance=employee,
    validated_data={'designation': 'Senior Engineer'}
)
```

### delete_employee(instance)

Deletes an employee.

```python
from apps.employees.services import delete_employee

delete_employee(instance=employee)
```

## Selectors

### get_employees()

Returns all employees with optimized queries (select_related on related objects).

```python
from apps.employees.selectors import get_employees

employees = get_employees()
```

### get_employee_by_id(employee_id)

Retrieve a specific employee by ID.

```python
from apps.employees.selectors import get_employee_by_id

employee = get_employee_by_id(employee_id=1)
```

## Serializers

### EmployeeListSerializer

Used for list view responses. Includes basic employee info and related names.

### EmployeeDetailSerializer

Used for detail view responses. Includes comprehensive employee information including IDs.

### EmployeeCreateSerializer

Used for creating new employees. Requires organization, department, user, employee_code, designation, and hire_date.

### EmployeeUpdateSerializer

Used for updating employees. Allows updating designation, manager, hire_date, and active status.

## Testing

Run employee tests:

```bash
pytest apps/employees/tests/
```

### Test Coverage

- **Model Tests**: Employee creation, relationships, and constraints
- **Service Tests**: CRUD operations and business rule validation
- **API Tests**: Endpoint functionality and permission checks

## Business Rules

1. **Employee Code Uniqueness**: Each employee code must be unique within its organization
2. **Department Belonging**: Selected department must belong to the selected organization
3. **Team Belonging**: If a team is selected, it must belong to the selected department
4. **Manager Organization**: Manager must belong to the same organization
5. **User Organization**: If applicable, the user must belong to the same organization

## Performance

The selectors use `select_related` to optimize database queries:

- `user`: Employee's user account
- `organization`: Organization data
- `department`: Department data
- `team`: Team data
- `manager`: Manager employee data
- `manager__user`: Manager's user account

## Example Usage

### Create Employee

```bash
curl -X POST http://localhost:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "organization": 1,
    "department": 1,
    "team": 1,
    "user": 2,
    "employee_code": "EMP001",
    "designation": "Software Engineer",
    "hire_date": "2023-01-01",
    "is_active": true
  }'
```

### List Employees

```bash
curl -X GET "http://localhost:8000/api/employees/?search=EMP&ordering=employee_code" \
  -H "Authorization: Bearer <token>"
```

### Get Employee Details

```bash
curl -X GET http://localhost:8000/api/employees/1/ \
  -H "Authorization: Bearer <token>"
```

### Update Employee

```bash
curl -X PATCH http://localhost:8000/api/employees/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"designation": "Senior Software Engineer"}'
```

### Delete Employee

```bash
curl -X DELETE http://localhost:8000/api/employees/1/ \
  -H "Authorization: Bearer <token>"
```
