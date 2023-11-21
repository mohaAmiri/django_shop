from django.shortcuts import render, get_object_or_404

from home.models import Category, Product


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
    context = {'product': product}
    return render(request, 'home/detail.html', context)
