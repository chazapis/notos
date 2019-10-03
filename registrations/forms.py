from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, Column, Submit, HTML
from tempus_dominus.widgets import DateTimePicker

from .models import Participant, Official, Exhibit, ExhibitParticipation, TravelDetails
from .layout import Formset


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('title', 'surname', 'name', 'photo', 'address', 'country', 'telephone', 'mobile', 'language', 'remarks')
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
            'photo',
            # HTML("""{% if form.photo.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.photo.value }}">{% endif %}""", ),
            'address',
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('language', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('mobile', css_class='form-group col-md-6 mb-0'),
                Column('telephone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'remarks',
            HTML('<div class="alert alert-warning small" role="alert">By submitting this entry form the exhibitor accepts the Regulations listed in article 2.1. and confirms the truthfulness of all data entered.</div>'),
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class OfficialForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = ('federation', 'commissioner', 'jury', 'apprentice_jury', 'accredited_juror', 'accredited_juror_disciplines', 'team_leader', 'team_leader_disciplines')
        labels = {'federation': 'National federation name',
                  'commissioner': 'Appointed national commissioner',
                  'jury': 'Proposed as jury member',
                  'apprentice_jury': 'Proposed as apprentice jury member',
                  'accredited_juror_disciplines': 'Accredited juror discipline(s)',
                  'team_leader_disciplines': 'Team leader discipline(s)'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'federation',
            'commissioner',
            'jury',
            'apprentice_jury',
            'accredited_juror',
            'accredited_juror_disciplines',
            'team_leader',
            'team_leader_disciplines',
            HTML('<div class="alert alert-warning small" role="alert">By submitting this entry form the exhibitor accepts the Regulations listed in article 2.1. and confirms the truthfulness of all data entered.</div>'),
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields = ('title', 'short_description', 'exhibit_class', 'date_of_birth', 'frames', 'cover', 'remarks', 'author', 'publisher', 'year_of_publication', 'language', 'pages', 'format', 'frequency', 'availability', 'price')
        labels = {'cover': 'Introductory page and Synopsis (Front cover and Short abstract if Philatelic Literature)'}
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
            'cover',
            'remarks',
            Div(
                HTML('<h6 class="mb-0">Previous Participations</h6>'),
                Formset('formset'),
                css_class='card card-body bg-light mb-3 pb-0'
            ),
            Div(
                HTML('<h6 class="mb-0">Philatelic Literature Details</h6>'),
                HTML('<small class="form-text text-muted">Fill in only if exhibit class is L1-L8</small>'),
                'author',
                Row(
                    Column('publisher', css_class='form-group col-md-9 mb-0'),
                    Column('year_of_publication', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('language', css_class='form-group col-md-3 mb-0'),
                    Column('pages', css_class='form-group col-md-2 mb-0'),
                    Column('format', css_class='form-group col-md-4 mb-0'),
                    Column('frequency', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('availability', css_class='form-group col-md-9 mb-0'),
                    Column('price', css_class='form-group col-md-3 mb-0'),
                    css_class='form-row'
                ),
                css_class='card card-body bg-light mb-3'
            ),
            HTML('<div class="alert alert-warning small" role="alert">By submitting this entry form the exhibitor accepts the Regulations listed in article 2.1. and confirms the truthfulness of all data entered.</div>'),
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )

class ExhibitParticipationForm(forms.ModelForm):
    class Meta:
        model = ExhibitParticipation
        fields = ('exhibition_level', 'exhibition_name', 'points', 'medal', 'special_prize', 'felicitations')
        labels = {'medal': 'Award/Medal',
                  'special_prize': 'SP',
                  'felicitations': 'F'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'

class TravelDetailsForm(forms.ModelForm):
    class Meta:
        model = TravelDetails
        fields = ('arrival', 'arrival_flight_number', 'departure', 'departure_flight_number', 'ticket_price', 'spouse', 'spouse_surname', 'spouse_name', 'hotel', 'hotel_website', 'remarks')
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
            Row(
                Column('hotel', css_class='form-group col-md-6 mb-0'),
                Column('hotel_website', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'remarks',
            HTML('<div class="alert alert-warning small" role="alert">By submitting this entry form the exhibitor accepts the Regulations listed in article 2.1. and confirms the truthfulness of all data entered.</div>'),
            Submit('submit', 'Submit', css_class='btn-success btn-lg btn-block')
        )
