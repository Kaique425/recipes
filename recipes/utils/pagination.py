from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def make_pagination(request, queryset, per_page):
    try:
        page = request.GET.get("page", "1")

    except (EmptyPage, PageNotAnInteger):
        page = "1"
    recipes_paginator = Paginator(queryset, per_page).page(page)

    return recipes_paginator
