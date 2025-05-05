from django.db.models.signals import pre_save
from django.dispatch import receiver
from taggit.models import Tag
from slugify import slugify

@receiver(pre_save, sender=Tag)
def set_tag_slug(sender, instance, **kwargs):
    if not instance.slug or slugify(instance.name) != instance.slug:
        instance.slug = slugify(instance.name)