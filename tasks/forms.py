from django import forms

from tasks.models import Match

EMPTY_INPUT_ERROR = "You can't have an empty Smarkets event address"

class MatchForm(forms.models.ModelForm):

    class Meta:
        model = Match
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': "Enter a Smarkets event web address",
            })
        }
        error_messages = {
            'text': {
                'required': EMPTY_INPUT_ERROR}
        }
