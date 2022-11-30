from django.shortcuts import render


def home(request):
    return render(request, 'draws/pages/home.html')
