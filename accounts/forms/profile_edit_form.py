from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile
from utils.django_forms import add_placeholder


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['bio'], 'Escreva sua bio')

    class Meta:
        model = Profile

        fields = ('bio', 'user_img')

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = self.cleaned_data
        bio = cleaned_data.get('bio')

        if len(bio) < 5:
            raise ValidationError('A bio deve ter mais de 5 caracteres!')

        return super_clean
