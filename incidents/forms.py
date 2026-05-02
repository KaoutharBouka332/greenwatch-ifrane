from django import forms
from .models import Incident

class PublicIncidentForm(forms.ModelForm):
    consent = forms.BooleanField(
        label='I confirm this report is submitted in good faith.',
        required=True
    )

    class Meta:
        model = Incident
        fields = [
            'title', 'category', 'severity', 'description', 'location_name',
            'latitude', 'longitude', 'reporter_name', 'reporter_contact', 'attachment'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe what happened, visible signs, urgency, and nearby landmarks...'
            }),
            # Coordinates are intentionally hidden from citizens.
            # They are filled automatically when the user clicks the map.
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('latitude')
        lng = cleaned_data.get('longitude')
        if lat is None or lng is None:
            raise forms.ValidationError('Please select the incident location on the map before submitting.')
        return cleaned_data

class AdminIncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['status', 'severity', 'is_public', 'authority_note']
        widgets = {'authority_note': forms.Textarea(attrs={'rows': 4})}
