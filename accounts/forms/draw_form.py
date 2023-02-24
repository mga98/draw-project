from django import forms
from collections import defaultdict
from django.core.exceptions import ValidationError

from draws.models import Draw
from utils.django_forms import add_placeholder
from accounts.validators import DrawValidator


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

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        DrawValidator(self.cleaned_data, ErrorClass=ValidationError)

        return super_clean
