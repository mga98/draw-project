from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError

from draws.models import Draw
from utils.django_forms import add_placeholder


class DrawForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_placeholder(self.fields['title'], 'Título do desenho')
        add_placeholder(self.fields['description'], 'Descrição do desenho')
        add_placeholder(self.fields['about'], 'Sobre seu desenho')

    class Meta:
        model = Draw

        fields = ('title', 'description', 'about', 'img')

    prepopulated_fields = {  # noqa
        'slug': ('title',)
    }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        about = cleaned_data.get('about')

        if len(title) < 5:
            self._my_errors['title'].append(
                'O título deve ter pelo menos 5 caracteres!'
            )

        if len(about) < 5:
            self._my_errors['about'].append(
                'Sobre precisa ter mais de 5 caracteres!'
            )

        if title == description:
            self._my_errors['title'].append(
                'O título deve ser diferente da descrição!'
            )
            self._my_errors['description'].append(
                'A descrição deve ser diferente do título!'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
