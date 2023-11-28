from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter

from order.models import ItemOrder, Order, Coupon


class OrderItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user', 'product', 'variant', 'size', 'quantity', 'price']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user', 'email', 'f_name', 'l_name', 'order_price', 'paid', 'code']
    inlines = [OrderItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'start', 'end', 'active']
    # -------------for persian date-------------------
    list_filter = (
        ('start', JDateFieldListFilter),
    )
