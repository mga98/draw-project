from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class LikeUnlikeTests(AccountsTestBase):
    def test_like_unlike_view_function(self):
        view = resolve(reverse('accounts:like_unlike'))

        self.assertIs(view.func, views.like_unlike)

    def test_succesfully_like_post(self):
        self.make_draw_and_login()

        url = reverse('accounts:like_unlike')
        url_2 = reverse('draws:draw_view', kwargs={'pk': 1})

        self.client.post(
            url, follow=True, data={'post_id': 1}
        )
        response = self.client.get(url_2)

        text = '<p id="like_count">1</p>'

        self.assertIn(text, response.content.decode('utf-8'))

    def test_succesfully_dislike_post(self):
        self.make_draw_and_login()

        url = reverse('accounts:like_unlike')
        url_2 = reverse('draws:draw_view', kwargs={'pk': 1})

        for i in range(0, 2):
            self.client.post(
                url, follow=True, data={'post_id': 1}
            )

        response = self.client.get(url_2)

        text = '<p id="like_count">0</p>'

        self.assertIn(text, response.content.decode('utf-8'))

    def test_like_unlike_returns_404_in_get_method(self):
        self.make_draw_and_login()

        url = reverse('accounts:like_unlike')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
