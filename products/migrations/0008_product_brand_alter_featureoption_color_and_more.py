# Generated by Django 5.2.4 on 2025-07-12 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_brand'),
        ('products', '0007_featureoption_color_alter_discount_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_products', to='categories.brand', verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='featureoption',
            name='color',
            field=models.CharField(blank=True, choices=[('red', 'قرمز'), ('blue', 'آبی'), ('green', 'سبز'), ('black', 'مشکی'), ('white', 'سفید'), ('yellow', 'زرد'), ('orange', 'نارنجی'), ('purple', 'بنفش'), ('pink', 'صورتی'), ('brown', 'قهوه\u200cای'), ('gray', 'خاکستری'), ('silver', 'نقره\u200cای'), ('gold', 'طلایی'), ('beige', 'بژ'), ('maroon', 'زرشکی'), ('navy', 'سرمه\u200cای'), ('teal', 'سبز آبی'), ('turquoise', 'فیروزه\u200cای'), ('cyan', 'آبی روشن'), ('magenta', 'ارغوانی'), ('lime', 'سبز لیمویی'), ('olive', 'زیتونی'), ('indigo', 'نیلی'), ('violet', 'بنفش روشن'), ('coral', 'مرجانی'), ('salmon', 'صورتی سالمونی'), ('khaki', 'کاکی'), ('mint', 'نعنایی'), ('peach', 'هلوئی'), ('ivory', 'عاجی'), ('lavender', 'اسطوخودوسی')], help_text='If this feature is a color, fill this field and leave the value field empty.', max_length=10, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='featureoption',
            name='value',
            field=models.CharField(blank=True, help_text='If this feature is a size, fill this field and leave the color field empty.', max_length=55, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_products', to='categories.category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discount_products', to='products.discount', verbose_name='discount'),
        ),
    ]
