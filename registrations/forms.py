from django import forms

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
