from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class MyDrawsEditTests(AccountsTestBase):
    def test_my_draws_edit_view_function(self):
        view = resolve(reverse('accounts:my_draws_edit', kwargs={'pk': 1}))

        self.assertIs(view.func, views.my_draws_edit)

    def test_my_draws_edit_founds_no_draw(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('accounts:my_draws_edit', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_succesfully_draw_edit(self):
        self.make_draw_and_login()

        url = reverse('accounts:my_draws_edit', kwargs={'pk': 1})
        response = self.client.post(
            url, data=self.draw_form_data, follow=True
        )
        msg = 'Seu desenho foi editado com sucesso!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_draw_title_and_description_are_equal(self):
        self.make_draw_and_login()
        self.draw_form_data['title'] = 'Draws'
        self.draw_form_data['description'] = 'Draws'

        url = reverse('accounts:my_draws_edit', kwargs={'pk': 1})
        response = self.client.post(
            url, data=self.draw_form_data, follow=True
        )
        msg = 'O título deve ser diferente da descrição!'
        msg2 = 'A descrição deve ser diferente do título!'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg2, response.content.decode('utf-8'))

    def test_draw_title_min_length(self):
        self.make_draw_and_login()
        self.draw_form_data['title'] = '123'

        url = reverse('accounts:my_draws_edit', kwargs={'pk': 1})
        response = self.client.post(
            url, data=self.draw_form_data, follow=True
        )
        msg = 'O título deve ter pelo menos 5 caracteres!'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_draw_about_min_length(self):
        self.make_draw_and_login()
        self.draw_form_data['about'] = '123'

        url = reverse('accounts:my_draws_edit', kwargs={'pk': 1})
        response = self.client.post(
            url, data=self.draw_form_data, follow=True
        )
        msg = 'Sobre precisa ter mais de 5 caracteres!'

        self.assertIn(msg, response.content.decode('utf-8'))
