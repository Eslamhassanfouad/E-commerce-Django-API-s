# Generated by Django 4.2.2 on 2023-06-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='product_number',
            new_name='product_quantity',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
