from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.forms import ModelForm
from django.urls import reverse
from taggit.managers import TaggableManager
from django_jalali.db import models as jmodel
from django.dispatch import receiver


class Category(models.Model):
    # ------for sub category--------------
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    sub_cat = models.BooleanField(default=False)
    # ---------------------------------------
    name = models.CharField(max_length=200, verbose_name='اسم')
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='category', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id])

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    VARIANT = (
        ('Size', 'size'),
        ('Color', 'color'),
        ('Both', 'Both'),
    )
    category = models.ManyToManyField(Category, blank=True, verbose_name='دسته بندی')
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    change = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    create = jmodel.jDateTimeField(auto_now_add=True)
    update = jmodel.jDateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products')
    available = models.BooleanField(default=True)
    status = models.CharField(null=True, blank=True, max_length=200, choices=VARIANT)
    # ---------------------similar object------------------------
    tags = TaggableManager(blank=True)
    # --------------like----------------------
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)
    # --------------------- for favorites -------------------------
    favorite = models.ManyToManyField(User, blank=True, related_name='fa_user')
    total_favorites = models.IntegerField(default=0)
    # --------------------- for filters ----------------------
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
    size = models.ManyToManyField('Size', blank=True)
    color = models.ManyToManyField('Color', blank=True)
    sell = models.IntegerField(default=0)
    # -------------------------count visits--------------------------------
    view = models.ManyToManyField(User, blank=True, related_name='product_view')
    num_view = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    # ---------------aggregate > for average of rates------------------

    def average(self):
        data = Comment.objects.filter(is_reply=False, product=self).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'محصولات'
        verbose_name_plural = 'محصولات'


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز'


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ'


class Variants(models.Model):
    name = models.CharField(max_length=100)
    update = jmodel.jDateTimeField(auto_now=True)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name_plural = 'Variants'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = jmodel.jDateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply_sub')
    is_reply = models.BooleanField(default=False)
    # ------------------like comment----------------
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like')
    total_like = models.PositiveIntegerField(default=0)

    def total_like(self):
        return self.comment_like.count()

    def __str__(self):
        return self.product.name

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class PhotoGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='gallery', blank=True, null=True)

    # ------------------------change name of app in admin-------------------------
    class Meta:
        verbose_name = 'گالری تصاویر'
        verbose_name_plural = 'گالری تصاویر'


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.IntegerField(default=0)
    update = jmodel.jDateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr_update', blank=True, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, related_name='v_update', blank=True, null=True)

    # ***add update with jalali to variant and product models

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'نمودار قیمت'
        verbose_name_plural = 'نمودار قیمت'


@receiver(post_save, sender=Product)
def product_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    if data.change is True:
        Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update, name=data.name)
        data.change = False
        data.save()


@receiver(post_save, sender=Variants)
def variant_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    Chart.objects.create(variant=data, unit_price=data.unit_price, update=data.update, name=data.name,
                         size=data.size_variant, color=data.color_variant)


class Views(models.Model):
    ip = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
