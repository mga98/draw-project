from draws.tests.test_draw_base import DrawTestBase


class AccountsTestBase(DrawTestBase):
    def setUp(self, *args, **kwargs):
        self.draw_form_data = {
            'title': 'Draw Title',
            'description': 'Draw Description',
            'about': 'Draw About',
        }

        return super().setUp(*args, **kwargs)

    def make_draw_and_login(self):
        self.make_draw()
        self.client.login(
            username='username',
            password='123456'
        )
