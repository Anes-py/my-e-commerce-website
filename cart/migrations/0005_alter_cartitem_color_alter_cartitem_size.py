# Generated by Django 5.2.4 on 2025-07-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cartitem_feature_option_cartitem_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='color',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.CharField(blank=True, max_length=55, null=True, verbose_name='size'),
        ),
    ]
