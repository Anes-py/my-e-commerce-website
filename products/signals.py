from django.db import transaction
from django.db.models.signals import pre_save
from django.dispatch import receiver


from .utils import custom_slugify
from .models import ProductImage, Product

@receiver(pre_save, sender=ProductImage)
def set_main_image(sender, instance, **kwargs):
    if instance.is_main:
        ProductImage.objects.filter(product=instance.product).\
            exclude(id=instance.id).update(is_main=False)

@receiver(pre_save, sender=Product)
def slug_validator(sender, instance, **kwargs):
        if not instance.slug:
            instance.slug = custom_slugify(instance.name)
        with transaction.atomic():
            counter = 1
            while Product.objects.filter(slug=instance.slug).exists():
                instance.slug = f"{instance.slug}-{counter}"
                counter += 1
