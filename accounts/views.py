from django.shortcuts import render
from django.urls import reverse

from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)
    form_title = 'Register'
    form_button = 'Enviar'

    return render(request, 'accounts/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('accounts:register_create'),
        'form_title': form_title,
        'form_button': form_button,
    })


def register_create(request):
    ...


def login_view(request):
    return render(request, 'accounts/pages/login_view.html')


def login_create(request):
    ...
