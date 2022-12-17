from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class MyDrawsViewTests(AccountsTestBase):
    def test_my_draw_view_function(self):
        view = resolve(reverse('accounts:my_draws'))

        self.assertIs(view.func, views.my_draws)

    def test_user_with_no_draws(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )
        url = reverse('accounts:my_draws')
        response = self.client.get(url, follow=True)
        msg = 'Você ainda não tem nenhum desenho publicado.'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_my_draws_view_loading_correct_draws(self):
        self.make_draw_and_login()

        url = reverse('accounts:my_draws')
        response = self.client.get(url, follow=True)
        title = 'Draw Title'

        self.assertIn(title, response.content.decode('utf-8'))
