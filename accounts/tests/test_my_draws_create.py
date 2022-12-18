from django.urls import resolve, reverse

from accounts import views
from .test_accounts_base import AccountsTestBase


class MyDrawsCreateTests(AccountsTestBase):
    def test_my_draws_create_view_function(self):
        view = resolve(reverse('accounts:my_draws_create'))

        self.assertIs(view.func, views.my_draws_create)

    def test_draw_created_successfully(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('accounts:my_draws_create')
        response = self.client.post(
            url, data=self.draw_form_data, follow=True
        )
        msg = 'Desenho criado com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))
