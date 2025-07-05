from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import transaction

from products.utils import custom_slugify
from .models import Category

@receiver(pre_save, sender=Category)
def slug_validator(sender, instance, **kwargs):
    """
    A Django signal that automatically generates a unique slug for a Category instance before saving.

    If the 'slug' field is empty, it uses a custom slugify function on the 'name' field to create one.
    Then, it checks for slug uniqueness in the database. If a conflict exists, it appends an incrementing
    number to the slug until a unique one is found.

    The entire uniqueness check is wrapped in an atomic transaction to prevent race conditions and ensure
    data consistency during concurrent saves.
    """
    if not instance.slug:
        instance.slug = custom_slugify(instance.name)

    with transaction.atomic():
        counter = 1
        original_slug = instance.slug
        while Category.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
