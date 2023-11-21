from django.contrib import admin

from home.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'sub_cat', 'sub_category']
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'unit_price', 'discount', 'total_price', 'available']
    raw_id_fields = ('category',)
