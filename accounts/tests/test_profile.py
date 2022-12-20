from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class ProfileTest(AccountsTestBase):
    def test_profile_view_function(self):
        view = resolve(
            reverse('accounts:profile_view', kwargs={'pk': 1})
        )

        self.assertIs(view.func, views.profile_view)

    def test_profile_view_raises_404_if_no_profile(self):
        url = reverse('accounts:profile_view', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_profile_view_empty_draws(self):
        self.make_author()

        url = reverse('accounts:profile_view', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)
        msg = 'Este usuário ainda não publicou nenhum desenho.'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_profile_loads_correct_draws(self):
        self.make_draw()

        url = reverse('accounts:profile_view', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)
        title = 'Draw Title'

        self.assertIn(title, response.content.decode('utf-8'))

    def test_profile_dont_show_not_published_draws(self):
        self.make_draw(is_published=False)

        url = reverse('accounts:profile_view', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)

        self.assertEqual(len(response.context['draws']), 0)

    def test_profile_loads_correct_user(self):
        self.make_author(first_name='Correct')

        url = reverse('accounts:profile_view', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)
        user = 'Correct'

        self.assertIn(user, response.content.decode('utf-8'))
