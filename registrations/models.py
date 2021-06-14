# Copyright (C) 2019 Antony Chazapis
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import io
import csv

from django.db import models
from django.conf import settings
from django_countries import countries
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from collections import OrderedDict


class ExportMixin():
    @classmethod
    def export_keys(cls):
        return list(cls._export_fields.keys())

    @classmethod
    def export_to_csv(cls):
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(cls.export_keys())
        for instance in cls.objects.all():
            writer.writerow(instance.export_values())
        return stream.getvalue()

    @classmethod
    def export_choices_to_csv(cls, choices):
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(['id', 'value'])
        for key, value in choices:
            writer.writerow([key, value])
        return stream.getvalue()

    @classmethod
    def export_countries_to_csv(cls):
        return cls.export_choices_to_csv(list(countries))

    @classmethod
    def export_to_xlsx(cls, workbook, name):
        row = 0
        worksheet = workbook.add_worksheet(name)
        worksheet.write_row(row, 0, cls.export_keys())
        for instance in cls.objects.all():
            row += 1
            worksheet.write_row(row, 0, instance.export_values())

    @classmethod
    def export_choices_to_xlsx(cls, workbook, name, choices):
        row = 0
        worksheet = workbook.add_worksheet(name)
        worksheet.write_row(row, 0, ['id', 'value'])
        for key, value in choices:
            row += 1
            worksheet.write_row(row, 0, [key, value])

    @classmethod
    def export_countries_to_xlsx(cls, workbook, name):
        return cls.export_choices_to_xlsx(workbook, name, list(countries))

    def export_values(self):
        values = []
        for field in self.__class__._export_fields.values():
            value = getattr(self, field)
            if not value:
                value = ''
            else:
                value = '\n'.join(str(value).splitlines())
            values.append(value)
        return values

class Participant(models.Model, ExportMixin):
    TITLE_CHOICES = [('MR', 'Mr'),
                     ('MRS', 'Mrs'),
                     ('MISS', 'Miss'),
                     ('DR', 'Dr'),
                     ('NONE', 'None')]
    LANGUAGE_CHOICES = [('EN', 'English'),
                        settings.NATIVE_COMMUNICATION_LANGUAGE]

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

    _export_fields = OrderedDict([('id', 'id'),
                                  ('title_id', 'title'),
                                  ('surname', 'surname'),
                                  ('name', 'name'),
                                  ('address', 'address'),
                                  ('country_id', 'country'),
                                  ('email', 'email'),
                                  ('telephone', 'telephone'),
                                  ('mobile', 'mobile'),
                                  ('language_id', 'language'),
                                  ('remarks', 'remarks')])

    @classmethod
    def export_to_csv(cls):
        stream = io.StringIO()
        writer = csv.writer(stream)
        writer.writerow(cls.export_keys() + Appointments.export_keys() + TravelDetails.export_keys())
        for participant in Participant.objects.all():
            appointments = participant.appointments.first() if participant.appointments.count() else Appointments()
            travel_details = participant.travel_details.first() if participant.travel_details.count() else TravelDetails()
            writer.writerow(participant.export_values() + appointments.export_values() + travel_details.export_values())
        return stream.getvalue()

    @classmethod
    def export_to_xlsx(cls, workbook, name):
        row = 0
        worksheet = workbook.add_worksheet(name)
        worksheet.write_row(row, 0, cls.export_keys() + Appointments.export_keys() + TravelDetails.export_keys())
        for participant in Participant.objects.all():
            row += 1
            appointments = participant.appointments.first() if participant.appointments.count() else Appointments()
            travel_details = participant.travel_details.first() if participant.travel_details.count() else TravelDetails()
            worksheet.write_row(row, 0, participant.export_values() + appointments.export_values() + travel_details.export_values())

    def full_name(self):
        return '%s, %s, %s' % (self.surname,
                               self.name,
                               dict(self.TITLE_CHOICES)[self.title])
    full_name.short_description = 'Full name'

    def printout(self, all_fields=False):
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

class Federation(models.Model, ExportMixin):
    country = models.CharField(max_length=32)
    country_code = models.CharField(max_length=2)
    name = models.CharField(max_length=128)
    commissioner_email = models.CharField(max_length=128, null=True, blank=True, help_text='Used if no commissioner has registered')
    email = models.CharField(max_length=128)

    _export_fields = OrderedDict([('id', 'id'),
                                  ('country', 'country'),
                                  ('country_code', 'country_code'),
                                  ('name', 'name'),
                                  ('commissioner_email', 'commissioner_email'),
                                  ('email', 'email')])

    def full_name(self):
        return 'FED %s - %s' % (self.country,
                                self.name)
    full_name.short_description = 'Full name'

    def email_list(self):
        if not self.email:
            return []
        return [address.strip() for address in self.email.split(',')]

    def __str__(self):
        return self.full_name()

class Appointments(models.Model, ExportMixin):
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

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    _export_fields = OrderedDict([('federation_id', 'federation_id'),
                                  ('commissioner', 'commissioner'),
                                  ('jury', 'jury'),
                                  ('apprentice_jury', 'apprentice_jury'),
                                  ('accredited_juror_id', 'accredited_juror'),
                                  ('accredited_juror_disciplines', 'accredited_juror_disciplines'),
                                  ('team_leader', 'team_leader'),
                                  ('team_leader_disciplines', 'team_leader_disciplines')])

    def printout(self, all_fields=False):
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

class Exhibit(models.Model, ExportMixin):
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
                             ('A4', 'A4. Other exhibits (non-competitive)')]
    FRAME_CHOICES = [(0, 'None')] + [(f, f) for f in range(1, 9)]

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
    isbn = models.CharField(max_length=32, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    format = models.CharField(max_length=64, blank=True)
    frequency = models.CharField(max_length=64, blank=True)
    availability = models.CharField(max_length=64, blank=True)
    price = models.CharField(max_length=64, blank=True)

    rejected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)

    _export_fields = OrderedDict([('id', 'id'),
                                  ('registrant_id', 'participant_id'),
                                  ('title', 'title'),
                                  ('short_description', 'short_description'),
                                  ('exhibit_class', 'exhibit_class'),
                                  ('date_of_birth', 'date_of_birth'),
                                  ('frames', 'frames'),
                                  ('introductory_page', 'introductory_page'),
                                  ('synopsis', 'synopsis'),
                                  ('remarks', 'remarks'),
                                  ('author', 'author'),
                                  ('publisher', 'publisher'),
                                  ('year_of_publication', 'year_of_publication'),
                                  ('language', 'language'),
                                  ('isbn', 'isbn'),
                                  ('pages', 'pages'),
                                  ('format', 'format'),
                                  ('frequency', 'frequency'),
                                  ('availability', 'availability'),
                                  ('price', 'price')])

    def printout(self, all_fields=False):
        result = OrderedDict([('Title', self.title),
                              ('Short description', self.short_description),
                              ('Exhibit class', dict(self.EXHIBIT_CLASS_CHOICES)[self.exhibit_class]),
                              ('Frames', self.frames)])
        if all_fields or self.exhibit_class.startswith('Y'):
            result.update(OrderedDict([('Date of birth', self.date_of_birth)]))
        if all_fields or self.exhibit_class.startswith('L'):
            result.update(OrderedDict([('Front cover', os.path.basename(self.introductory_page.path)),
                                       ('Short abstract', os.path.basename(self.synopsis.path) if self.synopsis else ''),
                                       ('Author', self.author),
                                       ('Publisher', self.publisher),
                                       ('Year of publication', self.year_of_publication or ''),
                                       ('Language(s)', self.language),
                                       ('ISBN/ISSN', self.isbn),
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

class ExhibitParticipation(models.Model, ExportMixin):
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

    _export_fields = OrderedDict([('id', 'id'),
                                  ('exhibit_id', 'exhibit_id'),
                                  ('exhibition_level_id', 'exhibition_level'),
                                  ('exhibition_name', 'exhibition_name'),
                                  ('points', 'points'),
                                  ('medal_id', 'medal'),
                                  ('special_prize', 'special_prize'),
                                  ('felicitations', 'felicitations')])

    # def clean(self):
    #     if self.exhibit.participations.count() >= 6:
    #         raise ValidationError('Please enter up to a maximum of 6 participations per exhibit')

    def printout(self, all_fields=False):
        result = OrderedDict([('Exhibition level', dict(self.EXHIBITION_LEVEL_CHOICES)[self.exhibition_level]),
                              ('Exhibition name', self.exhibition_name),
                              ('Points', self.points),
                              ('Award/Medal', dict(self.MEDAL_CHOICES)[self.medal] if self.medal else ''),
                              ('Special prize', 'Yes' if self.special_prize else 'No'),
                              ('Felicitations', 'Yes' if self.felicitations else 'No')])
        return result

class TravelDetails(models.Model, ExportMixin):
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

    _export_fields = OrderedDict([('arrival', 'arrival'),
                                  ('arrival_flight_number', 'arrival_flight_number'),
                                  ('departure', 'departure'),
                                  ('departure_flight_number', 'departure_flight_number'),
                                  ('ticket_price', 'ticket_price'),
                                  ('spouse', 'spouse'),
                                  ('spouse_surname', 'spouse_surname'),
                                  ('spouse_name', 'spouse_name'),
                                  ('hotel', 'hotel'),
                                  ('hotel_website', 'hotel_website'),
                                  ('travel_remarks', 'remarks')])

    def printout(self, all_fields=False):
        result = OrderedDict([('Arrival', self.arrival or ''),
                              ('Arrival flight number', self.arrival_flight_number),
                              ('Departure', self.departure or ''),
                              ('Departure flight number', self.departure_flight_number),
                              ('Ticket price', self.ticket_price),
                              ('Spouse/Partner', 'Yes' if self.spouse else 'No')])
        if all_fields or self.spouse:
            result.update(OrderedDict([('Spouse/Partner name', self.spouse_name),
                                       ('Spouse/Partner surname', self.spouse_surname)]))
        result.update(OrderedDict([('Hotel', self.hotel),
                                   ('Hotel website', self.hotel_website),
                                   ('Remarks', self.remarks)]))
        return result

    def __str__(self):
        return 'Travel Details for ' + self.participant.full_name()
