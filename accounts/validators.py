from collections import defaultdict
from django.core.exceptions import ValidationError


class DrawValidator:
    def __init__(self, data, errors=None, ErrorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        cleaned_data = self.data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        about = cleaned_data.get('about')

        if len(title) < 5:
            self.errors['title'].append(
                'O título deve ter pelo menos 5 caracteres!'
            )

        if len(about) < 5:
            self.errors['about'].append(
                'Sobre precisa ter mais de 5 caracteres!'
            )

        if title == description:
            self.errors['title'].append(
                'O título deve ser diferente da descrição!'
            )
            self.errors['description'].append(
                'A descrição deve ser diferente do título!'
            )

        if self.errors:
            raise self.ErrorClass(self.errors)
