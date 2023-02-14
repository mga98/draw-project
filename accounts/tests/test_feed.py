from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class FeedTest(AccountsTestBase):
    def test_feed_view_function(self):
        view = resolve(reverse('accounts:feed'))

        self.assertIs(view.func, views.feed)

    def test_feed_load_correct_draws(self):
        self.make_draw_and_login()

        url = reverse('accounts:feed')
        url_follow = reverse('accounts:follow_unfollow')

        self.client.post(
            url_follow, follow=True, data={'id': 1}
        )
        response = self.client.get(url, follow=True)
        title = 'Draw Title'

        self.assertIn(title, response.content.decode('utf-8'))

    def test_no_following_users_feed(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('accounts:feed')
        response = self.client.get(url, follow=True)
        msg = 'Você ainda não segue nenhum usuário'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_feed_doesnt_show_not_published_draws(self):
        self.make_draw(is_published=False)
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('accounts:feed')
        url_follow = reverse('accounts:follow_unfollow')

        self.client.post(
            url_follow, follow=True, data={'id': 1}
        )
        response = self.client.get(url, follow=True)

        msg = 'Nenhum desenho recente'

        self.assertIn(msg, response.content.decode('utf-8'))
