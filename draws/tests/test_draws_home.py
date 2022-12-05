from django.urls import resolve, reverse

from draws import views
from .test_draw_base import DrawTestBase


class DrawHomeViewTest(DrawTestBase):
    def test_draws_home_view_function_is_correct(self):
        view = resolve(reverse('draws:home'))

        self.assertIs(view.func, views.home)

    def test_not_published_draw_in_home_view(self):
        self.make_draw(is_published=False)

        response = self.client.get(reverse('draws:home'))
        response_context_draws = response.context['draws']

        self.assertEqual(len(response_context_draws), 0)

    def test_draws_home_loads_correct_template(self):
        response = self.client.get(reverse('draws:home'))
        template_url = 'draws/pages/home.html'

        self.assertTemplateUsed(response, template_url)
