import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    # ----------------------------------------------------side filter------------------------------------
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    # brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
    color = django_filters.ModelMultipleChoiceFilter(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
    # name of field must be same as model field
    # ----------------------------------------------------top filter------------------------------------
    # ------for cheapest and most expensive-------
    choice_1 = {
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }
    price = django_filters.ChoiceFilter(choices=choice_1, method='price_filter')

    def price_filter(self, queryset, name, value):
        # order of input values is important in these functions
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    # ------for newest-------
    choice_2 = {
        ('جدیدترین', 'جدیدترین'),
        ('قدیمی ترین', 'قدیمی ترین'),
    }
    create = django_filters.ChoiceFilter(choices=choice_2, method='create_filter')

    def create_filter(self, queryset, name, value):
        data = 'create' if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)

    # ------for more discount-------
    choice_3 = {
        ('بیشترین تخفیف', 'بیشترین تخفیف'),
        ('کمترین تخفیف', 'کمترین تخفیف'),
    }
    discount = django_filters.ChoiceFilter(choices=choice_3, method='discount_filter')

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 'کمترین تخفیف' else '-discount'
        return queryset.order_by(data)

    # ------for best seller-------
    choice_4 = {
        ('پرفروش ترین', 'پرفروش ترین'),
        ('کم فروش ترین', 'کم فروش ترین'),
    }
    sell = django_filters.ChoiceFilter(choices=choice_4, method='sell_filter')

    def sell_filter(self, queryset, name, value):
        data = 'sell' if value == 'کم فروش ترین' else '-sell'
        return queryset.order_by(data)

    # ------for favorite-------
    choice_5 = {
        ('محبوب ترین', 'محبوب ترین'),
        ('کم طرفدار', 'کم طرفدار'),
    }
    favorite = django_filters.ChoiceFilter(choices=choice_5, method='favorite_filter')

    def favorite_filter(self, queryset, name, value):
        data = 'total_favorites' if value == 'کم طرفدار' else '-total_favorites'
        return queryset.order_by(data)
