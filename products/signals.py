from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import custom_slugify
from .models import ProductImage, Product


@receiver(pre_save, sender=ProductImage)
def set_main_image(sender, instance, **kwargs):
    """
    Ensures one main image per product.
    If none exist, set the first one as main by default.
    """
    if not instance.product_id:
        return

    if instance.is_main:
        with transaction.atomic():
            ProductImage.objects.filter(
                product=instance.product
            ).exclude(id=instance.id).update(is_main=False)

    else:
        existing_main = ProductImage.objects.filter(
            product=instance.product,
            is_main=True
        ).exclude(id=instance.id).exists()

        if not existing_main:
            instance.is_main = True

@receiver(pre_save, sender=Product)
def slug_validator(sender, instance, **kwargs):
    """Generates and validates a unique slug for Product instances before saving.

    If the product's slug is not set, this function generates a base slug using
    `custom_slugify` based on the product's name. It checks for existing slugs in
    the database, excluding the current instance if it already exists, and appends
    a numeric suffix to ensure uniqueness. The operation is performed within an
    atomic transaction to maintain data integrity during concurrent saves.

    Args:
        sender (Model): The model class sending the signal (Product).
        instance (Product): The Product instance being saved.
        **kwargs: Additional keyword arguments passed by the signal.

    Returns:
        None
    """
    if not instance.slug:
        instance.slug = custom_slugify(instance.name)

    with transaction.atomic():
        counter = 1
        original_slug = instance.slug
        while Product.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1