# Generated by Django 4.2.3 on 2023-11-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_brand_product_color_product_size_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell',
            field=models.IntegerField(default=0),
        ),
    ]
