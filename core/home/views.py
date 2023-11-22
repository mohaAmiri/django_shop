from django.shortcuts import render, get_object_or_404

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
    if product.status is not None:
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            selected_variant = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            selected_variant = Variants.objects.get(id=variant[0].id)
        context = {'product': product, 'variant': variant, 'selected_variant': selected_variant}
        return render(request, 'home/detail.html', context)
    else:
        context = {'product': product}
        print(product.status)
        return render(request, 'home/detail.html', context)
