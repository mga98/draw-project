# flake8: noqa

from django.urls import reverse
from draws.tests.test_draw_base import DrawTestBase

from utils.pagination import make_pagination_range


class PaginationTest(DrawTestBase):
    # Pagination range tests:
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        # Current page is 1
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page is 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=2,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page is 3, where range should change
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page is 10
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=10,
        )['pagination']

        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page is 12
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=12,
        )['pagination']

        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page is 19
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            page_qty=4,
            current_page=19,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

    # Pagination tests:
    def test_if_pagination_is_showing_the_draws_correctly(self):
        self.make_draw()
        self.make_draw(
            author_data={'username': 'usertest'},
            slug='test-slug'
        )

        # Current page is 1
        url = reverse('draws:home')
        response = self.client.get(url + '?page=1')
        response_context_draws = response.context['recent_draws']

        self.assertEqual(len(response_context_draws), 2)
