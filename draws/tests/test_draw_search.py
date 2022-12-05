from django.urls import resolve, reverse

from draws import views

from .test_draw_base import DrawTestBase


class DrawSearchTest(DrawTestBase):
    def test_draw_search_class_is_correct(self):
        view = resolve(reverse('draws:draws_search'))

        self.assertIs(view.func.view_class, views.DrawSearch)

    def test_search_loads_correct_draws(self):
        title = 'title'

        draw = self.make_draw(title=title)

        search_url = reverse('draws:draws_search')
        response = self.client.get(
            f'{search_url}?q={title}'
        )

        self.assertIn(draw, response.context['draws'])

    def test_draw_search_raises_404_if_not_correct_term(self):
        response = self.client.get(
            reverse('draws:draws_search')
        )

        self.assertEqual(response.status_code, 404)
