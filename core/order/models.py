from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django_jalali.db import models as jmodel
from home.models import Product, Variants


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = jmodel.jDateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    code = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    f_name = models.CharField(max_length=300)
    l_name = models.CharField(max_length=300)
    address = models.CharField(max_length=1000)
    # ----------------------------discount system------------------
    discount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارشات'

    def order_price(self):
        total = sum(i.price() for i in self.order_sub.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int(total - discount_price)
        return total


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_sub')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username

    def size(self):
        return self.variant.size_variant.name

    def color(self):
        return self.variant.color_variant.name

    def price(self):
        if self.product.status is not None:
            return self.variant.total_price * self.quantity
        else:
            return self.product.total_price * self.quantity

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'خریداری شده'
        verbose_name_plural = 'خریداری شده'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'f_name', 'l_name', 'address']


class Coupon(models.Model):
    code = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    start = jmodel.jDateTimeField()
    end = jmodel.jDateTimeField()
    discount = models.IntegerField()

    def __str__(self):
        return self.code

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'کد نخفیف'
        verbose_name_plural = 'کد تخفیف'
