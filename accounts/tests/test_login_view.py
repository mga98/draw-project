from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from parameterized import parameterized

from accounts import views
from accounts.forms import LoginForm


class LoginViewUnitTest(TestCase):
    def test_login_view_function_is_correct(self):
        view = resolve(reverse('accounts:login'))

        self.assertIs(view.func, views.login_view)

    def test_login_create_view_function_is_correct(self):
        view = resolve(reverse('accounts:login_create'))

        self.assertIs(view.func, views.login_create)

    @parameterized.expand([
        ('username', 'Nome de usuário'),
        ('password', 'Sua senha'),
    ])
    def test_login_placeholders_are_correct(self, field, placeholder):
        form = LoginForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Usuário'),
        ('password', 'Senha'),
    ])
    def test_login_labels_are_correct(self, field, label):
        form = LoginForm()
        current_label = form[field].field.label

        self.assertEqual(label, current_label)


class AccountLoginIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'password': 'password',
        }

    def create_user(self):
        user = User.objects.create_user(
            username='user',
            password='password',
        )

        return user

    def test_successful_login(self):
        self.create_user()
        url = reverse('accounts:login_create')

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Logado com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_user_authentication(self):
        self.create_user()

        url = reverse('accounts:login_create')
        self.form_data['password'] = 'errortest'

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Usuário ou senha inválidos'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_form_not_valid(self):
        url = reverse('accounts:login_create')
        self.form_data.update({
            'username': '',
            'password': '',
        })

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Erro ao válidar formulário!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_request_to_login_create_returns_404(self):
        url = reverse('accounts:login_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
