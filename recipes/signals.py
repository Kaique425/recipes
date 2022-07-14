import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Recipe


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError) as e:
        ...


@receiver(pre_delete, sender=Recipe)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk)

    if old_instance:
        return
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
