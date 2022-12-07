from django.shortcuts import render


def register_view(request):
    return render(request, 'accounts/pages/register_view.html')


def register_create(request):
    ...


def login_view(request):
    return render(request, 'accounts/pages/login_view.html')


def login_create(request):
    ...
