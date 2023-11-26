from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from cart.models import CartForm
from home.forms import SearchForm
from home.models import Category, Product, Variants, Comment, ReplyForm, CommentForm, PhotoGallery


def home(request):
    category = Category.objects.filter(sub_cat=False)
    return render(request, 'home/home.html', {'category': category})


def all_products(request, slug=None, id=None):
    page_object = Product.objects.filter(available=True)  # products
    category = Category.objects.filter(sub_cat=False)
    # --------------------search with get------------------------------
    if 'search' in request.GET:
        form = SearchForm(request.GET, use_required_attribute=False)
        if form.is_valid():
            data_search = form.cleaned_data['search']
            page_object = Product.objects.filter(Q(name__icontains=data_search) | Q(information__icontains=data_search))
    # ----------------------------------------------------------------------
    if slug and id:
        selected_cat = get_object_or_404(Category, slug=slug, id=id)
        page_object = Product.objects.filter(category=selected_cat, available=True)
    return render(request, 'home/products.html', {'products': page_object, 'category': category})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    # --------------------------similar object---------------------
    similar = product.tags.similar_objects()[:2]
    # -----------------------------photo gallery---------------------
    gallery = PhotoGallery.objects.filter(product_id=id)
    # ------------------------------like---------------------------
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True

    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True
    # --------------------------------cart----------------------------
    cart_form = CartForm()
    # --------------------------------comment-------------------------
    comment_form = CommentForm()
    comments = Comment.objects.filter(product_id=id, is_reply=False)
    reply_form = ReplyForm()
    # -----------------------------favorite section---------------------------
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    if product.status is not None:
        if request.method == 'POST':
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            selected_variant = Variants.objects.get(id=var_id)
        else:
            variant = Variants.objects.filter(product_variant_id=id)
            selected_variant = Variants.objects.get(id=variant[0].id)
        context = {'product': product, 'variant': variant, 'selected_variant': selected_variant, 'similar': similar,
                   'is_like': is_like, 'is_unlike': is_unlike, 'comment_form': comment_form, 'comments': comments,
                   'reply_form': reply_form, 'gallery': gallery, 'cartForm': cart_form, 'is_favorite': is_favorite}
        return render(request, 'home/detail.html', context)
    else:
        context = {'product': product, 'similar': similar, 'is_like': is_like, 'is_unlike': is_unlike,
                   'comment_form': comment_form, 'comments': comments, 'reply_form': reply_form, 'gallery': gallery,
                   'cartForm': cart_form, 'is_favorite': is_favorite}
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


def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], rate=data['rate'], user_id=request.user.id, product_id=id)
            return redirect(url)
        else:
            return redirect(url)


def reply_comment(request, id, comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, product_id=id,
                                   reply_id=comment_id, is_reply=True)
            return redirect(url)
        else:
            return redirect(url)


def comment_like(request, id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)
    return redirect(url)


def search_product(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = Product.objects.filter(Q(unit_price__exact=data) | Q(discount__exact=data))
            else:
                products = Product.objects.filter(Q(name__icontains=data) | Q(information__icontains=data))
            return render(request, 'home/products.html', {'products': products, 'form': form})


def favorite(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)
        product.total_favorites -= 1
        product.save()
        is_favorite = False
    else:
        product.favorite.add(request.user)
        product.total_favorites += 1
        product.save()
        is_favorite = True
    return redirect(url)
