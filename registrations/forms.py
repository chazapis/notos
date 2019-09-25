from django import forms
from tempus_dominus.widgets import DateTimePicker

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
        widgets = {'arrival': DateTimePicker(options={'sideBySide': True},
                                             attrs={'append': 'fa fa-calendar'}),
                   'departure': DateTimePicker(options={'sideBySide': True},
                                               attrs={'append': 'fa fa-calendar'})}
