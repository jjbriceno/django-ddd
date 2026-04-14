from django.contrib import admin
from .persistence.customer_model import CustomerModel
from .persistence.order_model import OrderModel, OrderItemModel


@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "email"]


class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0
    readonly_fields = ["id"]


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_id", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["id"]
    inlines = [OrderItemInline]