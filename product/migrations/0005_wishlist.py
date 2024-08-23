# Generated by Django 5.1 on 2024-08-23 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('state', models.IntegerField(default=1)),
                ('user_id', models.BigIntegerField()),
                ('product_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'wishlist',
            },
        ),
    ]
