import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Recipe

"""def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
        print(f"cover of id: {instance.id} was deleted")
    except (ValueError, FileNotFoundError) as e:
        print(e, f"cover of id: {instance.id} wasn't deleted")


@receiver(pre_delete, sender=Recipe)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk)
    # delete_cover(old_instance)
    print(
        f"Antiga instancia: {old_instance.cover.path} Nova instancia:{instance.cover}"
    )


@receiver(pre_save, sender=Recipe)
def recipe_post_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk)
    # delete_cover(old_instance)
    is_new_cover = True if old_instance.cover != instance.cover else False
    answer = "Sim" if is_new_cover else "Não"
    if is_new_cover:
        delete_cover(old_instance)
        print(f"É uma nova imagem ? {answer}")
"""
