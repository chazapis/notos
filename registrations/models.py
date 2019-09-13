from django.db import models
from django_countries.fields import CountryField


class Participant(models.Model):
    TITLE_CHOICES = {('MR', 'Mr'),
                     ('MRS', 'Mrs'),
                     ('MISS', 'Miss'),
                     ('DR', 'Dr')}
    LANGUAGE_CHOICES = {('EN', 'English'),
                        ('EL', 'Greek')}

    title = models.CharField(max_length=8, choices=TITLE_CHOICES, default='MR')
    surname = models.CharField(max_length=128)
    name = models.CharField(max_length=128, help_text='Please include any middle names')
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
