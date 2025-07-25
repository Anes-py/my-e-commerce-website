# Generated by Django 5.2.4 on 2025-07-13 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_product_brand_alter_featureoption_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, help_text='It is preferable to leave this field blank so that it will be filled in automatically.', max_length=255, unique=True, verbose_name='slug'),
        ),
    ]
