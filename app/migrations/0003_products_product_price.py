# Generated by Django 4.2.2 on 2023-06-26 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_user_user_image_alter_products_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]