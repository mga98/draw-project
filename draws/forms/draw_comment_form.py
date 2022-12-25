from django import forms

from draws.models import DrawComment
from utils.django_forms import add_placeholder


class DrawCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['comment'], 'Deixe seu comentário')

    class Meta:
        model = DrawComment
        fields = ('comment',)
