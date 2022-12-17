from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404

from .forms import RegisterForm, LoginForm, DrawForm
from draws.models import Draw


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
            messages.success(
                request, 'Você foi registrado e logado com sucesso!'
            )

            del (request.session['register_form_data'])

            return redirect(reverse('draws:home'))

    return redirect(reverse('accounts:register'))


def login_view(request):
    form = LoginForm()

    is_login_form = True
    form_title = 'Login'
    form_button = 'Login'

    return render(request, 'accounts/pages/login_view.html', context={
        'form': form,
        'is_login_form': is_login_form,
        'form_title': form_title,
        'form_button': form_button,
        'form_action': reverse('accounts:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('accounts:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            messages.success(request, 'Logado com sucesso!')

            return redirect(reverse('draws:home'))

        else:
            messages.error(request, 'Usuário ou senha inválidos!')

    else:
        messages.error(request, 'Erro ao válidar formulário!')

    return redirect(login_url)


@login_required(login_url='accounts:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Logout não pode ser executado!')
        return redirect(reverse('accounts:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Usuário de logout inválido')
        return redirect(reverse('accounts:login'))

    logout(request)
    messages.success(request, 'Você foi deslogado.')
    return redirect(reverse('accounts:login'))


@login_required(login_url='accounts:login', redirect_field_name='next')
def my_draws(request):
    draws = Draw.objects.filter(
        author=request.user
    ).order_by('-id')

    return render(request, 'accounts/pages/my_draws.html', context={
        'draws': draws
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def my_draws_edit(request, pk):
    draw = get_object_or_404(
        Draw,
        author=request.user,
        pk=pk
    )

    if not draw:
        raise Http404

    form = DrawForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=draw
    )

    if form.is_valid():
        draw = form.save(commit=False)

        draw.author = request.user
        draw.is_published = False

        draw.save()

        messages.success(request, 'Seu desenho foi salvo com sucesso!')

        return redirect(reverse('accounts:my_draws'))

    return render(request, 'accounts/pages/my_draws_edit.html', context={
        'form': form,
        'form_button': 'Salvar',
        'form_title': 'Editar desenho',
    })
