from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify

from draws.models import Draw, DrawComment
from accounts.models import Profile
from .forms import DrawForm, LoginForm, RegisterForm, ProfileEditForm


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

            return redirect(reverse('accounts:my_draws'))

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
    return redirect(reverse('draws:home'))


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

        messages.success(request, 'Seu desenho foi editado com sucesso!')

        return redirect(reverse('accounts:my_draws'))

    return render(request, 'accounts/pages/my_draws_edit.html', context={
        'draw': draw,
        'form': form,
        'form_button': 'Salvar',
        'form_title': 'Editar Desenho',
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def my_draws_create(request):
    form = DrawForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        draw = form.save(commit=False)

        draw.author = request.user
        draw.is_published = False
        draw.slug = slugify(draw.title, allow_unicode=True)

        draw.save()

        messages.success(request, 'Desenho criado com sucesso!')
        return redirect(reverse('accounts:my_draws'))

    return render(request, 'accounts/pages/my_draws_edit.html', context={
        'form': form,
        'form_button': 'Salvar',
        'form_title': 'Novo Desenho'
    })


@login_required(
    login_url='accounts:my_draws_delete', redirect_field_name='next'
)
def my_draws_delete(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    id = POST.get('id')

    draw = get_object_or_404(Draw, author=request.user, pk=id)

    if not draw:
        raise Http404

    draw.delete()

    messages.success(request, 'Desenho deletado com sucesso!')

    return redirect(reverse('accounts:my_draws'))


def profile_view(request, pk):
    profile = get_object_or_404(
        Profile.objects.filter(pk=pk).select_related('user'), pk=pk
    )
    draws = Draw.objects.filter(
        author=profile.user,
        is_published=True,
    ).order_by('-id')

    return render(request, 'accounts/pages/profile_view.html', context={
        'profile': profile,
        'draws': draws
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def profile_edit(request, pk):
    profile = get_object_or_404(
        Profile.objects.filter(pk=pk).select_related('user'), pk=pk
    )

    form = ProfileEditForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=profile
    )

    if form.is_valid():
        form.save()

        messages.success(request, 'Bio editada com sucesso!')
        return redirect(reverse('accounts:my_draws'))

    return render(request, 'accounts/pages/profile_edit.html', context={
        'form': form,
        'profile': profile,
        'form_button': 'Salvar',
        'form_title': 'Editar Perfil'
    })


@login_required
def like_unlike(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        draw = get_object_or_404(Draw, id=id)

        if draw.like.filter(id=request.user.profile.id).exists():
            draw.like.remove(request.user.profile)
            draw.like_count -= 1
            result = draw.like_count
            draw.save()

        else:
            draw.like.add(request.user.profile)
            draw.like_count += 1
            result = draw.like_count
            draw.save()

        return JsonResponse({'result': result, })


@login_required(login_url='accounts:liked_posts', redirect_field_name='next')
def liked_posts(request):
    draws = Draw.objects.filter(
        like=request.user.profile
    )

    return render(request, 'accounts/pages/liked_posts.html', context={
        'draws': draws
    })


@login_required
def delete_comment(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    id = POST.get('id')

    comment = get_object_or_404(DrawComment, pk=id, user=request.user)

    if not comment:
        raise Http404

    comment.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
