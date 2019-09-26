from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit, HTML
from tempus_dominus.widgets import DateTimePicker

from .models import Participant, Exhibit, ExhibitParticipation, TravelDetails
from .layout import Formset


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('title', 'surname', 'name', 'address', 'country', 'commissioner_country', 'telephone', 'mobile', 'language', 'remarks')
        widgets = {'address': forms.Textarea(attrs={'rows': 3}),
                   'remarks': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-2 mb-0'),
                Column('name', css_class='form-group col-md-5 mb-0'),
                Column('surname', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            'address',
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('commissioner_country', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                Column('telephone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'language',
            'remarks',
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = ('title', 'short_description', 'exhibit_class', 'date_of_birth', 'frames', 'remarks', 'author', 'publisher', 'year_of_publication', 'pages', 'format', 'frequency', 'availability', 'price')
        widgets = {'short_description': forms.Textarea(attrs={'rows': 5}),
                   'remarks': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'short_description',
            Row(
                Column('exhibit_class', css_class='form-group col-md-6 mb-0'),
                Column('frames', css_class='form-group col-md-3 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'remarks',
            Div(
                HTML('<h6 class="mb-0">Philatelic Literature Details</h6>'),
                HTML('<small class="form-text text-muted">Fill in only if exhibit class is L1-8</small>'),
                'author',
                Row(
                    Column('publisher', css_class='form-group col-md-9 mb-0'),
                    Column('year_of_publication', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('pages', css_class='form-group col-md-4 mb-0'),
                    Column('format', css_class='form-group col-md-5 mb-0'),
                    Column('frequency', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('availability', css_class='form-group col-md-9 mb-0'),
                    Column('price', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Formset('formset'),
                css_class='card card-body bg-light mb-3'
            ),
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class ExhibitParticipationForm(forms.ModelForm):
    class Meta:
        model = ExhibitParticipation
        fields = ('exhibition_level', 'exhibition_name', 'points', 'medal', 'special_prize', 'felicitations')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('exhibition_level', css_class='form-group col-md-3 mb-0'),
                Column('exhibition_name', css_class='form-group col-md-5 mb-0'),
                Column('points', css_class='form-group col-md-2 mb-0'),
                Column('medal', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('special_prize', css_class='form-group col-md-3 mb-0'),
                Column('felicitations', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            # Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class TravelDetailsForm(forms.ModelForm):
    class Meta:
        model = TravelDetails
        fields = ('arrival', 'arrival_flight_number', 'departure', 'departure_flight_number', 'ticket_price', 'spouse', 'spouse_surname', 'spouse_name', 'remarks')
        widgets = {'address': forms.Textarea(attrs={'rows': 3}),
                   'remarks': forms.Textarea(attrs={'rows': 3})}
        widgets = {'arrival': DateTimePicker(options={'sideBySide': True},
                                             attrs={'append': 'fa fa-calendar'}),
                   'departure': DateTimePicker(options={'sideBySide': True},
                                               attrs={'append': 'fa fa-calendar'}),
                   'remarks': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('arrival', css_class='form-group col-md-7 mb-0'),
                Column('arrival_flight_number', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('departure', css_class='form-group col-md-7 mb-0'),
                Column('departure_flight_number', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            'ticket_price',
            'spouse',
            Row(
                Column('spouse_name', css_class='form-group col-md-6 mb-0'),
                Column('spouse_surname', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'remarks',
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )
