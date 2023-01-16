from django.urls import resolve, reverse

from accounts import views

from .test_accounts_base import AccountsTestBase


class FollowUnfollowTests(AccountsTestBase):
    def test_follow_unfollow_view_function(self):
        view = resolve(reverse('accounts:follow_unfollow'))

        self.assertIs(view.func, views.follow_unfollow)

    def test_succesfully_user_follow(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456',
        )

        self.make_author(
            username='Followed'
        )

        url = reverse('accounts:follow_unfollow')
        response = self.client.post(
            url, follow=True, data={'id': 2}
        )
        msg = 'Você começou a seguir Followed'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_succesfully_user_unfollow(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )

        self.make_author(
            username='Unfollowed'
        )

        url = reverse('accounts:follow_unfollow')
        self.client.post(
            url, follow=True, data={'id': 2}
        )
        response = self.client.post(
            url, follow=True, data={'id': 2}
        )
        msg = 'Você deixou de seguir Unfollowed'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_follow_unfollow_receives_get_method(self):
        self.make_author()
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('accounts:follow_unfollow')
        response = self.client.get(
            url, follow=True, data={'id': 1}
        )

        self.assertEqual(response.status_code, 404)
