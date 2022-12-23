from django import forms

from draws.models import DrawComment


class DrawCommentForm(forms.ModelForm):
    class Meta:
        model = DrawComment
        fields = ('comment',)
