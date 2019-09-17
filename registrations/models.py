from django.db import models
from django_countries.fields import CountryField


class Participant(models.Model):
    TITLE_CHOICES = [('MR', 'Mr'),
                     ('MRS', 'Mrs'),
                     ('MISS', 'Miss'),
                     ('DR', 'Dr')]
    LANGUAGE_CHOICES = [('EN', 'English'),
                        ('EL', 'Greek')]

    title = models.CharField(max_length=4, choices=TITLE_CHOICES, default='MR')
    surname = models.CharField(max_length=128)
    name = models.CharField(max_length=128, help_text='Include any middle names')
    address = models.TextField()
    country = CountryField()
    commissioner_country = CountryField(blank=True, help_text='State here if you are a national commissioner for another country')
    telephone = models.CharField(max_length=32, blank=True)
    mobile = models.CharField(max_length=32)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN', help_text='Communication language')
    remarks = models.TextField(blank=True)

    def full_name(self):
        return '%s, %s, %s' % (self.surname,
                               self.name,
                               dict(self.TITLE_CHOICES)[self.title])
    full_name.short_description = 'Full name'

    def __str__(self):
        return self.full_name()

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
                             ('Y3', 'Y3. Youth Philately - Exhibitor’s age (at 1.1.2021) 19-21 years')]
    FRAME_CHOICES = [(f, f) for f in (1, 2, 4, 6, 8)]

    title = models.CharField(max_length=128)
    short_description = models.TextField()
    exhibit_class = models.CharField(max_length=4, choices=EXHIBIT_CLASS_CHOICES)
    date_of_birth = models.DateField(blank=True, help_text='Youth phiilately only')
    frames = models.IntegerField(choices=FRAME_CHOICES)
    remarks = models.TextField(blank=True)

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

class ExhibitParticipation(models.Model):
    EXHIBITION_LEVEL_CHOICES = [('WORLD', 'FIP World'),
                                ('CONT', 'FEPA/FIAF/FIAP Continental'),
                                ('INT', 'Other International'),
                                ('NAT', 'National')]
    MEDAL_CHOICES = [('LG', 'Large Gold'),
                     ('G', 'Gold'),
                     ('LV', 'Large Vermeil'),
                     ('V', 'Vermeil'),
                     ('LS', 'Large Silver'),
                     ('S', 'Silver'),
                     ('SB', 'Silver Bronze'),
                     ('B','Bronze')]

    exhibition_level = models.CharField(max_length=8, choices=EXHIBITION_LEVEL_CHOICES)
    exhibition_name = models.CharField(max_length=128)
    points = models.IntegerField()
    medal = models.CharField(max_length=2, choices=MEDAL_CHOICES, blank=True)
    special_prize = models.BooleanField()
    felicitations = models.BooleanField()

    exhibit = models.ForeignKey(Exhibit, on_delete=models.CASCADE, related_name='participations')
