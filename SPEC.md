# DDD Order Management API - Specification

## Project Overview
- **Project name**: DDD Order Management API
- **Type**: Django + Django Ninja REST API
- **Core functionality**: Order management system demonstrating DDD patterns
- **Target users**: Development team learning DDD

## Domain: Order Management

### Bounded Contexts
1. **Order Context** - Core domain for order operations
2. **Customer Context** - Customer management

## DDD Patterns to Demonstrate

### Entities
- `Order` - Aggregate root with identity
- `OrderItem` - Entity within order aggregate
- `Customer` - Entity

### Value Objects
- `Money` - Immutable value type with currency
- `Address` - Immutable postal address
- `OrderStatus` - Enum-like value object
- `Quantity` - Positive integer value object

### DTOs
- `OrderCreateDTO` - Input for creating orders
- `OrderResponseDTO` - Output for order data
- `OrderItemDTO` - Order item data

### Mappers
- `OrderMapper` - Maps between domain entities and DTOs
- Maps to/from persistence models

### Dependency Injection
- Use Django Ninja's dependency injection
- Repository pattern with interfaces

### Error Handling
- Custom exception classes
- Global exception handler
- Proper HTTP error responses

### Layered Architecture
1. **Presentation Layer** - API endpoints
2. **Application Layer** - Use cases, DTOs, mappers
3. **Domain Layer** - Entities, Value Objects, Repository interfaces
4. **Infrastructure Layer** - Repository implementations, persistence

## API Endpoints

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders/{id}` - Get order by ID
- `GET /api/orders` - List all orders
- `PATCH /api/orders/{id}/status` - Update order status

### Customers
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer by ID

## Technology Stack
- Django 4.2+
- Django Ninja (djangoninja)
- SQLite (for simplicity)
- Python 3.10+

## Project Structure (DDD-aligned)

```
domain_driven_design/
├── apps/
│   ├── domain/           # Domain Layer
│   │   ├── entities/
│   │   ├── value_objects/
│   │   └── repositories/  # Interfaces
│   ├── application/       # Application Layer
│   │   ├── dtos/
│   │   ├── mappers/
│   │   └── services/
│   ├── infrastructure    # Infrastructure Layer
│   │   ├── persistence/
│   │   └── repositories/
│   └── presentation      # Presentation Layer
│       ├── api/
│       └── handlers/
├── core/
│   ├── exceptions/
│   └── di/
├── config/
└── manage.py
```

## Acceptance Criteria
1. All DDD patterns clearly visible in code
2. Entities with proper identity and equality
3. Value objects as immutable types
4. DTOs separate API from domain
5. Mappers handle conversion
6. Repository pattern with dependency injection
7. Proper error handling with custom exceptions
8. Layered architecture enforced
9. Code is readable and educational
10. Tests demonstrate usage patterns

## Testing

The project includes comprehensive tests demonstrating DDD testing patterns across all layers.

### Test Structure

```
ddd_project/tests/
├── conftest.py                 # Shared fixtures (mocks, factories)
├── domain/                     # Domain Layer Tests (158 total)
│   ├── test_money.py          # Value object tests
│   ├── test_address.py
│   ├── test_order_status.py
│   ├── test_quantity.py
│   ├── test_order.py          # Aggregate root tests
│   ├── test_order_item.py
│   └── test_customer.py
├── application/                # Application Layer Tests
│   ├── test_create_order.py
│   ├── test_get_order.py
│   ├── test_list_orders.py
│   ├── test_confirm_order.py
│   ├── test_cancel_order.py
│   └── test_customer_use_cases.py
└── infrastructure/             # Infrastructure Layer Tests
    ├── test_order_repository.py
    └── test_customer_repository.py
```

### Testing Principles by Layer

| Layer | Test Type | Description | Dependencies |
|-------|-----------|-------------|--------------|
| **Domain** | Unit Tests | Pure tests, no external dependencies | None |
| **Application** | Use Case Tests | Test with mocked repositories | Mock repositories |
| **Infrastructure** | Integration Tests | Test with actual Django ORM | SQLite test database |

### Domain Layer Testing
- **Pure unit tests** with no external dependencies
- Test value object creation, validation, and immutability
- Test entity business rules and state transitions
- Test aggregate invariants and domain exceptions

### Application Layer Testing
- **Mock repositories** for testing use cases in isolation
- Test correct repository calls with expected parameters
- Test DTO transformation
- Verify business logic in use cases

### Infrastructure Layer Testing
- **pytest-django** with `@pytest.mark.django_db`
- In-memory SQLite database for tests
- Test persistence mapping between domain and ORM
- Test CRUD operations

### Running Tests

```bash
cd ddd_project
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=/home/jorge/Proyectos/django-ddd python -m pytest tests/ -v
```

### Test Dependencies
- `pytest>=8.0`
- `pytest-django>=4.8`
- `pytest-cov>=4.1`
- `email-validator` (for Pydantic EmailStr)

### Test Coverage Highlights

**Value Objects**: 100% coverage of validation, operations, and immutability

**Entities**: Tests for:
- Creation and initialization
- Business rule enforcement
- Status transitions
- Aggregate invariants

**Use Cases**: Tests for:
- Successful execution paths
- Error handling (not found, validation errors)
- Repository interaction verification

**Repositories**: Tests for:
- CRUD operations
- Domain-to-ORM mapping
- Data integrity preservation