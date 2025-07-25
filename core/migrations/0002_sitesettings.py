# Generated by Django 5.2.4 on 2025-07-04 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=155, verbose_name='site name')),
                ('footer_text', models.CharField(blank=True, max_length=155, verbose_name='footer text')),
                ('footer_contact_phone', models.CharField(blank=True, max_length=55, verbose_name='footer contact phone')),
                ('footer_contact_text', models.CharField(blank=True, max_length=155, verbose_name='footer contact text')),
                ('footer_github_link', models.URLField(blank=True, max_length=100, verbose_name='footer github link')),
                ('footer_telegram_link', models.URLField(blank=True, max_length=100, verbose_name='footer telegram link')),
                ('footer_linkedin_link', models.URLField(blank=True, max_length=100, verbose_name='footer linkedin link')),
                ('footer_instagram_link', models.URLField(blank=True, max_length=100, verbose_name='footer instagram link')),
            ],
        ),
    ]
