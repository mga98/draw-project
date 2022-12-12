from django import forms

from utils.django_forms import add_placeholder, add_attr


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Nome de usuário')
        add_placeholder(self.fields['password'], 'Sua senha')

    username = forms.CharField(label='Usuário')
    add_attr(username, 'autofocus', 'autofocus')
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
    )
