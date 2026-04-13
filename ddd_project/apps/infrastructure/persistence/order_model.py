"""Order Model - Django ORM persistence model"""
import uuid
from django.db import models


class OrderItemModel(models.Model):
    """Django ORM model for OrderItem persistence."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(
        "OrderModel",
        on_delete=models.CASCADE,
        related_name="items"
    )

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


class OrderModel(models.Model):
    """Django ORM model for Order persistence.
    
    Infrastructure Principles:
    - Django ORM for persistence
    - Maps to database schema
    - Separate from domain entity
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.UUIDField(null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order {self.id} - {self.status}"