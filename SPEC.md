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