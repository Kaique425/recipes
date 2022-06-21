from django.conf import settings
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from .models import Recipe
from .utils.pagination import make_pagination
from django.contrib.auth.decorators import login_required
PER_PAGE = settings.PER_PAGE

@method_decorator(
    login_required(login_url="author:login", redirect_field_name="next"),name="dispatch"
)
class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ["-id"]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["recipes"] = make_pagination(
            self.request, context.get("recipes"), PER_PAGE
        )
        return context


@method_decorator(login_required(
    login_url="author:login", redirect_field_name="next"),
    name="dispatch")
class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipe_list.html"


@method_decorator(
    login_required(
        login_url="author:login", redirect_field_name="next"
    ), name="dispatch"
)
class SearchRecipeListView(RecipeListViewBase):
    template_name = "recipes/search.html"

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get("search", "").strip()

        if not search:
            raise Http404()
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search) | Q(description__icontains=search),
            ),
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search = self.request.GET.get("search", "").strip()
        print(search)
        context.update(
            {
                "search_url": f"&search={search}",
                "search": search,
                "url_view": reverse("recipe:search"),
            }
        )

        return context


@method_decorator(
    login_required(
        login_url="author:login", redirect_field_name="next"
    ), name="dispatch"
)
class CategoryRecipeListView(RecipeListViewBase):
    template_name = "recipe_list.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            category__id=self.kwargs.get("id"),
        )

        return queryset

@login_required(login_url="author:login", redirect_field_name="next")
def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    title = f"Recipe: {recipe.title}"
    context = {"recipe": recipe, "is_detail_page": True, "title": title}
    return render(request, "recipes/recipe_detail.html", context)



@method_decorator(
    login_required(
        login_url="author:login", redirect_field_name="next"
    ), name="dispatch"
)
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get("pk"))
        title = f"Recipe: {recipe.title}"
        context.update({"is_detail_page": True, "title": title})

        return context
