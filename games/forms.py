from django import forms
from games.models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['created_at', 'updated_at', 'id']
