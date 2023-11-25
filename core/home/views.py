from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from home.models import Category, Product, Variants


def home(request):
    category = Category.objects.filter(sub_cat=False)
    return render(request, 'home/home.html', {'category': category})


def all_products(request, slug=None, id=None):
    products = Product.objects.filter(available=True)
    category = Category.objects.filter(sub_cat=False)
    if slug and id:
        selected_cat = get_object_or_404(Category, slug=slug, id=id)
        products = Product.objects.filter(category=selected_cat, available=True)
    return render(request, 'home/products.html', {'products': products, 'category': category, })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    # --------------------------similar object---------------------
    similar = product.tags.similar_objects()[:2]
    # ------------------------------like---------------------------
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    # --------------------------------------------------------------
    if product.status is not None:
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            selected_variant = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            selected_variant = Variants.objects.get(id=variant[0].id)
        context = {'product': product, 'variant': variant, 'selected_variant': selected_variant, 'similar': similar,
                   'is_like': is_like, 'is_unlike': is_unlike}
        return render(request, 'home/detail.html', context)
    else:
        context = {'product': product, 'similar': similar, 'is_like': is_like, 'is_unlike': is_unlike}
        return render(request, 'home/detail.html', context)


def product_like(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
        is_like = False
        messages.success(request, 'لایک پس گرفته شد', 'warning')
    else:
        product.like.add(request.user)
        is_like = True
        messages.success(request, 'لایک شد', 'success')
    return redirect(url)


def product_unlike(request, id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=id)
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
        is_unlike = False
    else:
        product.unlike.add(request.user)
        is_unlike = True
    return redirect(url)
