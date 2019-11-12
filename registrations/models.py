import os

from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from collections import OrderedDict


class Participant(models.Model):
    TITLE_CHOICES = [('MR', 'Mr'),
                     ('MRS', 'Mrs'),
                     ('MISS', 'Miss'),
                     ('DR', 'Dr')]
    LANGUAGE_CHOICES = [('EN', 'English'),
                        ('EL', 'Greek')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=4, choices=TITLE_CHOICES, default='MR')
    surname = models.CharField(max_length=128)
    name = models.CharField(max_length=128, help_text='Include any middle names')
    photo = models.ImageField(blank=True, upload_to='participant/')
    address = models.TextField()
    country = CountryField()
    email = models.CharField(max_length=128)
    telephone = models.CharField(max_length=32, blank=True)
    mobile = models.CharField(max_length=32)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN', help_text='Communication language')
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return '%s, %s, %s' % (self.surname,
                               self.name,
                               dict(self.TITLE_CHOICES)[self.title])
    full_name.short_description = 'Full name'

    def printout(self):
        result = OrderedDict([('Title', dict(self.TITLE_CHOICES)[self.title]),
                              ('Name', self.name),
                              ('Surname', self.surname),
                              ('Photo', os.path.basename(self.photo.path) if self.photo else ''),
                              ('Address', self.address),
                              ('Country', self.country.name),
                              ('Language', dict(self.LANGUAGE_CHOICES)[self.language]),
                              ('Email', self.email),
                              ('Mobile', self.mobile),
                              ('Telephone', self.telephone),
                              ('Remarks', self.remarks)])
        return result

    def __str__(self):
        return self.full_name()

class Federation(models.Model):
    country = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def full_name(self):
        return 'FED %s - %s' % (self.country,
                                self.name)
    full_name.short_description = 'Full name'

    def __str__(self):
        return self.full_name()

class Appointments(models.Model):
    ACCREDITED_JUROR_CHOICES = [('FIP', 'FIP'),
                                ('FEPA', 'FEPA'),
                                ('NAT', 'National')]

    class Meta:
        verbose_name = 'Appointments'
        verbose_name_plural = 'Appointments'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='appointments')

    federation = models.ForeignKey(Federation, on_delete=models.SET_NULL, related_name='appointments', null=True)
    commissioner = models.BooleanField()
    jury = models.BooleanField()
    apprentice_jury = models.BooleanField()
    accredited_juror = models.CharField(max_length=4, blank=True, choices=ACCREDITED_JUROR_CHOICES)
    accredited_juror_disciplines = models.CharField(blank=True, max_length=128)
    team_leader = models.BooleanField()
    team_leader_disciplines = models.CharField(blank=True, max_length=128)

    def printout(self):
        result = OrderedDict([('National federation name', self.federation.full_name() if self.federation else ''),
                              ('Appointed national commissioner', 'Yes' if self.commissioner else 'No'),
                              ('Proposed as jury member', 'Yes' if self.jury else 'No'),
                              ('Proposed as apprentice jury member', 'Yes' if self.apprentice_jury else 'No'),
                              ('Accredited juror', dict(self.ACCREDITED_JUROR_CHOICES)[self.accredited_juror] if self.accredited_juror else ''),
                              ('Accredited juror discipline(s)', self.accredited_juror_disciplines),
                              ('Team leader', 'Yes' if self.team_leader else 'No'),
                              ('Team leader discipline(s)', self.team_leader_disciplines)])
        return result

    def __str__(self):
        return str(self.participant)

class Exhibit(models.Model):
    EXHIBIT_CLASS_CHOICES = [('B1', 'B1. Classe des Champions'),
                             ('C1', 'C1. Traditional Philately'),
                             ('C2', 'C2. Postal History'),
                             ('C3', 'C3. Postal Stationery'),
                             ('C4', 'C4. Aerophilately'),
                             ('C5', 'C5. Astrophilately'),
                             ('C6', 'C6. Revenues'),
                             ('C7', 'C7. Thematic Philately'),
                             ('C8', 'C8. Maximaphily'),
                             ('C9', 'C9. Open Philately'),
                             ('C10', 'C10. Picture Postcards'),
                             ('L1', 'L1. Philatelic Literature – Books of research nature, specialised catalogues'),
                             ('L2', 'L2. Philatelic Literature – Books of promotional and documentary character'),
                             ('L3', 'L3. Philatelic Literature – General catalogues'),
                             ('L4', 'L4. Philatelic Literature – Periodicals'),
                             ('L5', 'L5. Philatelic Literature – Articles (collections of)'),
                             ('L6', 'L6. Philatelic Literature – Websites'),
                             ('L7', 'L7. Philatelic Literature – Software'),
                             ('L8', 'L8. Philatelic Literature – Other digital works'),
                             ('Y1', 'Y1. Youth Philately - Exhibitor’s age (at 1.1.2021) 10-15 years'),
                             ('Y2', 'Y2. Youth Philately - Exhibitor’s age (at 1.1.2021) 16-18 years'),
                             ('Y3', 'Y3. Youth Philately - Exhibitor’s age (at 1.1.2021) 19-21 years'),
                             ('Α4', 'A4. Other exhibits (non-competitive)')]
    FRAME_CHOICES = [(f, f) for f in range(1, 9)]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='exhibits')

    title = models.CharField(max_length=128)
    short_description = models.TextField()
    exhibit_class = models.CharField(max_length=4, choices=EXHIBIT_CLASS_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True, help_text='Youth philately only')
    frames = models.IntegerField(choices=FRAME_CHOICES)
    introductory_page = models.FileField(upload_to='exhibit/')
    synopsis = models.FileField(upload_to='exhibit/', blank=True)
    remarks = models.TextField(blank=True)

    author = models.CharField(max_length=256, blank=True)
    publisher = models.CharField(max_length=128, blank=True)
    year_of_publication = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=64, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=64, blank=True)
    frequency = models.CharField(max_length=64, blank=True)
    availability = models.CharField(max_length=64, blank=True)
    price = models.CharField(max_length=64, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def printout(self):
        result = OrderedDict([('Title', self.title),
                              ('Short description', self.short_description),
                              ('Exhibit class', dict(self.EXHIBIT_CLASS_CHOICES)[self.exhibit_class]),
                              ('Frames', self.frames)])
        if self.exhibit_class.startswith('Y'):
            result.update(OrderedDict([('Date of birth', self.date_of_birth)]))
        if self.exhibit_class.startswith('L'):
            result.update(OrderedDict([('Front cover', os.path.basename(self.introductory_page.path)),
                                       ('Short abstract', os.path.basename(self.synopsis.path) if self.synopsis else ''),
                                       ('Author', self.author),
                                       ('Publisher', self.publisher),
                                       ('Year of publication', self.year_of_publication or ''),
                                       ('Language(s)', self.language),
                                       ('Pages', self.pages or ''),
                                       ('Format', self.format),
                                       ('Frequency', self.frequency),
                                       ('Availability', self.availability),
                                       ('Price', self.price)]))
        else:
            result.update(OrderedDict([('Introductory page', os.path.basename(self.introductory_page.path)),
                                       ('Synopsis', os.path.basename(self.synopsis.path) if self.synopsis else '')]))
        result.update(OrderedDict([('Remarks', self.remarks)]))
        return result

    def __str__(self):
        return self.title

class ExhibitParticipation(models.Model):
    EXHIBITION_LEVEL_CHOICES = [('WORLD', 'FIP World'),
                                ('CONT', 'FEPA/FIAF/FIAP Continental'),
                                ('INT', 'Other International'),
                                ('NAT', 'National')]
    MEDAL_CHOICES = [('GPdH', 'GPd\'H Candidate'),
                     ('GP', 'GP Winner'),
                     ('GPC', 'GP Candidate'),
                     ('LG', 'Large Gold'),
                     ('G', 'Gold'),
                     ('LV', 'Large Vermeil'),
                     ('V', 'Vermeil'),
                     ('LS', 'Large Silver'),
                     ('S', 'Silver'),
                     ('SB', 'Silver Bronze'),
                     ('B', 'Bronze')]

    class Meta:
        verbose_name = 'Exhibit Participation'
        verbose_name_plural = 'Exhibit Participations'

    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE, related_name='participations')

    exhibition_level = models.CharField(max_length=8, choices=EXHIBITION_LEVEL_CHOICES)
    exhibition_name = models.CharField(max_length=128)
    points = models.IntegerField()
    medal = models.CharField(max_length=4, choices=MEDAL_CHOICES, blank=True)
    special_prize = models.BooleanField()
    felicitations = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.exhibit.participations.count() >= 6:
            raise ValidationError('Please enter up to a maximum of 6 participations per exhibit')

    def printout(self):
        result = OrderedDict([('Exhibition level', dict(self.EXHIBITION_LEVEL_CHOICES)[self.exhibition_level]),
                              ('Exhibition name', self.exhibition_name),
                              ('Points', self.points),
                              ('Award/Medal', dict(self.MEDAL_CHOICES)[self.medal] if self.medal else ''),
                              ('Special prize', 'Yes' if self.special_prize else 'No'),
                              ('Felicitations', 'Yes' if self.felicitations else 'No')])
        return result

class TravelDetails(models.Model):
    class Meta:
        verbose_name = 'Travel Details'
        verbose_name_plural = 'Travel Details'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='travel_details')

    arrival = models.DateTimeField(null=True, blank=True)
    arrival_flight_number = models.CharField(max_length=8, blank=True)
    departure = models.DateTimeField(null=True, blank=True)
    departure_flight_number = models.CharField(max_length=8, blank=True)
    ticket_price = models.CharField(max_length=64, blank=True, help_text='If to be paid by the Organising Committee')
    spouse = models.BooleanField()
    spouse_surname = models.CharField(max_length=128, blank=True)
    spouse_name = models.CharField(max_length=128, blank=True, help_text='Include any middle names')
    hotel = models.CharField(max_length=128, blank=True)
    hotel_website = models.CharField(max_length=256, blank=True)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    def printout(self):
        result = OrderedDict([('Arrival', self.arrival or ''),
                              ('Arrival flight number', self.arrival_flight_number),
                              ('Departure', self.departure or ''),
                              ('Departure flight number', self.departure_flight_number),
                              ('Ticket price', self.ticket_price),
                              ('Spouse/Partner', 'Yes' if self.spouse else 'No')])
        if self.spouse:
            result.update(OrderedDict([('Spouse/Partner name', self.spouse_name),
                                       ('Spouse/Partner surname', self.spouse_surname)]))
        result.update(OrderedDict([('Hotel', self.hotel),
                                   ('Hotel website', self.hotel_website),
                                   ('Remarks', self.remarks)]))
        return result

    def __str__(self):
        return 'Travel Details for ' + self.participant.full_name()
