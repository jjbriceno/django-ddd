"""Customer Repository - Django implementation"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.entities import Customer
from ddd_project.apps.domain.repositories import CustomerRepository
from ddd_project.apps.domain.value_objects import Address
from ddd_project.apps.infrastructure.persistence import CustomerModel


class DjangoCustomerRepository(CustomerRepository):
    """Implements CustomerRepository using Django ORM."""

    def save(self, customer: Customer) -> Customer:
        customer_model, _ = CustomerModel.objects.update_or_create(
            id=customer.id,
            defaults={
                "name": customer.name,
                "email": customer.email,
                "street": customer.address.street if customer.address else "",
                "city": customer.address.city if customer.address else "",
                "state": customer.address.state if customer.address else "",
                "postal_code": customer.address.postal_code if customer.address else "",
                "country": customer.address.country if customer.address else "",
                "is_active": customer.is_active,
            }
        )
        return customer

    def find_by_id(self, customer_id: UUID) -> Optional[Customer]:
        try:
            customer_model = CustomerModel.objects.get(id=customer_id)
        except CustomerModel.DoesNotExist:
            return None

        return self._to_domain(customer_model)

    def find_all(self) -> list[Customer]:
        return [
            self._to_domain(model)
            for model in CustomerModel.objects.all()
        ]

    def delete(self, customer_id: UUID) -> bool:
        try:
            CustomerModel.objects.get(id=customer_id).delete()
            return True
        except CustomerModel.DoesNotExist:
            return False

    def _to_domain(self, model: CustomerModel) -> Customer:
        customer = Customer()
        customer.id = model.id
        customer.name = model.name
        customer.email = model.email
        customer.is_active = model.is_active
        customer.created_at = model.created_at
        customer.updated_at = model.updated_at

        if model.street:
            customer.address = Address.create(
                street=model.street,
                city=model.city,
                state=model.state,
                postal_code=model.postal_code,
                country=model.country,
            )

        return customer