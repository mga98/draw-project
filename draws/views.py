from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from django.http import Http404
from django.db.models import Q

from .models import Draw
from utils.pagination import make_pagination


def home(request):
    draws = Draw.objects.filter(
        is_published=True,
    ).order_by('-id')

    # Add a trending logic here.

    return render(request, 'draws/pages/home.html', context={
        'draws': draws
    })


def draw(request, pk):
    draw = get_object_or_404(Draw, id=pk, is_published=True)

    return render(request, 'draws/pages/draw_view.html', context={
        'draw': draw
    })


def all_draws(request):
    draws = Draw.objects.filter(
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        draws,
        9
    )

    return render(request, 'draws/pages/all_draws.html', context={
        'draws': page_obj,
        'pagination_range': pagination_range,
    })


class DrawSearch(ListView):
    template_name = 'draws/pages/draws_search.html'
    model = Draw
    context_object_name = 'draws'
    ordering = ['-id']

    def get_search_term(self):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404

        return search_term

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.get_search_term()
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.get_search_term()
        ctx.update(
            {
                'page_title': f'Pesquisa por {search_term}',
                'aditional_url_query': f'&q={search_term}'
            }
        )

        return ctx
