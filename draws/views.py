from django.shortcuts import render, get_object_or_404

from .models import Draw


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

    # Add pagination logic here.

    return render(request, 'draws/pages/all_draws.html', context={
        'draws': draws
    })
