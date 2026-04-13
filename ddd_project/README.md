# DDD Order Management API

A Django + Django Ninja project demonstrating Domain-Driven Design patterns.

## Project Structure

```
ddd_project/
├── apps/
│   ├── domain/           # Domain Layer (innermost)
│   │   ├── entities/    # Order, Customer, OrderItem
│   │   ├── value_objects/  # Money, Address, OrderStatus, Quantity
│   │   └── repositories/  # Interfaces (abstractions)
│   ├── application/    # Application Layer
│   │   ├── dtos/      # Data Transfer Objects
│   ├── mappers/       # Entity <-> DTO converters
│   │   └── services/ # Use cases
│   ├── infrastructure # Infrastructure Layer (outermost)
│   │   ├── persistence/  # Django ORM models
│   │   └── repositories/  # Repository implementations
│   └── presentation   # Presentation Layer
│       ├── api/      # Django Ninja endpoints
│       └── handlers/ # Exception handlers
├── core/
│   ├── di/          # Dependency injection
│   └── exceptions/  # Domain exceptions
└── config/         # Django settings
```

## DDD Patterns Demonstrated

| Pattern | Location | Description |
|---------|----------|-------------|
| **Entities** | `domain/entities/` | Objects with identity (Order, Customer) |
| **Value Objects** | `domain/value_objects/` | Immutable, equality by value (Money, Address) |
| **Aggregate** | `domain/entities/order.py` | Root entity controlling consistency |
| **Repository Interface** | `domain/repositories/` | Abstract persistence contract |
| **Repository Implementation** | `infrastructure/repositories/` | Concrete persistence |
| **DTOs** | `application/dtos/` | API data transfer objects |
| **Mappers** | `application/mappers/` | Entity <-> DTO conversion |
| **Services** | `application/services/` | Use case orchestration |
| **Dependency Injection** | `core/di/` |Factory functions for DI |

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install django djangoninja pydantic

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
```

## API Endpoints

- `POST /api/orders` - Create order
- `GET /api/orders/{id}` - Get order
- `GET /api/orders` - List orders
- `PATCH /api/orders/{id}/status` - Update status
- `POST /api/orders/{id}/confirm` - Confirm order
- `POST /api/orders/{id}/cancel` - Cancel order
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer
- `GET /api/customers` - List customers

## Example Usage

```python
# Create an order
import requests

order_data = {
    "items": [
        {"product_name": "Widget", "unit_price": 9.99, "quantity": 2}
    ],
    "shipping_address": "123 Main St, Anytown, USA"
}

response = requests.post("http://localhost:8000/api/orders", json=order_data)
print(response.json())
```

## Key DDD Concepts for Teaching

1. **Layered Architecture**: Domain is innermost - no dependencies on outer layers
2. **Entities vs Value Objects**: Identity vs equality by value
3. **Repository Pattern**:Abstraction over persistence
4. **DTOs**: Decouple API from domain
5. **Mappers**: Single responsibility conversion
6. **Services**: Orchestrate use cases
7. **Dependency Injection**: Loose coupling via interfaces