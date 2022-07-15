import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms import CharField
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return (
            self.filter(
                is_published=True,
            )
            .select_related("author", "category")
            .prefetch_related("tags")
        )


class Recipe(models.Model):
    objects = RecipeManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparations_time = models.IntegerField()
    preparations_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    praparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to="recipes/cover/%Y/%m/%d/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True, default="")

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe:recipe", args=(self.id,))

    def resize_image(self, image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        pillow_image = Image.open(image_full_path)
        old_width, old_height = pillow_image.size

        if old_width < new_width:
            pillow_image.close()
            return

        new_height = round((new_width * old_height) / old_width)
        new_image = pillow_image.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}"
        save = super().save(*args, **kwargs)
        if self.cover:
            self.resize_image(self.cover, 800)

        return save
