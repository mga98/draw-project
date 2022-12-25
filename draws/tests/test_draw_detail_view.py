from django.urls import resolve, reverse

from accounts.tests.test_accounts_base import AccountsTestBase
from draws import views


class DrawDetailViewTest(AccountsTestBase):
    def test_draw_detail_view_function_is_correct(self):
        view = resolve(reverse('draws:draw_view', kwargs={'pk': 1}))

        self.assertIs(view.func, views.draw)

    def test_not_published_draw_in_draw_view(self):
        self.make_draw(is_published=False)

        response = self.client.get(
            reverse('draws:draw_view', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 404)

    def test_draw_view_loads_correct_template(self):
        self.make_draw()

        response = self.client.get(
            reverse('draws:draw_view', kwargs={'pk': 1})
        )
        template_url = 'draws/pages/draw_view.html'

        self.assertTemplateUsed(response, template_url)

    def test_draw_view_loads_correct_draw(self):
        draw_title = 'Draw Title'

        self.make_draw()

        response = self.client.get(
            reverse('draws:draw_view', kwargs={'pk': 1})
        )

        self.assertIn(draw_title, response.content.decode('utf-8'))

    def test_draw_view_raises_404_if_draw_doesnt_exists(self):
        response = self.client.get(
            reverse('draws:draw_view', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 404)

    def test_logged_in_users_can_see_they_draws_not_publisheds(self):
        self.make_draw(is_published=False)
        self.client.login(
            username='username',
            password='123456'
        )

        url = reverse('draws:draw_view', kwargs={'pk': 1})
        response = self.client.get(url)
        title = 'Draw Title'

        self.assertIn(title, response.content.decode('utf-8'))


class DrawCommentTest(AccountsTestBase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'comment': 'Comment Test',
        }

    def test_succesful_draw_comment(self):
        self.make_draw_and_login()

        url = reverse('draws:draw_view', kwargs={'pk': 1})
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        comment = 'Comment Test'

        self.assertIn(comment, response.content.decode('utf-8'))

    def test_draw_comment_deleted(self):
        self.make_draw_and_login()

        # Making a comment
        url = reverse('draws:draw_view', kwargs={'pk': 1})
        self.client.post(
            url, data=self.form_data, follow=True
        )

        # Deleting comment
        url2 = reverse('accounts:comment_delete')
        self.client.post(
            url2, data={'id': 1}, follow=True
        )

        # Back to post page
        response = self.client.get(url, follow=True)
        text = 'Comentários(0)'

        self.assertIn(text, response.content.decode('utf-8'))

    def test_draw_comment_delete_receives_get_method(self):
        self.make_draw_and_login()

        # Making a comment
        url = reverse('draws:draw_view', kwargs={'pk': 1})
        self.client.post(
            url, data=self.form_data, follow=True
        )

        # Trying to delete with get method
        url2 = reverse('accounts:comment_delete')
        response = self.client.get(
            url2, data={'id': 1}, follow=True
        )

        self.assertEqual(response.status_code, 404)
