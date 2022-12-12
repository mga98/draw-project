from unittest import TestCase

from django.test import TestCase as DjangoTestCase
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


class AccountRegisterIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Password12.',
            'password2': 'Password12.'
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Você precisa preencher o campo de usuário!'),
        ('first_name', 'Você precisa preencher o campo de primeiro nome!'),
        ('last_name', 'Você precisa preencher o campo de último nome!'),
        ('email', 'Você precisa preencher o campo de E-mail!'),
        ('password', 'Você precisa preencher o campo da senha'),
        ('password2', 'Você precisa repetir sua senha!'),
    ])
    def test_register_fields_cannot_be_empty(self, field, msg):
        url = reverse('accounts:register_create')
        self.form_data[field] = ''

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_min_length(self):
        url = reverse('accounts:register_create')
        self.form_data['username'] = '123'
        msg = 'O nome de usuário precisa ter pelo menos 4 caracteres!'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_max_length(self):
        url = reverse('accounts:register_create')
        self.form_data['username'] = 'A' * 16
        msg = 'O nome de usuário pode ter no máximo 15 caracteres!'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_strength(self):
        url = reverse('accounts:register_create')
        self.form_data['password'] = 'password'
        msg = 'Sua senha deve ter no mínimo uma letra maiúscula, '
        'uma letra minúsucla e um número. '
        'E deve ter no mínimo 8 carateres.'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_passwords_matchs(self):
        url = reverse('accounts:register_create')
        self.form_data['password'] = 'Nomatch12.'
        msg = 'Verifique se as senhas são iguais'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_request_to_register_create_returns_404(self):
        url = reverse('accounts:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_email_must_be_unique(self):
        url = reverse('accounts:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Este E-mail já está sendo utilizado!'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_form_is_valid(self):
        url = reverse('accounts:register_create')

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Você foi registrado e logado com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_account_created_can_login(self):
        url = reverse('accounts:register_create')
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='user',
            password='Password12.'
        )

        self.assertTrue(is_authenticated)
