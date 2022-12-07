# flake8: noqa

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')
        add_placeholder(self.fields['email'], 'Digite um e-mail válido')
        add_placeholder(self.fields['first_name'], 'Digite seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite seu último nome')

    username = forms.CharField(
        label='Nome de usuário',
        error_messages={
            'required': 'Você precisa preencher o campo de usuário!',
            'min_length': 'O nome de usuário precisa ter pelo menos 4 caracteres!',
            'max_length': 'O nome de usuário pode ter no máximo 15 caracteres!'
        },
        help_text='O nome de usuário precisa ter entre 4 e 15 caracteres!',
        min_length=4,
        max_length=15,
    )

    first_name = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de primeiro nome!'},
        label='Primeiro nome'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de último nome!'},
        label='Último nome'
    )

    email = forms.CharField(
        error_messages={'required': 'Você precisa preencher o campo de E-mail!'},
        label='E-mail',
        help_text='O e-mail precisa ser válido!'
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(),
        validators=[strong_password],
        error_messages={'required': 'Você precisa preencher o campo da senha!'}
    )

    password2 = forms.CharField(
        label='Confirme sua senha',
        widget=forms.PasswordInput(),
        error_messages={'required': 'Você precisa repetir sua senha!'}
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Este E-mail já está sendo utilizado!',
                code='invalid'
            )

        return email

    def clean(self): 
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Verifique se as senhas são iguais!',
                code='invalid'
                )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
