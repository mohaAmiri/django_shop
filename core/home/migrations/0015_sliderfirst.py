# Generated by Django 4.2.3 on 2023-11-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_chart_options_product_num_view_product_view_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderFirst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='slider')),
            ],
        ),
    ]