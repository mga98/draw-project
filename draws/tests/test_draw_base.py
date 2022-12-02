from django.test import TestCase

from draws.models import Draw, User


class DrawMixin:
    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        """
        Create a generic author for tests
        """

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_draw(
        self,
        author_data=None,
        title='Draw Title',
        description='Draw Description',
        slug='draw-slug',
        about='Draw About',
        is_published=True,
    ):
        """
        Create a generic draw post for tests
        """

        if author_data is None:
            author_data = {}

        return Draw.objects.create(
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            about=about,
            is_published=is_published,
        )

    def make_various_draws(self, qtd=10):
        draws = []

        for i in range(qtd):
            kwargs = {
                'title': f'Draw Title {i}',
                'slug': f'r{i}',
                'author_data': {'username': f'u{i}'}
            }

            draw = self.make_draw(**kwargs)
            draws.append(draw)

        return draws


class DrawTestBase(TestCase, DrawMixin):
    def setUp(self) -> None:
        """
        Generic model for draw tests
        """
        return super().setUp()
