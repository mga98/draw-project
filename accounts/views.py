from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

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
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        authenticated_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        if authenticated_user is not None:
            login(request, authenticated_user)

            del (request.session['register_form_data'])

            return redirect(reverse('draws:home'))

    return redirect(reverse('accounts:register'))


def login_view(request):
    return render(request, 'accounts/pages/login_view.html')


def login_create(request):
    ...
