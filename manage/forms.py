from django import forms
from hands.models import Hand


class HandForm(forms.ModelForm):
    class Meta:
        model = Hand
        fields = ['subject', 'cards', 'bids', 'correct_answer', 'user_updated', 'metadata', 'optional_bids', 'explanation']
