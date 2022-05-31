from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def make_pagination(request, queryset, per_page):
    try:
        page = int(request.GET.get("page"))

    except:
        page = "1"
    recipes_paginator = Paginator(queryset, per_page).page(page)

    return recipes_paginator
