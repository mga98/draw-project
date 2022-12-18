from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class MyDrawsDeleteTest(AccountsTestBase):
    def test_my_draws_delete_view_function(self):
        view = resolve(reverse('accounts:my_draws_delete'))

        self.assertIs(view.func, views.my_draws_delete)

    def test_my_draws_delete_receives_get_method(self):
        self.make_draw_and_login()

        url = reverse('accounts:my_draws_delete')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_my_draws_deleted_succesfully(self):
        self.make_draw_and_login()

        url = reverse('accounts:my_draws_delete')
        response = self.client.post(
            url, follow=True, data={'id': 1}
        )
        msg = 'Desenho deletado com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_my_draws_delete_returns_404_if_draw_doesnt_exists(self):
        self.make_draw_and_login()

        url = reverse('accounts:my_draws_delete')
        response = self.client.post(
            url, data={'id': 2}, follow=True
        )

        self.assertEqual(response.status_code, 404)
