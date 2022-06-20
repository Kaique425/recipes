from django.contrib.auth.models import User
from django.db import models
from django.forms import CharField
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
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

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe:recipe", args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}"

        return super().save(*args, **kwargs)
