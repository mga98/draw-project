from django.urls import resolve, reverse

from draws import views

from .test_draw_base import DrawTestBase


class DrawDetailViewTest(DrawTestBase):
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
