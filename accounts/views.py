from itertools import chain

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import Profile
from draws.models import Draw, DrawComment
from utils.pagination import make_pagination

from .forms import DrawForm, LoginForm, ProfileEditForm, RegisterForm


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

    if request.user.id:
        current_user = get_object_or_404(Profile, pk=request.user.id)

        if current_user.following.filter(user=pk).exists():
            follow_button = "Deixar de seguir"
        else:
            follow_button = "Seguir"

    else:
        follow_button = None

    return render(request, 'accounts/pages/profile_view.html', context={
        'profile': profile,
        'draws': draws,
        'follow_button': follow_button,
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


@login_required(login_url='accounts:login', redirect_field_name='next')
def feed(request):
    profile = get_object_or_404(Profile, id=request.user.id)
    following = profile.following.all()[:10]

    usernames = []
    feed = []

    for user in profile.following.all():
        usernames.append(user.user)

    for username in usernames:
        draws = Draw.objects.select_related(
            'author', 'author__profile'
        ).filter(
            author=username,
            is_published=True,
        ).order_by('-created_at')
        feed.append(draws)

    feed_list = list(chain(*feed))

    page_obj, pagination_range = make_pagination(
        request,
        feed_list,
        8
    )

    return render(request, 'accounts/pages/feed.html', context={
        'draws': page_obj,
        'pagination_range': pagination_range,
        'following': following,
    })


@login_required
def follow_unfollow(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    user_id = POST.get('id')

    follower = get_object_or_404(Profile, pk=user_id)
    current_user = get_object_or_404(Profile, pk=request.user.id)

    if current_user.following.filter(user=user_id).exists():
        current_user.following.remove(follower)
        current_user.save()
        messages.success(request, f'Você deixou de seguir {follower.user}')

    else:
        current_user.following.add(follower)
        current_user.save()
        messages.success(request, f'Você começou a seguir {follower.user}')

    return redirect(reverse('accounts:profile_view', kwargs={'pk': user_id}))


@login_required
def like_unlike(request):
    if request.method == 'POST':
        id = request.POST.get('post_id')
        draw = get_object_or_404(Draw, id=id)

        if draw.like.filter(id=request.user.profile.id).exists():
            draw.like.remove(request.user.profile)
            draw.like_count -= 1
            draw.save()

        else:
            draw.like.add(request.user.profile)
            draw.like_count += 1
            draw.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        raise Http404


@login_required(login_url='accounts:liked_posts', redirect_field_name='next')
def liked_posts(request):
    draws = Draw.objects.filter(
        like=request.user.profile
    )

    draws = list(reversed(draws))

    page_obj, pagination_range = make_pagination(
        request,
        draws,
        10
    )

    return render(request, 'accounts/pages/liked_posts.html', context={
        'draws': page_obj,
        'pagination_range': pagination_range,
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
