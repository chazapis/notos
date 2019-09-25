from django import forms

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        exclude = ('user',)
        widgets = {'step': forms.HiddenInput()}

class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        exclude = ('participant',)
        widgets = {'step': forms.HiddenInput()}

class TravelDetailsForm(forms.ModelForm):
    class Meta:
        model = TravelDetails
        exclude = ('participant',)
        widgets = {'step': forms.HiddenInput()}
