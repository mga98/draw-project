from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from accounts import views


class LogoutViewTest(TestCase):
    def create_user_and_login(self):
        User.objects.create_user(
            username='usertest',
            password='Testuser@1'
        )

        self.client.login(
            username='usertest',
            password='Testuser@1',
        )

    def test_logout_view_function_is_correct(self):
        view = resolve(reverse('accounts:logout'))

        self.assertIs(view.func, views.logout_view)

    def test_succesful_logout(self):
        self.create_user_and_login()
        url = reverse('accounts:logout')
        msg = 'Você foi deslogado.'

        response = self.client.post(
            url, data={'username': 'usertest'}, follow=True
        )

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_logout_receive_get_method(self):
        self.create_user_and_login()
        url = reverse('accounts:logout')
        msg = 'Logout não pode ser executado'

        response = self.client.get(url, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_user_tries_to_logout_another_user(self):
        self.create_user_and_login()
        url = reverse('accounts:logout')
        msg = 'Usuário de logout inválido'

        response = self.client.post(
            url, data={'username': 'anotheruser'}, follow=True
        )

        self.assertIn(msg, response.content.decode('utf-8'))
