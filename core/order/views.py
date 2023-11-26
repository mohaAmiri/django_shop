from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
import datetime
from cart.models import Cart
from order.forms import CouponForm
from order.models import Order, OrderForm, ItemOrder, Coupon


def order_detail(request, id):
    order = Order.objects.get(id=id)
    # ---------------discount system----------------
    form = CouponForm()
    # ----------------------------------------------
    return render(request, 'order/order.html', {'order': order, 'form': form})


def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            code = get_random_string(length=8)
            order = Order.objects.create(user_id=request.user.id, email=data['email'], f_name=data['f_name'],
                                         l_name=data['l_name'], address=data['address'], code=code)
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id,
                                         variant_id=c.variant_id, quantity=c.quantity)
            Cart.objects.filter(user_id=request.user.id).delete()
            return redirect('order:order-detail', order.id)


@require_POST
def coupon_order(request, id):
    form = CouponForm(request.POST)
    time = datetime.datetime.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'کد اشتباه است یا در بازه زمانی مشخص شده وارد نشده است', 'danger')
            return redirect('order:order-detail', id)
        order = Order.objects.get(id=id)
        order.discount = coupon.discount
        order.save()
        coupon.active = False
    return redirect('order:order-detail', id)
