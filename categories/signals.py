from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction

from products.utils import custom_slugify
from .models import Category

@receiver(pre_save, sender=Category)
def slug_validator(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = custom_slugify(instance.name)

    with transaction.atomic():
        counter = 1
        while Category.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{instance.slug}-{counter}"
            counter += 1
