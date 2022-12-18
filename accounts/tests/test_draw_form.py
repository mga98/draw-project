from django.urls import reverse

from .test_accounts_base import AccountsTestBase


class DrawFormTests(AccountsTestBase):
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
