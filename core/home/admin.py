from django.contrib import admin

from home.models import Category, Product, Variants, Color, Size


class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2


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
    inlines = [ProductVariantInlines]


@admin.register(Variants)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_variant', 'size_variant', 'color_variant', 'amount', 'unit_price', 'discount',
                    'total_price']


admin.site.register(Size)
admin.site.register(Color)
