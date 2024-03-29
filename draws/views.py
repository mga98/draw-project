from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.urls import reverse
from django.http import JsonResponse

from utils.pagination import make_pagination

from .models import Draw, DrawComment
from .forms import DrawCommentForm


class DrawListViewBase(ListView):
    model = Draw
    context_object_name = 'draws'
    paginate_by = None
    ordering = ['-id']
    template_name = 'draws/pages/all_draws.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        paje_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('draws'),
            9
        )
        ctx.update({
            'draws': paje_obj,
            'pagination_range': pagination_range,
        })

        return ctx


def home(request):
    draws = Draw.objects.select_related('author', 'author__profile').filter(
        is_published=True,
    ).order_by('-id')

    recent_draws = draws.order_by('-id')[:10]
    trending_draws = draws.order_by('-like_count', '-created_at')[:5]

    return render(request, 'draws/pages/home.html', context={
        'trending_draws': trending_draws,
        'recent_draws': recent_draws,
    })


class HomeViewApi(DrawListViewBase):
    template_name = 'draws/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        draws = self.get_context_data()['draws']
        draws_list = draws.object_list.values()

        return JsonResponse(
            list(draws_list),
            safe=False
        )


def draw(request, pk):
    draw = get_object_or_404(Draw, id=pk)
    comments = DrawComment.objects.filter(draw=pk).order_by('-created_at')

    if request.user == draw.author:
        draw = get_object_or_404(Draw, id=pk)

    else:
        draw = get_object_or_404(Draw, id=pk, is_published=True)

    if request.method == 'POST':
        form = DrawCommentForm(
            request.POST or None,
        )

        if form.is_valid():
            comment = form.save(commit=False)

            comment.user = request.user
            comment.draw = draw
            comment.save()
            form = DrawCommentForm()

            return redirect(reverse('draws:draw_view', kwargs={'pk': pk}))

    else:
        form = DrawCommentForm()

    return render(request, 'draws/pages/draw_view.html', context={
        'draw': draw,
        'form': form,
        'comments': comments,
    })


def all_draws(request):
    draws = Draw.objects.select_related('author', 'author__profile').filter(
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


class DrawSearch(DrawListViewBase):
    template_name = 'draws/pages/draws_search.html'

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
                Q(description__icontains=search_term) |
                Q(author__username__icontains=search_term)
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
                'additional_url_query': f'&q={search_term}',
            }
        )

        return ctx
