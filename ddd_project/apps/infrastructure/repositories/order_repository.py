"""Order Repository - Django implementation"""
from typing import Optional
from uuid import UUID

from ddd_project.apps.domain.entities import Order, OrderItem
from ddd_project.apps.domain.repositories import OrderRepository
from ddd_project.apps.domain.value_objects import Money, OrderStatus, Quantity
from ddd_project.apps.infrastructure.persistence import OrderModel, OrderItemModel


class DjangoOrderRepository(OrderRepository):
    """Implements OrderRepository using Django ORM.
    
    Repository Implementation Principles:
    - Implements domain interface
    - Handles persistence details
    - Maps between ORM and domain entities
    - Single responsibility for persistence
    """

    def save(self, order: Order) -> Order:
        order_model, _ = OrderModel.objects.update_or_create(
            id=order.id,
            defaults={
                "customer_id": order.customer_id,
                "status": str(order.status),
                "shipping_address": order.shipping_address,
                "notes": order.notes,
            }
        )

        OrderItemModel.objects.filter(order=order_model).delete()
        for item in order.items:
            OrderItemModel.objects.create(
                id=item.id,
                order=order_model,
                product_name=item.product_name,
                unit_price=item.unit_price.amount,
                quantity=item.quantity.value,
            )

        return order

    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        try:
            order_model = OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return None

        return self._to_domain(order_model)

    def find_all(self) -> list[Order]:
        return [
            self._to_domain(order_model)
            for order_model in OrderModel.objects.all()
        ]

    def delete(self, order_id: UUID) -> bool:
        try:
            OrderModel.objects.get(id=order_id).delete()
            return True
        except OrderModel.DoesNotExist:
            return False

    def _to_domain(self, order_model: OrderModel) -> Order:
        order = Order()
        order.id = order_model.id
        order.customer_id = order_model.customer_id
        order.status = OrderStatus.from_string(order_model.status)
        order.shipping_address = order_model.shipping_address
        order.notes = order_model.notes
        order.created_at = order_model.created_at
        order.updated_at = order_model.updated_at

        for item_model in order_model.items.all():
            item = OrderItem(
                id=item_model.id,
                product_name=item_model.product_name,
                unit_price=Money.create(float(item_model.unit_price), "USD"),
                quantity=Quantity.create(item_model.quantity),
            )
            order.items.append(item)

        return order