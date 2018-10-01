from django import forms

from .utils import convert_smarkets_web_address_to_match_name
from .utils import convert_smarkets_web_address_to_datetime_date_format

from tasks.models import Match

EMPTY_INPUT_ERROR = "You can't have an empty Smarkets event address"


class MatchForm(forms.models.ModelForm):

    class Meta:
        model = Match
        fields = ('full_text', )
        widgets = {
            'full_text': forms.fields.TextInput(attrs={
                'placeholder': "Enter a Smarkets event web address",
                'amount_already_bet_home': forms.fields.TextInput(),
            })
        }
        error_messages = {
            'full_text': {
                'required': EMPTY_INPUT_ERROR}
        }

    def save(self, for_task, full_text, **kwargs):
        self.instance.task = for_task
        self.instance.text = convert_smarkets_web_address_to_match_name(
            full_text)
        self.instance.date = convert_smarkets_web_address_to_datetime_date_format(
            full_text)
        if 'amount_already_bet_home' in kwargs:
            self.instance.amount_already_bet_home = kwargs[
                'amount_already_bet_home']
        return super().save()
