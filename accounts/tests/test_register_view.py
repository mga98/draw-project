from unittest import TestCase

# from django.test import TestCase as DjangoTestCase
from django.urls import resolve, reverse
from parameterized import parameterized

from accounts import views
from accounts.forms import RegisterForm


class RegisterViewUnitTest(TestCase):
    def test_register_view_function_is_correct(self):
        view = resolve(reverse('accounts:register'))

        self.assertIs(view.func, views.register_view)

    def test_register_create_view_function_is_correct(self):
        view = resolve(reverse('accounts:register_create'))

        self.assertIs(view.func, views.register_create)

    @parameterized.expand([
        ('username', 'Seu nome de usuário'),
        ('password', 'Digite sua senha'),
        ('password2', 'Repita sua senha'),
        ('email', 'Digite um e-mail válido'),
        ('first_name', 'Digite seu primeiro nome'),
        ('last_name', 'Digite seu último nome'),
    ])
    def test_placeholder_fields_are_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'O nome de usuário precisa ter entre 4 e 15 caracteres!'),
        ('email', 'O e-mail precisa ser válido!'),
    ])
    def test_fields_help_texts_are_correct(self, field, helptext):
        form = RegisterForm()
        current_help_text = form[field].field.help_text

        self.assertEqual(helptext, current_help_text)

    @parameterized.expand([
        ('username', 'Nome de usuário'),
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_label_are_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(label, current_label)
