from django.shortcuts import render

from .models import Draw


def home(request):
    draws = Draw.objects.filter(
        is_published=True,
    ).order_by('-id')

    return render(request, 'draws/pages/home.html', context={
        'draws': draws
    })


def draw(request):
    ...
