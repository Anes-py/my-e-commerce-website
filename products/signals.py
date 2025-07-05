from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import custom_slugify
from .models import ProductImage, Product


@receiver(pre_save, sender=ProductImage)
def set_main_image(sender, instance, **kwargs):
    """
    Ensures that only one ProductImage per product is marked as the main image.

    Before saving a ProductImage instance, if `is_main` is set to True,
    this function sets `is_main=False` for all other images of the same product.
    """
    if instance.is_main:
        ProductImage.objects.filter(product=instance.product).\
            exclude(id=instance.id).update(is_main=False)


@receiver(pre_save, sender=Product)
def slug_validator(sender, instance, **kwargs):
    """
    Auto-generates a unique slug for Product instances before saving.

    If the slug is not already set, this function uses `custom_slugify` to generate
    a base slug from the product's name. It then checks for slug conflicts in the database
    and appends a counter to ensure uniqueness.

    Uses an atomic transaction to ensure data integrity in concurrent save operations.
    """
    if not instance.slug:
        instance.slug = custom_slugify(instance.name)

    with transaction.atomic():
        counter = 1
        original_slug = instance.slug
        while Product.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
