# Generated by Django 4.2.3 on 2023-11-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_product_favorite_product_total_favorites'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name': 'رنگ', 'verbose_name_plural': 'رنگ'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'کامنت', 'verbose_name_plural': 'کامنت ها'},
        ),
        migrations.AlterModelOptions(
            name='photogallery',
            options={'verbose_name': 'گالری تصاویر', 'verbose_name_plural': 'گالری تصاویر'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'محصولات', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name': 'سایز', 'verbose_name_plural': 'سایز'},
        ),
        migrations.AlterModelOptions(
            name='variants',
            options={'verbose_name_plural': 'Variants'},
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, to='home.category', verbose_name='دسته بندی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='نام محصول'),
        ),
    ]
