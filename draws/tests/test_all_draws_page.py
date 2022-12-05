from django.urls import resolve, reverse

from draws import views
from .test_draw_base import DrawTestBase


class AllDrawsViewTest(DrawTestBase):
    def test_all_draws_view_function_is_correct(self):
        view = resolve(reverse('draws:all_draws'))

        self.assertIs(view.func, views.all_draws)

    def test_not_published_draw_in_all_draws_view(self):
        self.make_draw(is_published=False)

        response = self.client.get(
            reverse('draws:all_draws')
        )
        msg = 'Nenhum desenho recente.'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_draw_view_loads_correct_template(self):
        response = self.client.get(
            reverse('draws:all_draws')
        )
        template_url = 'draws/pages/all_draws.html'

        self.assertTemplateUsed(response, template_url)
