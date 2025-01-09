from django import forms
from hands.models import Hand
import json

class HandForm(forms.ModelForm):
    class Meta:
        model = Hand
        fields = ['subject', 'cards', 'bids', 'correct_answer', 'user_updated', 'metadata', 'optional_bids', 'explanation']


class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label="Upload JSON File")
    subject = forms.CharField(label="Subject", max_length=255)
    metadata = forms.CharField(
        label="Metadata (JSON format)",
        widget=forms.Textarea,
        required=False
    )

    def clean_metadata(self):
        metadata = self.cleaned_data.get('metadata', '')
        if metadata:
            try:
                # Attempt to parse the metadata as JSON
                return json.loads(metadata)
            except json.JSONDecodeError:
                raise ValidationError("Metadata must be a valid JSON object.")
        return {}


class ExplanationForm(forms.ModelForm):
    class Meta:
        model = Hand
        fields = ['correct_answer', 'explanation']


class CompetitionForm(forms.Form):
    number_of_hands = forms.IntegerField(
        label="Number of Hands",
        min_value=1,
        help_text="Enter the number of random hands to include."
    )

