# Generated by Django 5.1 on 2024-08-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.IntegerField(default=1),
        ),
    ]
