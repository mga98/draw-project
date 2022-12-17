from draws.tests.test_draw_base import DrawTestBase


class AccountsTestBase(DrawTestBase):
    def make_draw_and_login(self):
        self.make_draw()
        self.client.login(
            username='username',
            password='123456'
        )
