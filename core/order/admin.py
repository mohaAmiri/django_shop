from django.contrib import admin

from order.models import ItemOrder, Order


class OrderItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user', 'product', 'variant', 'size', 'quantity', 'price']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user', 'email', 'f_name', 'l_name', 'order_price', 'paid', 'code']
    inlines = [OrderItemInline]
