import admin_thumbnails
from django.contrib import admin

from home.models import Category, Product, Variants, Color, Size, PhotoGallery, Chart, SliderFirst


class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'sub_cat', 'sub_category']
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin_thumbnails.thumbnail('image')
class PhotoGalleryInline(admin.TabularInline):
    model = PhotoGallery
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'unit_price', 'discount', 'total_price', 'available']
    raw_id_fields = ('category',)
    inlines = [ProductVariantInlines, PhotoGalleryInline]
    # ------for chart in admin --------
    change_list_template = 'home/change.html'


@admin.register(Variants)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_variant', 'size_variant', 'color_variant', 'amount', 'unit_price', 'discount',
                    'total_price']


@admin.register(Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit_price', 'product', 'variant', 'update']


admin.site.register(Size)
admin.site.register(Color)
admin.site.register(SliderFirst)
